'''
Created on Sep 18, 2013
@author: Garcia

This module is for user commands.  User commands are commands received
by the bot from irc users in PRIVMSG's.  The Command class creates a
user command object and runs the user commands' associated functions
passing the user command object to them.  Functions for user commands
can be defined in different modules.  This module provides ease for
defining command functions, or other structures, that trigger when the
bot receives a user command.

For examples and a robust description of how to use this module, see
the misc_commands module.

'''

# Dictionary of commands and associated functions
# Updated from modules containing command definitions
command_dic = {}

class Command(object):
    ''' Creates PRIVMSG command objects from user commands.
    
    All user commands have a prefix, root, and arguments.
    Subsequential arguments are separated by spaces.  This class
    creates an object for each command with root (string) and arguments
    (list) attributes.  It then runs the associated command function
    depending on its root.

    Command: <prefix> <root> <args>
    Example: <.>      <quit> <['Bye','everyone!']>
    Raw:     <Garcia> .quit Bye everyone!
             * Bearbot has quit (Quit: Bye everyone!)

    This class is also a proxy class to the Bot class to make command
    definitions simpler.  However, using proxy methods in command
    function definitions reduces performance slightly.  It's only for
    ease of use. Also, be careful when using proxy attributes.  They
    are shallow copies and will not change the Bot attributes.
    '''

    def __init__(self, bot, msg):
        self.bot, self.msg = bot, msg
        self.content = msg.content[1:].split()
        self.root, self.args = self.content[0], None
        if len(self.content) > 1:
            self.args = self.content[1:]
        command_dic[self.root](self)  # Runs command
    
    def __getattr__(self, attr):
        ''' Makes class a proxy class to Bot '''
        return getattr(self.bot, attr)
    
    # Overriden Methods
    
    def notify(self, message):
        ''' Sends NOTICE response to user command '''
        self.bot.notify(self.msg.nick, message)
    
    # Accessors
    
    @property
    def cmd_prefix(self):
        return self.bot.cmd_prefix

    # Mutators

    @cmd_prefix.setter
    def cmd_prefix(self, prefix):
        self.bot.cmd_prefix = prefix
    
    # Command methods

    def reply(self, message):
        ''' Replies to user command source with message '''
        self.bot.say(self.msg.source, message)