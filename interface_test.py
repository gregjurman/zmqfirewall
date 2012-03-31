from __future__ import print_function

from zmqfirewall.core.interface import Interface
from zmqfirewall.core.reactor import reactor
from zmqfirewall.utils import get_interface

# Define a helper that generates messages for us
from math import sin, radians
def sin_gen():
    i = 0
    while True:
        yield sin(radians(i))
        i = i + 1


# Right now any subscribing interfaces that rely on defined publishing
# interfaces need to be declared after the publishing interface



class FakeExternalPublisher(Interface):
    """
        Our fake 'external server' that is pushing messages 
        into the firewall. 
    """
    connection_uri = 'pub-tcp://0.0.0.0:7000'
    name = 'fake_incoming'


class SineMessagePublisher(Interface):
    """
        Our publisher for sending our 'sine messages' to other
        parts of the firewall
    """
    connection_uri = 'pub-ipc:///tmp/sinemessages'
    name = 'ipc_sine_pub'


class IntegerOnlySubscriber(Interface):
    """
        This subscriber prints only integer numbers
    """
    name = 'integer_only'
    connection_uri = 'sub-ipc:///tmp/sinemessages'
    topics = ['integers']
    filter = (lambda x: print("Integer got: %s" % x.body))


class NonIntegerOnlySubscriber(Interface):
    """
        This subscriber only prints non-integer(float) numbers
    """
    name = 'non_integer_only'
    connection_uri = 'sub-ipc:///tmp/sinemessages'
    topics = ['non_integers']
    filter = (lambda x: print("Float got: %s" % x.body))


def routing_filter(message):
    '''
        Our routing function/filter that is called whenever a
        message comes in. This sorts out messages into integers
        and non-integers, then publishes them to our IPC based
        socket.
    '''
    if message.body in ['0.0', '1.0']:
        message.topic = 'integers'
    else:
        message.topic = 'non_integers'
    get_interface('ipc_sine_pub').send_out(message)


class MessageRoutingSubscriber(Interface):
    """
        This is our incoming subcriber that listens for messages from
        the 'sinewave' topic.
    """
    connection_uri = 'sub-tcp://localhost:7000'
    name = 'messagerouter'
    topics = ['sinewave']
    filter = routing_filter
   

def test_pubsub():
    '''
        because we are internally generating messages (rather than being a daemon)
        We need to generate some traffic, we'll use our fake incoming publisher
        to do so.
    '''
    sin_wave = sin_gen()
    def publish():
        get_interface('fake_incoming').publish(str(sin_wave.next()), 'sinewave')
        reactor.callLater(1, publish)

    reactor.callLater(1, publish)

    reactor.run()

if __name__ == "__main__":
    test_pubsub()
