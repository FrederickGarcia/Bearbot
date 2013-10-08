'''
Created on Sep 18, 2013
@author: Garcia

This module is for useless chatter. It updates a the file, /bearbot/resources/chatterbox.bb.
It provides functions to load the file, add entries, and remove entries.
It contains an is_trigger() function that returns respective boolean values.

/bearbot/resources/chatterbox.bb - has key:value on each line to represent trigger:response
'''

#Built-in
import re

#Core
from bearbot.core import command

chatter_dic = {} #chatter dictionary
chatter_on = False #Toggles chatter responses off and on
chatter_file = '../../resources/chatterbox.bb' #Trigger:Response data file
bold = '\u0002'

#Loads chatter triggers and responses from file
def load_chatter():  
    with open(chatter_file, 'r') as chatterbox: #Read file
        for line in chatterbox:
            phrases = line.strip('\n').split(':') #creates a tuple (key, value)
            #sets first phrase as key and second phrase as value
            chatter_dic[phrases[0]] = phrases[1] 

#Appends chatter entry to chatterbox.bb
def add_entry(key, value):
    if key in chatter_dic: #Checks for duplicate key entry
        return False     
    chatter_dic[key] = value #Adds trigger/response to current dictionary
    with open(chatter_file, 'a') as chatterbox: #opens file to append to
        chatterbox.write('%s:%s\n' % (key, value)) #Writes trigger/response to file
    return True

#Removes chatter entry by key
def remove_entry(key):
    if key not in chatter_dic: #Checks if requested key exists
        return False
    chatter_dic.pop(key) #Removes trigger/response from dictionary
    with open(chatter_file, 'w') as chatterbox: #Write file
        for trigger in chatter_dic:
            #Overwrites file using dictionary
            chatterbox.write('%s:%s\n' % (trigger, chatter_dic[trigger]))
            return True

#Returns response for trigger (False if not trigger)
def get_value(bot, content, source):
    if content in chatter_dic:
        bot.say(source, chatter_dic[content]) #Returns a response

'''
Command Definitions
'''

#/chatter [on]/[off] - Toggles chatter on and off
def bchatter(cmd):
    global chatter_on
    
    if 'on' in cmd.args:
        if chatter_on == True:
            cmd.reply('Chatter is already turned on.')
        else:
            chatter_on = True
            cmd.reply('Chatter turned on.')
        
    if 'off' in cmd.args:
        if chatter_on == False:
            cmd.reply('Chatter is already turned off.')
        else:
            chatter_on = False
            cmd.reply('Chatter turned off.')
            
    if 'list' in cmd.args:
        chatter_list = []
        for key in chatter_dic:
            chatter_list.append(key)
            
        cmd.reply('Chatter triggers: %s' % (', ').join(chatter_list))
         
#/set - adds chatter entries (ie /set $1 = $2) ***** needs $nick variable feature
def bset(cmd):
    if not re.search(r'\w+ = \w+', (' ').join(cmd.args)): #Checks syntax
        cmd.reply('Improper syntax for /set command.\r\n \
                        Requires /set [string] = [string]')
    else:
        key, value = (' ').join(cmd.args).split(' = ') #Splits key/value
                        
        if add_entry(key, value): #Checks if entry exists already
            add_entry(key, value) #Adds chatter entry
            cmd.reply('Response, %s%s%s, added for the trigger, %s%s%s.' %
                     (bold, value, bold, bold, key, bold))
        else:
            cmd.reply('A value for "%s" already exists.' % key)

#/del - deletes chatter entries (ie. /del <key>)
def delete(cmd):       
    if cmd.args != None:
        key = (' ').join(cmd.args)
        if remove_entry(key): #Checks if entry key exists
            remove_entry(key) #Removes key/value entry
            cmd.reply('"%s" entry removed from dictionary.' % (key))
        else:
            cmd.reply('An entry for "%s" does not exist.' % (key))
            
chatter_commands = {'chatter': bchatter, 'set': bset, 'del': delete}
command.command_dic.update(chatter_commands)
load_chatter()