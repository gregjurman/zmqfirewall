import zmqfirewall.actions as za
from tests.helper import Message

from nose.tools import eq_

test_msg = Message(
    message="I am the cheese",
    from_host="127.0.0.1", 
    topic='test')

test_msg_topic = Message(
    message="I am the cheese",
    from_host="127.0.0.1",
    topic='diff_topic')


def test_default_filter_action():
    filt = za.FilterTopicAction(['test'])
    
    out = filt.action(test_msg)
    eq_(out, test_msg)

    out = filt.action(test_msg_topic)
    eq_(out, None)

def test_callable_filter_action():
    filt = za.FilterTopicAction(['test'])
    
    out = filt(test_msg)
    eq_(out, test_msg)

    out = filt.action(test_msg_topic)
    eq_(out, None)

def test_filter_str_action():
    nfilt = za.FilterTopicAction(['test'], on_success='drop', on_failure='accept')

    out = nfilt.action(test_msg)
    eq_(out, None)

    out = nfilt.action(test_msg_topic)
    eq_(out, test_msg_topic)


def test_filter_bad_action():
    try:
        filt = za.FilterTopicAction(['test'], on_failure=None)
    except ValueError as e:
        eq_(str(e), 'on_failure must be a string or Action, got None')

    try:
        filt = za.FilterTopicAction(['test'], on_success=None)
    except ValueError as e:
        eq_(str(e), 'on_success must be a string or Action, got None')

def test_accept_action():
    out = za.AcceptMessageAction.action(test_msg)

    eq_(test_msg, out)


def test_drop_action():
    out = za.DropMessageAction.action(test_msg)

    eq_(out, None)


def test_custom_action():
    class MangleTestAction(za.Action):
        def action(self, msg):
            msg.message = "Hello, " + msg.message
            return msg

    out = MangleTestAction.action(test_msg)
    eq_(str(out), "Hello, I am the cheese")
