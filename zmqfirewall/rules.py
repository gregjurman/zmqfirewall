import actions


class AbstractRule(object):
    def incoming(self, host, message):
        return actions.pass_on

    def outgoing(self, host, message):
        return actions.pass_on


class SimpleIPRule(object):
    allowed_incoming = None
    allowed_outgoing = None
    
    denied_incoming = None
    denied_outgoing = None

    def incoming(self, host, message):
        pass

    def outgoing(self, host, message):
        pass
