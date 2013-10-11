import zmqfirewall.filters as zmf
from zmqfirewall.filters.base import FilterMeta
from zmqfirewall.actions import AcceptMessageAction, FilterTopicAction, Action
from zmqfirewall.utils import get_filter, divert, interrupt

from nose.tools import eq_, assert_is_none, assert_is_not_none, raises
from unittest import TestCase
from tests.helper import Message


class AppendHelloAction(Action):
    def action(self, message):
        message.body = "Hello, %s" % message.body
        return message


class DivertFilterCheeseAction(Action):
    def action(self, message):
        if 'cheese' in message.body.split(' '):
            divert(AppendHelloAction)
        else:
            return message


class InterruptFilterCheeseAction(Action):
    def action(self, message):
        if 'cheese' in message.body.split(' '):
            interrupt('appendhello')
        else:
            return message


class AppendNotCheeseAction(Action):
    def action(self, message):
        message.body = "%s. I am not the cheese" % message.body
        return message


class FilterTest(TestCase):
    def setUp(self):
        # clean up all filters just in case
        FilterMeta.deregisterAll()


    def defineCheese(self):
        class AnotherTestFilter(zmf.FirewallFilter):
            chain = [
                FilterTopicAction(['log_message']),
                AcceptMessageAction
            ]
            name = "iamthecheese"

        return AnotherTestFilter


    def test_basic_filter(self):
        class TestFilter(zmf.FirewallFilter):
            chain = [
                FilterTopicAction(['test_topic']),
                AcceptMessageAction
            ]

        eq_('test', TestFilter.name)


    def test_basic_filter_2(self):
        AnotherTestFilter = self.defineCheese()
        eq_('iamthecheese', AnotherTestFilter.name)


    def test_basic_filter_process(self):
        self.defineCheese()
        test_msg = Message("I am the cheese", "localhost", topic="log_message")
        bad_test_msg = Message("I am the ham", "localhost", topic="bad_topic")

        filt = get_filter('iamthecheese')
        assert_is_not_none(filt)

        out = filt(test_msg)
        eq_(test_msg, out)

        out = filt(bad_test_msg)
        eq_(None, out)


    @raises(AttributeError)
    def test_bad_filter_chain(self):
        class BadChainFilter(zmf.FirewallFilter):
            pass


    @raises(NameError)
    def test_duplicate_filter_name(self):
        self.defineCheese()
        class IAmTheCheeseFilter(zmf.FirewallFilter):
            chain = [AcceptMessageAction]


    @raises(TypeError)
    def test_filter_already_registered(self):
        self.defineCheese()
        self.defineCheese()


    @raises(KeyError)
    def test_filter_de_register(self):
        self.defineCheese()
        FilterMeta.deregister("iamthecheese")

        derp = get_filter("iamthecheese")


    def test_divert_filter(self):
        class DivertFilterTestFilter(zmf.FirewallFilter):
            chain = [DivertFilterCheeseAction]

        test_msg = Message("I am the cheese", "localhost", topic="log_message")
        out = DivertFilterTestFilter.handle(test_msg)
        eq_(str(out), 'Hello, I am the cheese')

        bad_test_msg = Message("I am the ham", "localhost", topic="bad_topic")
        out = DivertFilterTestFilter.handle(bad_test_msg)
        eq_(str(out), 'I am the ham')


    def test_interrupt_filter(self):
        class InterruptFilterTestFilter(zmf.FirewallFilter):
            chain = [InterruptFilterCheeseAction, AppendNotCheeseAction]

        test_msg = Message("I am the cheese", "localhost", topic="log_message")
        out = InterruptFilterTestFilter.handle(test_msg)
        eq_(str(out), 'Hello, I am the cheese')

        bad_test_msg = Message("I am the ham", "localhost", topic="bad_topic")
        out = InterruptFilterTestFilter.handle(bad_test_msg)
        eq_(str(out), 'I am the ham. I am not the cheese')
