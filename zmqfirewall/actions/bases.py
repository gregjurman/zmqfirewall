import logging

log = logging.getLogger('zmqfirewall.action')

class ActionMeta(type):
    registered_actions = {}

    def __new__(mcs, name, bases, dct):
        if name != 'Action':
            if 'action' not in dct or not callable(dct['action']):
                raise AttributeError, '%s is missing an action callback' % name

        ins = type.__new__(mcs, name, bases, dct)

        return ins

class Action(object):
    __metaclass__ = ActionMeta
    
    action = None

    def __new__(cls, **kw):
        ins = type(cls.__name__, (cls,), kw)

        return ins

