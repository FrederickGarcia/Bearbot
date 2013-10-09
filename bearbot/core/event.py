'''
Created on Oct 2, 2013
@author: Garcia

This module will contain event/handler/listener logic.  It's a
spaghetti right now.

'''

from bearbot.sub_modules import chatter

from bearbot.core import command
from bearbot.core.command import Command

handlers = {} #Dictionary of server command/handlers

class Spaghetti_Handler(object):
    '''Determines what to do based off the message the bot receives '''

    def __init__(self, bot, msg):
        self.bot = bot

        # Sends each command to respective method
        if msg.command in handlers.keys():
            handlers[msg.command](self, msg)

    def user_message(self, msg):
        ''' Handles user messages (user/channel) '''
        if msg.content[0] == self.bot.cmd_prefix and \
           len(msg.content) > 1: #Checks if potential command
            cmd = Command(self.bot, msg); return #runs a command

        # Checks for a trigger word and replies with value
        if chatter.chatter_on:
            chatter.get_value(self.bot, msg.content, msg.source)

    def pong(self, ping_msg):
        ''' Handles PING's '''
        self.bot.send('PONG %s' % ping_msg.params)

# Dictionary of server commands to their associated handling methods
handlers.update({'PRIVMSG': Spaghetti_Handler.user_message,
                 'PING': Spaghetti_Handler.pong})

class Event:
    ''' Registers/Unregisters handlers to events '''

    def __init__(self):
        self.handlers = set()

    def register(self, handler):
        self.handlers.add(handler)
        return self

    def unregister(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError('Handler %s not registered to event' % handler)
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def handler_count(self):
        return len(self.handlers)

    __iadd__ = register #Event += handler registers handler to event
    __isub__ = unregister #Event -= handler unregisters handler from event
    __call__ = fire #
    __len__  = handler_count #This may come in handy later

class Who_Event:
    ''' Who Commands '''

    def __init__(self):
        self.who_event = Event()

    def handle(self):
        who = 'who object...'
        self.who_event(who)
        print(who)

def log(who):
    print('Who one: %s' % who)

def log2(who):
    print('Who two: %s' % who)


class Response_Waiter(object):
    ''' Waits for a requested message response '''
    
    def __init__(self, **kwargs):
        # Do things here to start a new thread and wait
        # Register it to an event
        pass

def main():
    ''' Test stub '''
    cmdhandler = Who_Event()
    cmdhandler.new_cmd += log2
    cmdhandler.new_cmd += log
    cmdhandler.new_cmd -= log2
    cmdhandler.new_cmd += log2
    cmdhandler.handle()
    
if __name__ == '__main__':
    main()