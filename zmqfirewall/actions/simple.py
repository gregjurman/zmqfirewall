import bases

class DropMessageAction(bases.Action):
    """An Action that drops any message that comes in."""

    name = "drop"

    def action(self, message):
        pass

class AcceptMessageAction(bases.Action):
    """Action that accepts any message that comes in."""

    log_action = False # We don't want to log every accepted message

    name = "accept"

    def action(self, message):
        return message
