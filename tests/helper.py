class Message(object):
    def __init__(self, body, from_host, topic=None):
        self.from_host = from_host
        self.topic = topic
        self.body = body
        self.topic = topic

    def __repr__(self):
        return "<Message: from=%s, topic=%s>" % (
            self.from_host,
            self.topic,
        )

    def __str__(self):
        return self.body
