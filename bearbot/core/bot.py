'''
Created on Sep 16, 2013
@author: Garcia

This module holds the Bot class.  Its purpose is to provide basic bot
functionality.  Anything beyond that scope should be in a different
module.

Note: The msg_generator produces an infinite amount of messages for the
      duration of the bot's life. There's a get_response method that
      waits for a particular server response and returns it. It is very
      helpful. It throws all the messages to the handle method until it
      finds what its looking for and then returns flow back to the
      listener.

'''

import socket
from time import sleep

from bearbot.sub_modules import misc_commands

from bearbot.core.message import *
from bearbot.core.event import *

except_str = '\n◢✘◣ EXCEPTION OCCURRED - '

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
                 buffer=4096, port=6667, msg_delay=.5):
        self.host = host
        self.owner = owner
        self.password = password
        self.channels = channels
        self.user_name = user_name
        self.nick = nick
        self.realname = real_name
        self.cmd_prefix = cmd_prefix
        self.buffer = buffer  # Buffer size in bytes
        self.port = port
        self.msg_delay = msg_delay  # Flood control

        self.alive = True  # Running status
        self.irc = socket.socket()
        self._connect()
    
    # Helpers
    
    def _connect(self):
        ''' Connects to server and configures irc details  '''
        self.irc.connect((self.host, self.port))
        self.set_nick(self.nick)
        self.send('USER %s 0 * :%s' % (self.user_name, self.realname))
        self.join(self.channels)
        self._listen()
    
    def _listen(self):
        for msg in self.msg_generator():
            self.handle(msg)
    
    def msg_generator(self):
        ''' Provides messages until bot dies '''
        while self.alive:
            for msg in self.irc.recv(self.buffer).split('\r\n'.encode()):
                if len(msg) > 3:
                    try:
                        yield Message(msg.decode())
                    except Exception as e:
                        self.log('%s %s\n' % (except_str, str(e)))

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
    
    def join(self, channels):
        ''' Joins channel(s) '''
        self.send('JOIN %s' % channels)
        # Requires checking for join success
        # Needs to update self.channels on join success..
        
    def part(self, channels, message=''):
        ''' Parts channel(s) with optional message '''
        if not isinstance(channels, str):
            self.send('PART %s %s' % ((', ').join(channels), message))
        else:
            self.send('PART %s %s' % (channels, message))
        self.channels -= channels
    
    def who(self, nick):
        ''' Sends who command and returns response '''
        self.send('WHO %s' % nick)
        return self.get_response('352')

    # Utils

    def log(self, message):
        ''' Logs messages to the console '''
        if not message is None:
            print(str(message))  #logs to console
    
    def get_response(self, command):
        ''' Returns server response command code message '''
        for msg in self.msg_generator():
            self.handle(msg)
            if msg.command == command:
                return msg
            # Needs a time-out
            # Will also need to be a generator
            # to allow for multiple responses (/who #channel etc)
            
    def handle(self, msg):
        ''' Handles Messages '''
        self.log('◀    %s' % (msg))
        SpaghettiHandler(self, msg)

    def set_msg_delay(self, seconds):
        ''' Sets delay for messages '''
        try:
            if not seconds >= 0 and not seconds <= 30:
                return
            self.msg_delay = seconds
            self.log('✽✽ Message delay set to: %s seconds ✽✽' % seconds)
        except Exception as e:
            self.log('%s (Message delay) ' % (except_str, e))

    def close_connection(self):
        ''' Closes the irc connection '''
        self.irc.close()

def main():
    ''' Driver '''
    bearbot = Bot('irc.rizon.net', 'Garcia', 'hbdhbd123', '#botparty')

if __name__ == '__main__':
    main() 