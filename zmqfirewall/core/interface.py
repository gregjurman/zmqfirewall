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
    print "Running deferreds"
    for call in _deferred_calls:
        call()

reactor.callLater(0, do_deferreds)

class InterfaceMeta(type):
    registered_interfaces = {}

    def __new__(mcs, name, _bases, dct):
        print name, dct

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
            host = uri_properties['uri'],
            topics = topics,
            hwm = dct['hwm'] if 'hwm' in dct else 0,
            identity = dct['identity'] if 'identity' in dct else None,
            filter = dct['filter'] if 'filter' in dct else None)

        ins = type.__new__(mcs, name, bases, {})(**new_dct)
       
        mcs.registered_interfaces[dct['name']] = ins

        return ins

    @classmethod
    def get_interface_by_name(mcs, name):
        return mcs.registered_interfaces[name]


class Interface(object):
    __metaclass__ = InterfaceMeta


class ZMQSubscriberInterface(txzmq.ZmqSubConnection):
    def __init__(self, host, topics=None, **kw):
        super(ZMQSubscriberInterface, self).__init__(factory)

        if not isinstance(topics, list):
            topics = list((topics,))

        deferred(self.connectTo, host)

        for topic in topics:
            deferred(self.subscribe, topic)

    def get_host(self):
        return [endpoint.address for endpoint in self.endpoints]

    in_host = property(get_host)

    out_host = property((lambda: None))

    def gotMessage(self, message, tag):
        print message, tag
        msg = ZMQMessage(message, tag, self)
        self.filter(msg)
        
    def connectTo(self, host):
        self.addEndpoints([txzmq.ZmqEndpoint('connect', host)])

    def send_out(self, message):
        raise NotImplementedError("Not supported")


class ZMQPublisherInterface(txzmq.ZmqPubConnection):
    def __init__(self, host, identity=None, hwm=0, **kw):
        print factory, host, identity
        super(ZMQPublisherInterface, self).__init__(factory, 
                txzmq.ZmqEndpoint('bind', host), identity)

    def get_host(self):
        raise NotImplementedError("We have no idea how to see who is connected")

    def send_out(self, message):
        self.publish(message.body, message.topic)

    out_host = property(get_host)

    in_host = property((lambda: None))
