'''
Created on Sep 18, 2013
@author: Garcia

Handles messages in unicode format from an irc server based on RFC 2812.

Irc messages are separated by \r\n. A message contains: *<prefix>
<command> <parameters> separated by spaces.  The optional prefix is the
message's origin address.  Examples of commands are PRIVMSG and PING.
Parameters are unique to a command, however some follow similar
structure.

This module provides a class to create message objects that structures
a message into its respective attributes.

'''

import re

server_commands = {}  # Dictionary of server commands/setup methods

class Message(object):
    ''' Structures irc messages from into useful objects
    
    An object of this class has attributes dependent on its command,
    so be careful to know what command the message has before calling
    its attribute.

    '''

    def __init__(self, raw_msg):
        self.raw_msg = raw_msg.strip('\r\n')  # Raw message from host
        self.set_parts(self.raw_msg)  # Creates prefix, command, and params
        self.set_params()  # Sets attributes according to command type

    def set_parts(self, raw_msg):
        ''' Organizes message into three main parts and subparts '''
        if not raw_msg[0] == ':':  # Prefix, command, and params
            self.prefix = None
            self.command, self.params = raw_msg.split(' ', 1); return
        self.prefix, self.command, self.params = raw_msg.split(' ', 2)
        self.prefix = self.prefix[1:]  # Removes prefix ':'
        if re.search(r'^\w+!', self.prefix):  # Checks for nick!user@host
            self.nick, self.uhost = self.prefix.split('!')  # Sets nick, uhost
            self.user, self.host = self.uhost.split('@')  # Sets user, host

    def set_params(self):
        ''' Returns parameters depending on command type '''
        if self.command in server_commands.keys(): 
            # Runs method depending on command
            server_commands[self.command](self)

    def __str__(self):
        ''' Outputs attributes in human-readable format '''
        if hasattr(self, 'to_string'):
            return self.to_string
        if hasattr(self, 'prefix'):
            return ('%s %s %s' % (self.prefix, self.command, self.params))
        return ('%s %s' % (self.command, self.params))


''' Parameter setup functions

All messages have parameters. Parameters are unique to the command.
These functions serve to set the appropriate attributes depending on
the command.  The Message class passes itself to the appropriate
function and the function sets its attributes according to the type of
command.

These functions are left outside of the class for performance.  There
will eventually be too many for the program to build references to
every time a Message object is created, which can be hundreds to
thousands per second.  The set_params() method uses the server_commands
dictionary to point the object to these functions depending on its
command type. To manage its parameters, use its msg.

'''

def privmsg(pm):
    ''' Sets PRIVMSG attributes '''
    pm.source, pm.content = pm.params.split(':', 1)  # Sets source, content
    pm.source = pm.source.strip()  # Removes trailing ' '
    if hasattr(pm, 'nick'):  # Sets string for str(msg)
        pm.to_string = ('%s %s@%s %s <%s|%s> %s' % (pm.nick, pm.user, pm.host,
                                                    pm.command, pm.nick,
                                                    pm.source, pm.content))
        return
    pm.to_string = ('%s %s <%s> %s' % (pm.prefix, pm.command, pm.source,
                                       pm.content))

def ping(ping_msg):
    ''' Sets PING attributes '''
    ping_msg.params = ping_msg.params[1:]  # Removes the ':'
    ping_msg.to_string = ('PING %s' % ping_msg.params)

''' Command Response Messages

Just like above, these functions serve to set attributes unique to the
type of command a message has.  These are server replies that have
three digit control codes as commands.  In the range 200-399 are server
responses to commands given to them.

'''

def who_reply(who):
    ''' (352 - RPL_WHOREPLY) sets attributes for WHO command replies '''
    param_parts = who.params.split(None, 8)
    hopcount = param_parts[7]
    hopcount = hopcount[1:] #Removes ':'
    who.who_reply = {'channel': param_parts[1],  # Channel
                     'user': param_parts[2],  # Username
                     'host': param_parts[3],  # Host
                     'server': param_parts[4],  # Server
                     'nick': param_parts[5],  # Nickname
                     'flags': param_parts[6],  # Flags
                     'hopcount': hopcount,  # Hop Count
                     'realname': param_parts[8]}  # Realname

def end_of_who(end_msg):
    ''' (315 - RPL_ENDOFWHO) sets attributes for ENDOFWHO messages '''
    param_parts, end_msg.content = end_msg.params.split(':')
    end_msg.name = param_parts.split()[1]

# Dictionary of server commands to their respective setup methods
server_commands = {'PRIVMSG': privmsg, 'PING': ping, '352': who_reply,
                   '315': end_of_who}

def main():
    ''' Test stub '''
    tests = [":Garcia!~Frederick@B.E.A.R.S PRIVMSG #botparty :I love #bears",
             ':Bweeze086!~bweeze@bweeze.086 PRIVMSG Garcia :does this work?',
             'PING :92874389239837',
             ':irc.cccp-project.net 352 Garcia #bears Crono is.better.than.'\
             'you.at.battlefield * Crono Hr+ :0 Crono',
             ':irc.cccp-project.net 315 Garcia crono :End of /WHO list.']

    for test in tests:
        print(str(Message(test)))
    
if __name__ == '__main__':
    main()