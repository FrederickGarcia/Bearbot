'''
Created on Oct 2, 2013
@author: Garcia

This module will contain event/handler/listener logic.  It's a
spaghetti right now.

'''

import threading
from time import sleep

from bearbot.core import command
from bearbot.core.command import Command

# The chatter import could be eliminated with the proper event system
from applications import chatter

handlers = {} #Dictionary of server command/handlers

# For later
# t = threading.Thread(target=handler, args=args, kwargs=kwargs)
# t.start()

class SpaghettiHandler(object):
    '''Determines what to do based off the message the bot receives '''

    def __init__(self, bot, msg):
        self.bot = bot

        # Sends each command to respective method
        if msg.command in handlers.keys():
            handlers[msg.command](self, msg)

    def user_message(self, msg):
        ''' Handles user messages (user/channel) '''
        if msg.content[0] == self.bot.cmd_prefix and len(msg.content) > 1:
            try:
                cmd = Command(self.bot, msg)
                command.command_dic[cmd.root](cmd)  # Runs command
            except Exception as e:
                self.bot.log('Command exception: %s' % e)

        # Checks for a trigger word and replies with value
        if chatter.chatter_on:
            chatter.get_value(self.bot, msg.content, msg.source)

    def pong(self, ping_msg):
        ''' Handles PING's '''
        self.bot.send('PONG %s' % ping_msg.params)

# Dictionary of server commands to their associated handling methods
handlers.update({'PRIVMSG': SpaghettiHandler.user_message,
                 'PING': SpaghettiHandler.pong})

def main():
    ''' Test stub '''
    
if __name__ == '__main__':
    main()