import zmqfirewall.actions as za
from tests.helper import Message

from nose.tools import eq_, raises


@raises(za.DropMessageAction)
def test_default_filter_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')

    test_msg_topic = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='diff_topic')
    filt = za.FilterTopicAction(['test'])
    out = filt.action(test_msg)
    eq_(out, test_msg)

    filt.action(test_msg_topic)

@raises(za.DropMessageAction)
def test_callable_filter_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')
    test_msg_topic = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='diff_topic')
    filt = za.FilterTopicAction(['test'])
    out = filt(test_msg)
    eq_(out, test_msg)

    out = filt.action(test_msg_topic)


def test_filter_str_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')

    test_msg_topic = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='diff_topic')
    # TODO: Fix this shit test
    za.AcceptMessageAction.register()
    za.DropMessageAction.register()
    nfilt = za.FilterTopicAction(['test'],
                                 on_success='drop',
                                 on_failure='accept')

    try:
        nfilt.action(test_msg)
    except za.DropMessageAction:
        pass

    out = nfilt.action(test_msg_topic)
    eq_(out, test_msg_topic)


@raises(ValueError)
def test_filter_bad_action():
    filt = za.FilterTopicAction(['test'], on_failure=None)


@raises(ValueError)
def test_filter_bad_action_2():
    filt = za.FilterTopicAction(['test'], on_success=None)


def test_accept_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')

    out = za.AcceptMessageAction.action(test_msg)
    eq_(test_msg, out)


@raises(za.DropMessageAction)
def test_drop_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')
    za.DropMessageAction.action(test_msg)


def test_custom_action():
    test_msg = Message(
        body="I am the cheese",
        from_host="127.0.0.1",
        topic='test')
    class MangleTestAction(za.Action):
        def action(self, msg):
            msg.body = "Hello, " + msg.body
            return msg

    out = MangleTestAction.action(test_msg)
    eq_(str(out), "Hello, I am the cheese")
