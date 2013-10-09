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

from bearbot.core import command

chatter_dic = {}  # Chatter dictionary
chatter_on = False  # Toggles chatter responses off and on
chatter_file = '../../resources/chatterbox.bb'  # Trigger:Response data file
bold = '\u0002'

def load_chatter():
    ''' Loads chatter triggers and responses from file '''
    with open(chatter_file, 'r') as chatterbox:
        for line in chatterbox:
            phrases = line.strip('\n').split(':')  # Creates a tuple
            # Sets first phrase as key and second phrase as value
            chatter_dic[phrases[0]] = phrases[1]

def add_entry(key, value):
    ''' Appends chatter entry to chatterbox.bb '''
    if key in chatter_dic:  # Checks for duplicate key entry
        return False     
    chatter_dic[key] = value  # Adds trigger/response to current dictionary
    with open(chatter_file, 'a') as chatterbox:  # Opens file to append to
        chatterbox.write('%s:%s\n' % (key, value))  # Writes trigger/response
    return True

def remove_entry(key):
    ''' Removes chatter entry by key '''
    if key not in chatter_dic:  # Checks if requested key exists
        return False
    chatter_dic.pop(key)  # Removes trigger/response from dictionary
    with open(chatter_file, 'w') as chatterbox:
        for trigger in chatter_dic:
            # Overwrites file using dictionary
            chatterbox.write('%s:%s\n' % (trigger, chatter_dic[trigger]))
            return True

def get_value(bot, content, source):
    ''' Returns response for trigger (False if not trigger) '''
    if content in chatter_dic:
        bot.say(source, chatter_dic[content])

''' Command Definitions '''

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
        chatter_list = []
        for key in chatter_dic:
            chatter_list.append(key)
            
        cmd.reply('Chatter triggers: %s' % (', ').join(chatter_list))
         
# Needs $nick variable feature
def set_(cmd):
    ''' Adds chatter entries (ie .set $1 = $2) '''
    if not re.search(r'\w+ = \w+', (' ').join(cmd.args)):  # Checks syntax
        cmd.reply('Improper syntax for /set command.\r\nRequires /set'\
                  '[string] = [string]')
    else:
        key, value = (' ').join(cmd.args).split(' = ')  # Splits key/value
        # Checks if entry exists already and adds item entry
        if add_entry(key, value):
            add_entry(key, value)
            cmd.reply('Response, %s%s%s, added for the trigger, %s%s%s.' %
                     (bold, value, bold, bold, key, bold))
        else:
            cmd.reply('A value for "%s" already exists.' % key)

def del_(cmd):  
    ''' Deletes chatter entries (ie. .del <key>) '''
    if not cmd.args is None:
        key = (' ').join(cmd.args)
        # Checks if entry key exists and removes item entry
        if remove_entry(key):
            remove_entry(key)
            cmd.reply('"%s" entry removed from dictionary.' % (key))
        else:
            cmd.reply('An entry for "%s" does not exist.' % (key))

# Command dictionary
chatter_commands = {'chatter': chatter_, 'set': set_, 'del': del_}
command.command_dic.update(chatter_commands)
load_chatter()