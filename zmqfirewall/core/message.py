from zmq.core.message import Frame

class ZeroMQMessage(Frame):
    def __init__(self, data=None, **kw):
        self.__split_cache = data.split('\0', 1)
        if len(self.__split_cache) == 1:
            self.__split_cache.insert(0, None)

        super(ZeroMQMessage, self).__init__(data, **kw)

    def get_topic(self):
        return self.__split_cache[0]

    def set_topic(self, value):
        if isinstance(value, str):
            self.__split_cache[0] = value
        else:
            raise ValueError, "value must be a str object"

    def del_topic(self):
        self.__split_cache[0] = None

    topic = property(get_topic, set_topic, del_topic, "Message topic")

    def get_body(self):
        return self.__split_cache[1]

    def set_body(self, value):
        if isinstance(value, str):
            self.__split_cache[1] = value
        else:
            raise ValueError, "value must be a str object"

    def del_body(self):
        self.__split_cache[1] = None
        
    body = property(get_body, set_body, del_body, "Message body")

    def prepare(self):
        if not self.__split_cache[0]:
            self.data = self.__split_cache[1]
        else:
            self.data = "\0".join(self.__split_cache)
