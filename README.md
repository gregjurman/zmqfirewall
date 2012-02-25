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
            return "Hello %s" % message

### Action that drops messages that doesn't have the word 'important' in them
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
