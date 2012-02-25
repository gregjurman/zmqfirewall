import bases

class DropMessage(bases.Action):
    def action(message):
        log.info('Message %r dropped' % message)

class AcceptMessage(bases.Action):
    def action(message):
        return message
