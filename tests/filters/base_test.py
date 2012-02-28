import zmqfirewall.filters
from zmqfirewall.actions import AcceptMessageAction, FilterTopicAction
from zmqfirewall.utils import get_filter, divert

from nose.tools import eq_

from tests.helper import Message

test_msg = Message("I am the cheese", "localhost", topic="log_message")
bad_test_msg = Message("I am the ham", "localhost", topic="bad_topic")

def test_basic_filter():
    class TestFilter(zmqfirewall.filters.FirewallFilter):
        chain = [
            FilterTopicAction(['test_topic']),
            AcceptMessageAction
        ]

    eq_('test', TestFilter.name)

def test_basic_filter_2():
    class AnotherTestFilter(zmqfirewall.filters.FirewallFilter):
        chain = [
            FilterTopicAction(['log_message']),
            AcceptMessageAction
        ]
        name = "iamthecheese"

    eq_('iamthecheese', AnotherTestFilter.name)

def test_basic_filter_process():
    filt = get_filter('iamthecheese')

    out = filt(test_msg)
    eq_(test_msg, out)

    out = filt(bad_test_msg)
    eq_(None, out)


def bad_filter_chain_test():
    try:
        class BadChainFilter(zmqfirewall.filters.FirewallFilter):
            pass
        assert(False)
    except Exception as e:
        eq_(str(e), 'BadChainFilter does not have a valid chain')
        

def duplicate_filter_name_test():
    try:
        class IAmTheCheeseFilter(zmqfirewall.filters.FirewallFilter):
            chain = [AcceptMessageAction]
        assert(False)
    except Exception as e:
        eq_(str(e), "A filter named 'iamthecheese' is already registered!")

def filter_already_registered_test():
    try:
        class AnotherTestFilter(zmqfirewall.filters.FirewallFilter):
            chain = [AcceptMessageAction]
        assert(False)
    except Exception as e:
        eq_(str(e), "AnotherTestFilter is already registered!")



class AppendHelloAction(zmqfirewall.actions.Action):
    def action(self, message):
        message.body = "Hello, %s" % message.body
        return message

class FilterCheeseAction(zmqfirewall.actions.Action):
    def action(self, message):
        if 'cheese' in message.body.split(' '):
            divert(AppendHelloAction)
        else:
            return message

def divert_filter_test():
    class DivertFilterTestFilter(zmqfirewall.filters.FirewallFilter):
        chain = [FilterCheeseAction]

    out = DivertFilterTestFilter.handle(test_msg)
    eq_(str(out), 'Hello, I am the cheese')

def interrupt_filter_test():
    pass

