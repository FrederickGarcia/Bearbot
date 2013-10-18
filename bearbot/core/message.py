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

    def __init__(self, raw):
        self.raw = raw.strip('\r\n')  # Raw message from host
        self.parse(self.raw)  # Sets prefix, command, and params
        self.parse_params()  # Sets attributes according to command type

    def parse(self, raw):
        ''' Parses message into three main parts and subparts '''
        
        # Message = *prefix, command, params
        if not raw[0] == ':':
            self.prefix = ''
            self.command, self.params = raw.split(' ', 1)
        else:
            self.prefix, self.command, self.params = raw.split(' ', 2)
            self.prefix = self.prefix[1:]  # Removes colon
            if '!' in self.prefix:  # Checks for nick!user@host
                self.nick, self.uhost = self.prefix.split('!')  # nick, uhost
                self.user, self.host = self.uhost.split('@')  # user, host

        # Params = middle, trailing
        if ':' in self.params:
            self.middle, self.trailing = self.params.split(':', 1)
        else:
            self.middle, self.trailing = self.params, ''
        self.middle = self.middle.strip()  # Removes trailing ' '

    def parse_params(self):
        ''' Sets attributes depending on message type '''
        if self.command in server_commands.keys(): 
            server_commands[self.command](self)

    def __str__(self):
        ''' Outputs attributes in human-readable format '''
        if hasattr(self, 'string'):
            return self.string
        
        # Default strings for messages undefined
        if not self.prefix is None:
            return ('%s %s %s %s' % (self.prefix, self.command, self.middle,
                                     self.trailing))
        return ('%s %s %s' % (self.command, self.middle, self.trailing))


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
    pm.source, pm.content = pm.middle, pm.trailing  # Sets source, content
    
    # Sets human-readable string
    if hasattr(pm, 'nick'):
        pm.string = ('%s <%s> %s' % (pm.source, pm.nick, pm.content)); return
    pm.string = ('%s %s <%s> %s' % (pm.prefix, pm.command,pm.source,
                                    pm.content))

def ping(pmsg):
    ''' Sets PING attributes '''
    pmsg.string = ('%s %s' % (pmsg.command, pmsg.trailing))
    
def join(jmsg):
    ''' Sets JOIN attributes '''
    jmsg.channel = jmsg.middle
    jmsg.string = ('━━▶  %s (%s) has joined %s' %
                   (jmsg.nick, jmsg.uhost, jmsg.channel))

def part(pmsg):
    ''' Sets PART attributes '''
    pmsg.channel = pmsg.middle
    pmsg.string = ('◀━━  %s (%s) has left %s' %
                   (pmsg.nick, pmsg.uhost, pmsg.channel))

def nick(nmsg):
    ''' Sets NICK attributes '''
    nmsg.new_nick = nmsg.trailing
    nmsg.string = ('❢  %s is now known as %s' %
                   (nmsg.nick, nmsg.new_nick))
    
def quit_(qmsg):
    ''' Sets QUIT attributes '''
    qmsg.quit_message = qmsg.params[1:]
    qmsg.string = ('◀━━  %s (%s) has quit (%s)' % (qmsg.nick,
                      qmsg.uhost, qmsg.quit_message))

def notice(nmsg):
    ''' Sets NOTICE attributes '''
    nmsg.source, nmsg.content = nmsg.middle, nmsg.trailing
    if hasattr(nmsg, 'nick'):
        nmsg.string = ('%s (%s) - NOTICE - %s' %
                       (nmsg.nick, nmsg.uhost, nmsg.content)); return
    nmsg.string = ('%s - NOTICE - %s' % (nmsg.prefix, nmsg.content))

''' Command Response Messages

Just like above, these functions serve to set attributes unique to the
type of command a message has.  These are server replies that have
three digit control codes as commands.  In the range 200-399 are server
responses to commands given to them.

'''

def who_reply(who):
    ''' (352 - RPL_WHOREPLY) sets attributes for WHO command replies '''
    who.source, who.channel, who.user, who.host, who.server, who.nick,\
    who.flags = who.middle.split()
    who.hopcount, who.realname = who.trailing.split()
    
    who.string = ('%s %s %s@%s (%s)' %
                  (who.channel, who.nick, who.user, who.host, who.realname))

def end_of_who(end_msg):
    ''' (315 - RPL_ENDOFWHO) sets attributes for ENDOFWHO messages '''
    end_msg.source, end_msg.target = end_msg.middle.split()
    end_msg.content = end_msg.trailing

def motd(motd_msg):
    ''' (372, 375, 376 - MOTD) sets attributes for MOTD messages'''
    motd_msg.source, motd_msg.content = motd_msg.middle, motd_msg.trailing
    motd_msg.string = ('✉  %s' % motd_msg.content)

# Dictionary of server commands to their respective setup methods
server_commands = {
        'PRIVMSG': privmsg, 'PING': ping, '352': who_reply, '315': end_of_who, '372': motd,
        '375': motd, '376': motd, 'JOIN': join, 'PART': part, 'NICK': nick,
        'QUIT': quit_, 'NOTICE': notice
    }

def main():
    ''' Test stub '''
    tests = [
        ":Garcia!~Frederick@B.E.A.R.S PRIVMSG #botparty :I love #bears",
        ':Bweeze086!~bweeze@bweeze.086 PRIVMSG Garcia :does this work?',
        'PING :92874389239837',
        ':irc.cccp-project.net 352 Garcia #bears Crono is.better.than.you.at'\
        '.battlefield * Crono Hr+ :0 Crono',
        ':irc.cccp-project.net 315 Garcia crono :End of /WHO list.',
        ':Umbreoff!EliteBNC@why.does.everyone.hate.me.so.much NICK :Umbreon',
        ':Combot!~Combot@my.name.isnt.cumbot QUIT :Ping timeout: 240 seconds',
        ':MisterKpak!~IceChat77@Rizon-589BB261.bflony.fios.verizon.net PART '\
        '#chat',
        ':MisterKpak!~IceChat77@Rizon-589BB261.bflony.fios.verizon.net JOIN '\
        ':#chat',
        ':MisterKpak!~IceChat77@Rizon-589BB261.bflony.fios.verizon.net QUIT '\
        ':Killed (irc.sxci.net (4 joins/parts in #chat within 3 seconds.))',
        ':Ziginox!~geek@418.I.am.a.teapot PRIVMSG #chat :ACTION is blown aw'\
        "ay by the force of Rosie's statement",
        ':Global!service@rizon.net NOTICE Bearbot :[Logon News - May 21 201'\
        '1] First time on Rizon? Be sure to read the FAQ! http://s.rizon.ne'\
        't/FAQ',
        ':irc.cccp-project.net NOTICE AUTH :*** Looking up your hostname...'
    ]

    for test in tests:
        print(str(Message(test)))

if __name__ == '__main__':
    main()