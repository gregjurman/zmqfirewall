import txzmq
from message import ZMQMessage
import re

import functools
from reactor import reactor

factory = txzmq.ZmqFactory()

connection_string_regex = re.compile(r'^(?P<type>[\w]{3,4})-(?P<uri>.*)$')

_deferred_calls = []


def deferred(func, *args, **kw):
    defer = functools.partial(func, *args, **kw)
    _deferred_calls.append(defer)


def early_deferred(func, *args, **kw):
    defer = functools.partial(func, *args, **kw)
    _deferred_calls.insert(0, defer)


def do_deferreds():
    for call in _deferred_calls:
        call()

reactor.callLater(0, do_deferreds)


class InterfaceMeta(type):
    registered_interfaces = {}

    def __new__(mcs, name, _bases, dct):
        if name is "Interface":
            return type.__new__(mcs, name, _bases, dct)

        if not 'connection_uri' in dct:
            raise AttributeError('missing connection_uri parameter')

        matches = connection_string_regex.match(dct['connection_uri'])
        uri_properties = matches.groupdict()

        bases = (object, )
        if uri_properties['type'] == 'sub':
            bases = (ZMQSubscriberInterface, Interface, )
        elif uri_properties['type'] == 'pub':
            bases = (ZMQPublisherInterface, Interface, )
        elif uri_properties['type'] == 'push':
            bases = (ZMQPushInterface, Interface, )
        elif uri_properties['type'] == 'pull':
            bases = (ZMQPullInterface, Interface, )
        else:
            raise NotImplementedError('%s socket type not implemented yet.' %
                                      uri_properties['type'])

        topics = []
        if 'topics' in dct:
            topics = dct['topics']
            if isinstance(topics, str):
                topics = [topics]
            elif not hasattr(topics, '__iter__'):
                raise AttributeError('topics must be iterable')

        new_dct = dict(
            host=uri_properties['uri'],
            topics=topics,
            hwm=dct['hwm'] if 'hwm' in dct else 0,
            identity=dct['identity'] if 'identity' in dct else None,
            filter=dct['filter'] if 'filter' in dct else None)

        ins = type.__new__(mcs, name, bases, {
                           'highWaterMark': new_dct['hwm']
                           })

        deferred(mcs.register, ins, dct['name'], new_dct)

        return ins

    @classmethod
    def register(mcs, cls, name, new_dct):
        ins = cls(**new_dct)
        mcs.registered_interfaces[name] = ins

    @classmethod
    def get_interface_by_name(mcs, name):
        return mcs.registered_interfaces[name]

    @classmethod
    def shutdown_all(mcs):
        for interface in mcs.registered_interfaces.values():
            interface.shutdown()


class Interface(object):
    __metaclass__ = InterfaceMeta

    @classmethod
    def shutdown(self):
        InterfaceMeta.shutdown_all()


class ZMQSubscriberInterface(txzmq.ZmqSubConnection):
    def __init__(self, host, topics=None, filter=None, **kw):
        super(ZMQSubscriberInterface, self).__init__(factory)

        if topics and not isinstance(topics, list):
            topics = list((topics,))

        self.connectTo(host)

        if topics:
            for topic in topics:
                self.subscribe(topic)

        self.filter = filter

    def get_host(self):
        return [endpoint.address for endpoint in self.endpoints]

    in_host = property(get_host)

    out_host = property((lambda: None))

    def gotMessage(self, message, tag):
        msg = ZMQMessage(message, tag, self)
        self.filter(msg)

    def connectTo(self, host):
        self.addEndpoints([txzmq.ZmqEndpoint('connect', host)])

    def send_out(self, message):
        raise NotImplementedError("Not supported")


class ZMQPublisherInterface(txzmq.ZmqPubConnection):
    def __init__(self, host, identity=None, **kw):
        super(ZMQPublisherInterface,
              self).__init__(factory,
                             txzmq.ZmqEndpoint('bind', host), identity)

    def send_out(self, message):
        self.publish(message.body, message.topic)

    def get_host(self):
        raise NotImplementedError("No idea how to see who is connected")

    out_host = property(get_host)

    in_host = property((lambda: None))


class ZMQPushInterface(txzmq.ZmqPushConnection):
    def __init__(self, host, identity=None, **kw):
        super(ZMQPushInterface,
              self).__init__(factory,
                             txzmq.ZmqEndpoint('bind', host), identity)

    def send_out(self, message):
        self.push(message.body)

    def get_host(self):
        raise NotImplementedError("No idea how to see who is connected")

    out_host = property(get_host)

    in_host = property((lambda: None))


class ZMQPullInterface(txzmq.ZmqPullConnection):
    def __init__(self, host, filter=None, **kw):
        super(ZMQPullInterface, self).__init__(factory)

        self.connectTo(host)

        self.filter = filter

    def get_host(self):
        return [endpoint.address for endpoint in self.endpoints]

    in_host = property(get_host)

    out_host = property((lambda: None))

    def onPull(self, message):
        msg = ZMQMessage(message[0], None, self)
        self.filter(msg)

    def connectTo(self, host):
        self.addEndpoints([txzmq.ZmqEndpoint('connect', host)])

    def send_out(self, message):
        raise NotImplementedError("Not supported")
