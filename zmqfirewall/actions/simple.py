import bases

class DropMessageAction(bases.Action):
    """An Action that drops any message that comes in."""

    def action(self, message):
        pass

class AcceptMessageAction(bases.Action):
    """Action that accepts any message that comes in."""

    log_action = False # We don't want to log every accepted message

    def action(self, message):
        return message
