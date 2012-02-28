import base
from zmqfirewall.utils import get_action

__all__ = ['DropMessageAction', 'AcceptMessageAction', 'FilterTopicAction']

class DropMessageAction(base.Action, Exception):
    """An Action that drops any message that comes in."""

    name = "drop"

    def action(self, message):
        # When you see this you will WAT.
        raise self

class AcceptMessageAction(base.Action):
    """Action that accepts any message that comes in."""

    log_action = False # We don't want to log every accepted message

    name = "accept"

    def action(self, message):
        return message

class FilterTopicAction(base.Action):
    no_register = True

    def __init__(self, topics, on_success=AcceptMessageAction, on_failure=DropMessageAction):
        self.topics = topics
        if isinstance(on_failure, str):
            self.on_failure = get_action(on_failure)
        elif issubclass(on_failure.__class__, base.ActionMeta):
            self.on_failure = on_failure
        else:
            raise ValueError, 'on_failure must be a string or Action, got %r' % on_failure

        if isinstance(on_success, str):
            self.on_success = get_action(on_success)
        elif issubclass(on_success.__class__, base.ActionMeta):
            self.on_success = on_success
        else:
            raise ValueError, 'on_success must be a string or Action, got %r' % on_success

    def action(self, message):
        if message.topic in self.topics:
            return self.on_success.action(message)
        else:
            return self.on_failure.action(message)
