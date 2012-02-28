zmqfirewall - ZeroMQ Firewall
=============================

A simple, extensible object-based firewall for applications that use ZeroMQ.


Creating an Action Handler
--------------------------

Defining a custom action handler is simple to do esspecially if you need to
mangle messages. Each Action class has a callable function named action that 
accepts a message and returns the same message after alterations have been
made. An Action that does not return anything 'drops' the message.

### Action that appends 'Hello' to every message processed
    from zmqfirewall.actions import Action

    class HelloAction(Action):
        def action(self, message):
            message.body = "Hello %s" % message
            return message

### Action that drops messages that don't have the word 'important' in them
    from zmqfirewall.actions import Action

    class ImportantOnlyAction(Action):
        def action(self, message):
            if 'important' in str(message).lower().split(' '):
                return message

### Action that redirects any message that comes in to the topic 'hijacked'
    from zmqfirewall.actions import Action

    class HijackMessageAction(Action):
        def action(self, message):
            message.topic = 'hijacked'
            return message

### Log splitting example
    from zmqfirewall.actions import Action, DropMessageAction

    class InfoLogMessageAction(Action):
        def action(self, message):
            # Move message to the 'log.informational' queue
            message.topic = "log.informational"
            return message

    class ImportantLogMessageAction(Action):
        def action(self, message):
            # Move message to the 'log.important' queue
            message.topic = "log.important" 
            return message

    class LoggingRedirectAction(Action):
        def action(self, message):
            tag = str(message).lower().split(' ')[0]

            if tag in ['error', 'critical', 'fatal']:
                return ImportantLogMessageAction
            elif tag in ['info', 'debug']:
                return InfoLogMessageAction
            else:
                # Drop the message
                return DropMessageAction

Creating Rules
--------------

### Basic Message Acceptance Rule
    from zmqfirewall.rules import Rule

    # This is a really stupid example, btw
    class AcceptAllMessagesRule(Rule):
        filter_chain = []


### Only pass messages from the 'log.important' topic
    from zmqfirewall.actions import FilterTopicAction
    from zmqfirewall.rules import Rule

    class AcceptImportantMessagesRule(Rule):
        filter_chain = [
            FilterTopicAction(['log.important'])
        ]

### Mangle all messages from the topic 'log' and prepend date/time
    from zmqfirewall.actions import Action
    from zmqfirewall.rules import Rule
    from datetime import datetime

    class PrependDatetimeRule(Rule):
        filter_chain = [
            FilterTopicAction(['log'], on_failure='accept'),
            Action(
                action = lambda m: m.set_body('[%s] %s' % (datetime.now(), m))
            )
        ]
