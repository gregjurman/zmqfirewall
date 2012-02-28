class Message(object):
    def __init__(self, message, from_host, topic=None):
        self.from_host = from_host
        self.topic = topic
        self.message = message
        self.topic = topic

    def __repr__(self):
        return "<Message: from=%s, topic=%s>" % (
            self.from_host,
            self.topic,
        )

    def __str__(self):
        return self.message
