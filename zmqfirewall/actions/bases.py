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
    """Base action handler"""
    __metaclass__ = ActionMeta
    
    action = (lambda: None)

    log_message = True

    @classmethod
    def req(cls, msg, **kw):
        """
        Handle the action.
        """
        ins = object.__new__(cls)
        ins.__init__(**kw)
        
        return ins.action(msg)


    def __new__(cls, **kw):
        """Return a new action handler class."""
        return type("%s_s" % cls.__name__, (cls,), cls.__dict__)

    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)

