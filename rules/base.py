import logging
import moksha.firewall.actions

__all__ = ['Rule']

core_log = logging.getLogger('moksha.firewall.core')
rule_log = logging.getLogger('moksha.firewall.rule')

class RuleMeta(type):
    _registered_rules = {}
    _rule_index = {}

    def __new__(mcs, name, bases, dct):
        if name != 'Rule':
            if 'filter_chain' not in dct or not isinstance(dct['filter_chain'], list):
                raise AttributeError, '%s does not have a valid filter_chain' % name
        else:
            return type.__new__(mcs, name, bases, dct)

        ins = type.__new__(mcs, name, bases, dct)

        if name not in [x.__name__ for x in mcs._registered_rules]:
            handler = ins.req()

            if ins.name is None:
                # Rip of the word action from the end if it is there
                index_name = ins.__name__.lower()[::-1].replace('elur', '', 1)[::-1]
            else:
                index_name = ins.name

            if index_name in mcs._rule_index:
                # Hold on, something is trying to overwrite a registered action
                raise NameError, "A rule named '%s' is already registered!" % index_name

            mcs._registered_rules[ins] = handler
            mcs._rule_index[index_name] = ins

            core_log.info("Added %s to rule registry as '%s'" % (name, index_name))
        else:
            raise TypeError, "%s is already registered!" % name

        return ins

    @classmethod
    def get_rule_by_name(mcs, name):
        return mcs._registered_rules[mcs._rule_index[name]]


class Rule(object):
    """Base action handler"""
    __metaclass__ = RuleMeta

    filter_chain = None

    name = None

    @classmethod
    def req(cls, **kw):
        """
        Handle the action.
        """
        ins = object.__new__(cls)
        ins.__init__(**kw)

        return ins
