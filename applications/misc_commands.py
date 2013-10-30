'''
Created on Sep 24, 2013
@author: Garcia

This module houses some miscellaneous commands

It serves as an example of how to add custom commands to your bot in
other modules.

A good design practice is to create a module that does something and
define the related command function at the end of the module.
Following that design practice keeps command definitions near their
implementation to make it easier to debug.

-=-=-=-=-=-=-=-=-=  Defining your own user commands -=-=-=-=-=-=-=-=-=-

To add a command definition in your module:

    1. Add 'from bearbot.core.command import *' to the top of your
       module

    2. Define your command with a parameter to accept a Command object:

           ex. def my_function(cmd):
                   ...do stuff with cmd
                   ...use your module or bearbot.core

    3. Update the command_dic dictionary. Each key must be a string of
       what you want to trigger your function after the prefix (ie.
       'quit') and the key's value must be a reference to your
       function's object - the name of your function without ()'s.

           ex. command_dic.update({'quit': my_quit_function})

       * Ensure the dictionary is updated after the function
         definitions.  Otherwise, the interpreter won't recognize them.

The Command object passed to your definition provides:

          - Methods such as reply(source, message).  The Command Class
            documentation to know what other methods are available.

    .root - The root of the user command as a string stripped of the
            prefix (ex. 'quit').

    .args - A list of arguments (ex. ['bye', 'everybody']).  The value
            of arguments is None if there aren't any.  There are
            decorators @no_args and @require args covered later.

          - Use (' ').join(args) if you need them as a string, or use
            the @string decorator.
            
          - If a command requires a certain access level to use
            admin.get_access(nick), or use @no_access, @admin, etc.
            decorators covered later.

                ex. if admin.get_access(cmd.msg.nick) >= 5000:..

    .bot - The Bot object that received the user command.  This
           attribute provides useful Bot methods.  See the Bot class
           for documentation and methods you can use with it.

         - Note that a Command object is a proxy class of the Bot
           class, so Bot object attributes can be referenced through a
           Command object.

               Example: cmd.notice(cmd.msg.nick, 'Oh hi!') instead of..
                        cmd.bot.notice(cmd.msg.nick, 'Oh hi!')

         - WARNING: Using proxy methods in command function definitions
                    reduces performance slightly.  It's only for ease
                    of use.  Also, be careful when using proxy
                    attributes.  They are shallow copies and will not
                    change Bot attributes.

    .msg - The Message object the user command came from.  This
           attribute provides you with a means to retrieve message
           information the command derived from such as the source,
           nick, host and more.  Read the Message class documentation
           for more attributes of a Message object.

Decorators are also available to your command definitions:

    There're decorators that your command definition can use.  These
    decorators assist in typical command definition operations.  For
    example, the @no_args decorator says that your command definition
    does not require any args.  So accordingly, the @no_args decorator
    skips the function and replies with an error message to the user
    that issued the command.  For a list of decorators, read the
    command module's documentation.
    
Docstring use:

    Your docstring will be available in the help commands to display
    proper syntax and the description of the command.

Below are some examples of defining your own user commands.

Note at the bottom of the module, there's a dictionary of all the roots
and function objects, and then the command_dic is updated with that
dictionary.

'''

import re
import random
from codecs import getencoder

from bearbot.core.command import *

@one_arg
def who(cmd):
    ''' who [nick] - Returns who information '''
    who_list = cmd.bot.who(cmd.args[0])
    for who in who_list:
        cmd.reply(who)

@as_string
def action(cmd):
    ''' action [message] - Performs irc action "/me *" '''
    cmd.action(cmd.msg.source, '%s' % cmd.args)

@requires_args
def say(cmd):
    ''' say [user|#channel] [message] '''
    if cmd.args[1] == '/me':
        cmd.action(cmd.args[0], (' ').join(cmd.args[2:]))
    else:
        cmd.say(cmd.args[0], (' ').join(cmd.args[1:]))

@owner
def quit_(cmd):
    ''' quit - Disconnects bot from the server '''
    if cmd.args != None:
        quit_message = (' ').join(cmd.args)
    else:
        quit_message = 'Okay, bye'  # Default quit message
    cmd.bot.quit(quit_message)
    cmd.bot.alive = False  # Kills bot
    cmd.bot.close_connection()
    cmd.bot.log('End of session.')
    #Bear in mind, quit messages only show after being
    #connected to the server for a few minutes (spam protection)

