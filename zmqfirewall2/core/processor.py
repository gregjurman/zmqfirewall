from reactor import reactor

from twisted.internet import protocol

import txZMQ
import zmq
import time

import logging

log = logging.getLogger('zmqfirewall.core')

class BasicProcessor(object):
    def __init__(self):
        self.context = zmq.Context(1)

        self.outbound_socket = self.context.socket(zmq.PUB)
        self.outbound_socket.bind('tcp://*:6500')

        self.twisted_zmq_factory = txZMQ.ZmqFactory()

        self.inbound = txZMQ.ZmqEndpoint("connect", 'tcp://127.0.0.1:6501')

        time.sleep(1)
