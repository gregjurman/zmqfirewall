import actions

class Message(object):
    def __init__(self, from_host, message, topic=None, def_action=actions.pass_on):
        self.from_host = from_host
        self.topic = topic
        self.message = message
        self.topic = topic
        self.default_action = action

    def __repr__(self):
        return "<Message: from=%s, topic=%s, action=%s>" % (
            self.from_host,
            self.topic,
            self.action,
        )
