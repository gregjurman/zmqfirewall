import logging

core_log = logging.getLogger('zmqfirewall.core')
action_log = logging.getLogger('zmqfirewall.action')

__all__ = ['Action']


class ActionMeta(type):
    _registered_actions = {}
    _action_index = {}

    def __new__(mcs, name, bases, dct):
        if name != 'Action':
            if 'action' not in dct or not callable(dct['action']):
                raise AttributeError('%s is missing an action callback' % name)
        else:
            return type.__new__(mcs, name, bases, dct)

        ins = type.__new__(mcs, name, bases, dct)

        # This works if the action doesn't expect any __init__
        handler = None
        try:
            handler = ins.req()
            # Short ciruit
            ins.action = handler.action
        except TypeError:
            pass

        if 'no_register' not in dct or not dct['no_register']:
            mcs.register(name, ins, handler)

        return ins


    @classmethod
    def register(mcs, name, ins, handler):
        if name not in [x.__name__ for x in mcs._registered_actions]:
            if ins.name is None:
                # Rip of the word action from the end if it is there
                _iname = ins.__name__.lower()
                index_name = _iname[::-1].replace('noitca', '', 1)[::-1]
            else:
                index_name = ins.name

            if index_name in mcs._action_index:
                # Hold on, something is trying to overwrite a regged action
                raise NameError("Action named '%s' already registered!" %
                                index_name)

            mcs._registered_actions[ins] = handler
            mcs._action_index[index_name] = ins

            core_log.info("Added %s to action registry as '%s'" %
                            (name, index_name))
        else:
            raise TypeError("%s is already registered!" % name)


    @classmethod
    def get_action_by_name(mcs, name):
        return mcs._registered_actions[mcs._action_index[name]]

    @classmethod
    def deregister(mcs, name):
        core_log.info("De-registering '%s' action!" % name)
        del mcs._registered_actions[mcs._action_index[name]]
        del mcs._action_index[name]

    @classmethod
    def deregisterAll(mcs):
        core_log.info("De-registering all actions!")
        mcs._registered_actions.clear()
        mcs._action_index.clear()

class Action(object):
    """Base action handler"""
    __metaclass__ = ActionMeta

    action = (lambda: None)
    log_message = True
    name = None

    @classmethod
    def register(cls):
        handler = None
        try:
            handler = cls.req()
            cls.action = handler.action
        except TypeError:
            pass

        ActionMeta.register(cls.__name__, cls, handler)

    @classmethod
    def req(cls, **kw):
        """
        Handle the action.
        """
        ins = cls.__new__(cls)
        ins.__init__(**kw)

        return ins

    def __call__(self, message):
        return self.action(message)
