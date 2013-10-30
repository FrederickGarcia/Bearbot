'''
Created on Oct 2, 2013
@author: Garcia, Evan

This module will contain event/handler/listener logic.  It's a
spaghetti right now.

'''

import threading

from bearbot.core import command
from bearbot.core.command import Command

#TODO
# The applications import will be eliminated with a proper loading system
from applications import chatter, misc_commands
from bearbot.sub_modules import irc_commands, bot_commands, ctcp_commands

#Dictionary of server command/command_handlers
#TODO create methods to manage adding to this, similar to the command manager
command_handlers = {'PRIVMSG': [bot_commands.privmsg_, ctcp_commands.ctcp_],
                    'PING': [irc_commands.ping_]}

# TODO For later
# t = threading.Thread(target=handler, args=args, kwargs=kwargs)
# t.start()

class SpaghettiHandler(object):
    '''Determines what to do based off the message the bot receives '''

    def __init__(self, bot, msg):
        self.bot = bot

        # Sends each command to respective method
        if msg.command in command_handlers:
            for handler in command_handlers[msg.command]:
                handler(self, msg)