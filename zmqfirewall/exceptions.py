from zmqfirewall.utils import get_action
from zmqfirewall.actions.base import ActionMeta

class DivertAction(Exception):
    def __init__(self, new_action):
        if isinstance(new_action, str):
            self.action = get_action(new_action).action
        elif issubclass(new_action.__class__, ActionMeta):
            self.action = new_action.action
        else:
            raise ValueError, 'new_action must be a string or Action, got %r' % new_action

    def __call__(self, message):
        return self.action(message)

class InterruptAction(DivertAction):
    pass
