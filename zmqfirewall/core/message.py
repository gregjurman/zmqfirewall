class ZMQMessage(object):
    def __init__(self, message, tag, interface=None):
        self.message = message
        self.topic = tag
        self.interface = interface

    def get_topic(self):
        return self.topic

    def set_topic(self, value):
        if isinstance(value, str):
            self.topic = value
        else:
            raise ValueError, "value must be a str object"

    def del_topic(self):
        self.topic = None

    topic = property(get_topic, set_topic, del_topic, "Message topic")

    def get_body(self):
        return self.message

    def set_body(self, value):
        if isinstance(value, str):
            self.message = value
        else:
            raise ValueError, "value must be a str object"

    def del_body(self):
        self.message = None
        
    body = property(get_body, set_body, del_body, "Message body")
