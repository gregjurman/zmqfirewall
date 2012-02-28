from zmqfirewall.filters import FirewallFilter
from zmqfirewall.actions import FilterTopicAction, Action
from zmqfirewall.exceptions import InterruptAction
from zmqfirewall.utils import interrupt, divert

from tests.helper import Message
from hashlib import md5

from nose.tools import eq_

class MarkAsBadAction(Action):
    no_register = True
    def action(self, msg):
        msg.body = "[BAD MESSAGE] %s" % msg.body
        msg.topic = "bad_message"
        return msg

class AppendMD5Action(Action):
    no_register = True
    def action(self, msg):
        msg.body = "%s [%s]" % (msg.body, md5(msg.body).hexdigest())
        return msg

class MarkAsImportantLogMessage(Action):
    no_register = True
    def action(self, msg):
        msg.body = "[IMPORTANT] %s" % msg.body
        return msg

class ImportantMessageAction(Action):
    no_register = True
    def action(self, msg):
        if 'important' in msg.body.lower().split(' '):
            divert(MarkAsImportantLogMessage)
        else:
            return msg

class InterruptMarkAsBad(Action):
    no_register = True
    def action(self, msg):
        interrupt(MarkAsBadAction)

class FunctionalFilterTestFilter(FirewallFilter):
    chain = [
        FilterTopicAction(
            ['log_message'],
            on_failure=InterruptMarkAsBad
        ),
        ImportantMessageAction,
        AppendMD5Action,
    ]

def bad_message_test():
    msg = Message(body="i am a bad message", topic="not_log", from_host="localhost")
    out = FunctionalFilterTestFilter.handle(msg)
    eq_(str(out), "[BAD MESSAGE] i am a bad message")

    msg = Message(body="i am an important log!", topic="log_message", from_host="localhost")
    out = FunctionalFilterTestFilter.handle(msg)
    eq_(str(out), "[IMPORTANT] i am an important log! [04f6255dd0c703fc555e7605e3e1df73]")

    msg = Message(body="i am a regular log!", topic="log_message", from_host="localhost")
    out = FunctionalFilterTestFilter.handle(msg)
    eq_(str(out), "i am a regular log! [129d357ed288b7c6bf119e76033689a1]")
