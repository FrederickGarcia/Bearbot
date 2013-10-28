<<<<<<< HEAD
''' Takes PRIVMSG and calls modules
Created on 29/10/2013

@author: Evan
'''
from bearbot.core.command import *
from bearbot.sub_modules.ctcp_commands import *

def privmsg_(handler, msg):
    ''' Handles user messages (user/channel) '''
    if msg.content[0] == handler.bot.cmd_prefix and len(msg.content) > 1:
        try:
            cmd = Command(handler.bot, msg)
            command_dic[cmd.root](cmd)  # Runs command
        except Exception as e:
=======
''' Takes PRIVMSG and calls modules
Created on 29/10/2013

@author: Evan
'''
from bearbot.core.command import *
from bearbot.sub_modules.ctcp_commands import *

def privmsg_(handler, msg):
    ''' Handles user messages (user/channel) '''
    if msg.content[0] == handler.bot.cmd_prefix and len(msg.content) > 1:
        try:
            cmd = Command(handler.bot, msg)
            command_dic[cmd.root](cmd)  # Runs command
        except Exception as e:
>>>>>>> 3b02f0b451bd251f3a499a7b6950f482b62d8266
            handler.bot.log('Command exception: %s' % e)