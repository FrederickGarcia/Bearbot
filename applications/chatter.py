'''
Created on Sep 18, 2013
@author: Garcia

This module is for useless chatter

It updates the file, /bearbot/resources/chatterbox.bb.  It provides
functions to load the file, add entries, and remove entries.  It
contains an is_trigger() function that returns respective boolean
values. /bearbot/resources/chatterbox.bb - has key:value on each line to
represent trigger:response.

'''

import re

from bearbot.core.command import *

chat_dic = {}  # Chatter dictionary
chatter_on = False  # Toggles chatter responses off and on
chat_file = '../../resources/chatterbox.bb'  # Trigger:Response data file
bold = '\u0002'

def load_chatter():
    ''' Loads chatter triggers and responses from file '''
    with open(chat_file, 'r') as cf:
        chat_dic.update(line[:-1].split(':') for line in cf)

def add_entry(key, value):
    ''' Appends chatter entry to chatterbox.bb '''
    chat_dic[key] = value  # Adds trigger/response to current dictionary
    with open(chat_file, 'a') as cf:  # Opens file to append to
        cf.write('%s:%s\n' % (key, value))  # Writes trigger/response

def entry_exists(key):
    ''' Checks if entry exists in the chatter dictionary '''
    if key in chat_dic:
        return True
    return False

def remove_entry(key):
    ''' Removes chatter entry by key '''
    chat_dic.pop(key)
    with open(chat_file, 'w') as cf:
        for entry in chat_dic:
            cf.write('%s:%s\n' % (entry, chat_dic[entry]))

def get_value(bot, content, source):
    ''' Returns response for trigger (False if not trigger) '''
    for key in chat_dic:
        if str.lower(content) == str.lower(key):
            bot.say(source, chat_dic[key])

# Command Definitions

@one_arg
def chatter_(cmd):
    ''' chatter [on]/[off] - Toggles chatter on and off '''
    global chatter_on
    
    if 'on' in cmd.args:
        if chatter_on is True:
            cmd.reply('Chatter is already turned on.')
        else:
            chatter_on = True
            cmd.reply('Chatter turned on.')
    if 'off' in cmd.args:
        if chatter_on is False:
            cmd.reply('Chatter is already turned off.')
        else:
            chatter_on = False
            cmd.reply('Chatter turned off.')
    if 'list' in cmd.args:
        triggers = []
        for key in chat_dic:
            triggers.append(key)
            
        cmd.reply('Chatter triggers: %s' % (' |  ').join(triggers))
         
# Needs $nick variable feature or regexp
@requires_args
def set_(cmd):
    ''' Adds chatter entries (.set $1 = $2) '''
    if not re.search(r'\w+ = \w+', (' ').join(cmd.args)):  # Checks syntax
        cmd.reply('Improper syntax for set command.\nRequires %sset [string]'\
                  ' = [string]' % cmd.bot.cmd_prefix); return
    key, value = (' ').join(cmd.args).split(' = ')  # Splits key/value
    if not entry_exists(key):
        add_entry(key, value)
        cmd.reply('Response, %s%s%s, added for the trigger, %s%s%s.' %
                  (bold, value, bold, bold, key, bold)); return
    cmd.reply('A value for "%s" already exists.' % key)

@requires_args
def del_(cmd):
    ''' Deletes chatter entries (ie. .del <key>) '''
    key = (' ').join(cmd.args)
    if entry_exists(key):
        remove_entry(key)
        cmd.reply('"%s" entry removed from dictionary.' % (key)); return
    cmd.reply('An entry for "%s" does not exist.' % (key))

# Command dictionary
command_dic.update({'chatter': chatter_, 'set': set_, 'del': del_})
load_chatter()