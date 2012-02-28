import zmqfirewall.filters
from zmqfirewall.actions import AcceptMessageAction, FilterTopicAction
from zmqfirewall.utils.lookup import get_filter

from nose.tools import eq_

from tests.helper import Message

test_msg = Message("I am the cheese", "localhost", topic="log_message")
bad_test_msg = Message("I am not the cheese", "localhost", topic="bad_topic")

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