@owner
def delay(cmd):
    ''' delay *[seconds] - Sets message delay time in seconds '''
    if not cmd.args:
        cmd.reply('The current delay is set to %s seconds' %
                  cmd.bot.msg_delay)
        return
    if len(cmd.args) > 2:
        cmd.reply('Too many arguments. Requires: %sdelay [int|float]' %
                  cmd.cmd_prefix)
        return
    try:
        if not 0 <= float(cmd.args[0]) <= 10:
            cmd.reply('Delay must be from 0 - 10 seconds.')
            return
        cmd.bot.set_msg_delay(float(cmd.args[0]))
        cmd.reply('Message delay set to %s seconds.' % float(cmd.args[0]))
    except:
        cmd.reply('Invalid input. Requires: %sdelay [int|float]' %
                  cmd.cmd_prefix)

@owner
@requires_args
def prefix(cmd):
    ''' prefix [char] - Changes the command prefix '''
    if len(cmd.args) > 1 or len(cmd.args[0]) != 1:
        cmd.reply('Improper syntax, Requires: %sprefix [char]' % 
                  cmd.cmd_prefix)
    else:
        cmd.cmd_prefix = cmd.args[0]
        cmd.reply("Command prefix set to: %s" % cmd.args[0])

@owner
@requires_args
def join(cmd):
    ''' join [#channel(s)] - Bot joins channels specified '''
    print('Misc commands: before receiving error list')
    errors = cmd.bot.join(cmd.args)
    print('Misc commands: after receiving error list %s' % errors)
    if errors is not None:
        for e in errors:
            cmd.reply('Error: %s' % e.params)

@owner
def part(cmd):
    ''' part [#channel(s)] - Bot parts a channel. '''
    if cmd.args is None and re.search(r'^#', cmd.msg.source): 
        cmd.bot.part(cmd.msg.source); return  # Parts current channel
    cmd.bot.part(cmd.args)  # Parts the list of channels

@no_args
def bots(cmd):
    ''' Reports itself as a bot '''
    cmd.reply('Reporting in.')

def help_(cmd):
    ''' help *[command] - Lists commands, their syntax, and descriptions. '''
    if not cmd.args:
        cmd.notice('Type %shelp [command] for the syntax and description of'\
                   ' a command' % cmd.bot.cmd_prefix)
        cmd.notice(cmd.cmd_prefix +
                   (' %s' % cmd.cmd_prefix).join(command_dic.keys()))
        return
    if len(cmd.args) > 1:
        cmd.notice('The %s help command takes only one argument')
        return
    if cmd.args[0] in command_dic.keys():
        cmd.notice('%s%s: %s' % (cmd.bot.cmd_prefix, cmd.args[0],
                                 command_dic[cmd.args[0]].__doc__))
        return
    cmd.notice('%s is not a command' % cmd.args[0])

#######################################################################
#                                                                     #
#                     Fun / Useless Commands                          #
#                                                                     #
#######################################################################

@no_args
def hbd(cmd):
    ''' A test user command definition '''
    cmd.reply("Happy bear day, %s!" % cmd.msg.nick)

@as_string
def rot_13(cmd):
    ''' rot13 [message] - encodes (decodes) rot13 '''
    encoder = getencoder('rot-13')
    cmd.reply(encoder(cmd.args)[0])

@as_string
def reverse(cmd):
    ''' reverse [string] - Replies with string reversed '''
    cmd.reply(cmd.args[::-1])

@one_arg
def rps(cmd):
    ''' Play rock, paper, scissors, BEAR! with the bot. '''
    if str.lower(cmd.args[0]) == 'bear':
        cmd.action(cmd.msg.source, 'runs away..')
        return
    options = ['rock', 'paper', 'scissors']
    if cmd.args[0] not in options:
        cmd.reply("That is not a valid choice. I'm not playing with you "\
                  'anymore.')
        return
    move = random.choice(options)
    cmd.reply('Rock... Paper... ')
    if move == cmd.args[0]:
        cmd.reply('BEARRRRR!!!!!!!!!!')
        cmd.action(cmd.msg.source, 'wins because bear eats %s and %s.' %
                  (cmd.args[0], cmd.msg.nick))
        return
    cmd.reply('Scissors...')
    cmd.action(cmd.msg.source, 'forms %s with his hand.' % move)
    if move == 'scissors' and cmd.args[0] == 'rock' or\
            move == 'rock' and cmd.args[0] == 'paper' or\
            move == 'paper' and cmd.args[0] == 'scissors':
        cmd.reply('Congratulations, %s, you win this time! %s beats %s :)' % 
                  (cmd.msg.nick, cmd.args[0], move))
        return
    cmd.reply('Sorry, %s, you lost this time. %s beats %s :(' % 
              (cmd.msg.nick, move, cmd.args[0]))
    return

# Dictionary of commands and their respective function references
misc_commands = {'hbd': hbd, 'quit': quit_, 'join': join, 'part': part,
                 'delay': delay, 'prefix': prefix, 'who': who,
                 'action': action, 'reverse': reverse, 'bots': bots,
                 'help': help_, 'say': say, 'rot13': rot_13, 'rps': rps}

command_dic.update(misc_commands)  # Updates the master command dictionary