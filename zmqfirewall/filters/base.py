import logging
import zmqfirewall.firewall.actions
from zmqfirewall.firewall.exceptions import DivertAction

from collections import deque

__all__ = ['FirewallFilter']

core_log = logging.getLogger('zmqfirewall.firewall.core')
filter_log = logging.getLogger('zmqfirewall.firewall.filter')

class FilterMeta(type):
    _registered_filters = {}
    _filter_index = {}

    def __new__(mcs, name, bases, dct):
        if name != 'FirewallFilter':
            if 'chain' not in dct or not isinstance(dct['chain'], list):
                raise AttributeError, '%s does not have a valid chain' % name
        else:
            return type.__new__(mcs, name, bases, dct)

        if 'name' not in dct or dct['name'] is None:
            # Rip of the word filter from the end if it is there
            dct['name'] = name.lower()[::-1].replace('retlif', '', 1)[::-1]
        
        ins = type.__new__(mcs, name, bases, dct)

        index_name = ins.name

        if name not in [x.__name__ for x in mcs._registered_filters]:
            handler = ins.req()

            if index_name in mcs._filter_index:
                # Hold on, something is trying to overwrite a registered filter
                raise NameError, "A filter named '%s' is already registered!" % index_name

            mcs._registered_filter[ins] = handler
            mcs._filter_index[index_name] = ins

            core_log.info("Added %s to filter registry as '%s'" % (name, index_name))
        else:
            raise TypeError, "%s is already registered!" % name

        return ins

    @classmethod
    def get_filter_by_name(mcs, name):
        return mcs._registered_filter[mcs._filter_index[name]]


class FirewallFilter(object):
    """Base filter handler"""
    __metaclass__ = FilterMeta

    chain = None

    name = None

    @classmethod
    def req(cls, **kw):
        """
        Handle the action.
        """
        ins = object.__new__(cls)
        ins.__init__(**kw)

        return ins

    def __call__(self, message):
        actions = deque(self.chain)

        while(len(actions) > 0):
            try:
                out = action(message)
            except DivertAction as diversion:
                # Append the diversion so its run next
                actions.appendleft(diversion) 