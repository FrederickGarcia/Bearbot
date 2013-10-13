'''
Created on Sep 16, 2013
@author: Garcia

This module holds the Bot class.  Its purpose is to provide basic bot
functionality.  Anything beyond that scope should be in a different
module.

'''

import socket
from time import sleep

from bearbot.sub_modules import misc_commands

from bearbot.core.message import *
from bearbot.core.event import *

class Bot(object):
    ''' Connects to an irc server and listens to incoming messages

    It runs a loop and receives messages from a socket.  Then it
    creates Message objects to pass to a message handler.  To drive
    this class, create a Bot object and use its connect command.

    Ex. bearbot = Bot('irc.rizon.net', 'Garcia', 'pass123',
                      '#my_channel')
        bearbot.connect()

    '''

    def __init__(self, host, owner, password, channels, user_name='Bear',
                 nick='Bearbot', real_name='I am the bearest', cmd_prefix='.',
                 buffersize=3072, port=6667, msg_delay=.5):
        self.host = host
        self.owner = owner
        self.password = password
        self.channels = channels
        self.user_name = user_name
        self.nick = nick
        self.realname = real_name
        self.cmd_prefix = cmd_prefix
        self.buffersize = buffersize
        self.port = port
        self.msg_delay = msg_delay  # Flood control

        self.on = True  # Running status
        self.irc = socket.socket()
        self._connect()
    
    # Helpers
    
    def _connect(self):
        ''' Connects to server and configures irc details  '''
        self.irc.connect((self.host, self.port))
        self.set_nick(self.nick)
        self.send('USER %s 0 * :%s' % (self.user_name, self.realname))
        self.join(self.channels)
        self._listen()  # Listens for incoming messages

    def _listen(self):
        ''' Listens for incoming messages '''
        while self.on :
            try:
                for msg in self.get_messages():
                    self.log('◀    %s' % (msg))
                    SpaghettiHandler(self, msg)
            except Exception as e:
                self.log('Exception occurred: %s' % str(e))
    
    def get_messages(self):
        ''' Generator to return Message objects received from host '''
        msgs = self.irc.recv(self.buffersize).split(('\r\n').encode())
        for msg in msgs:
            if len(msg) > 3:
                try:
                    message = Message(msg.decode())
                except Exception as e: print('** While decoding message: %s'
                                             % e)
                yield message

    # Outgoing Command Methods
   
    def send(self, msg):
        ''' Sends message to the host using socket '''
        self.irc.send(('%s\r\n' % msg).encode())
        self.log('▶    %s ' % msg)
        sleep(self.msg_delay)
    
    def send_generic(self, command, target, message):
        ''' Sends a message to a target using a command '''
        self.send('%s %s :%s' % (command, target, message))

    def say(self, target, message):
        ''' Sends  PRIVMSG to target (user|#channel) '''
        self.send_generic('PRIVMSG', target, message)
    
    def notify(self, target, message):
        ''' Sends NOTICE to target with message '''
        self.send_generic('NOTICE', target, message)
    
    def action(self, target, action_msg):
        ''' Performs an action (/me msg) '''
        self.say(target, '\001ACTION %s\001' % action_msg)
    
    def quit(self, quit_msg=''):
        ''' Disconnects from the irc server '''
        self.send('QUIT :%s' % quit_msg)
        
    def set_nick(self, nick):
        ''' Changes bot's nickname '''
        self.send('NICK %s' % nick)
        # Requires checking for nick change success
        # Needs to change self.nick on success
        # Ask for forgiveness if nick unsuccessful
    
    def join(self, channels):
        ''' Joins channel(s) '''
        self.send('JOIN %s' % channels)
        # Requires checking for join success
        # Needs to update self.channels on join success
        # Ask for forgiveness if join unsuccessful
        # Leave regular error checking for interface
        # No loop necessary: JOIN #channel, #channel,...
        
    def part(self, channels, message=''):
        ''' Parts channel(s) with optional message '''
        if not isinstance(channels, str):
            self.send('PART %s %s' % ((', ').join(channels), message))
        else:
            self.send('PART %s %s' % (channels, message))
        # Needs to update self.channels on part

    '''Will need a proper event handling system for this:
    
    def who(bot, nick):
        bot.send('who %s' % nick)
        return get_msg('who', nick)
    
    def get_msg():
    '''   

    # Internal Helper Methods

    def log(self, message):
        ''' Logs messages to the console '''
        if message or message != '':
            print(str(message))  #logs to console

    def set_msg_delay(self, seconds):
        ''' Sets delay for messages '''
        try:
            if seconds >= 0 and seconds <= 30:
                self.msg_delay = seconds
                self.log('** Message delay set to: %s seconds' % seconds)
        except Exception as e:
            self.log('** Message delay: ' % e)

    def close_connection(self):
        ''' Closes the irc connection '''
        self.irc.close()

def main():
    ''' Driver '''
    bearbot = Bot('irc.rizon.net', 'Garcia', 'hbdhbd123', '#botparty')

if __name__ == '__main__':
    main() 