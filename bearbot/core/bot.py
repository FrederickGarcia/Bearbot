'''
Created on Sep 16, 2013
@author: Garcia

This module holds the Bot class.  Its purpose is to provide basic bot
functionality.  Anything beyond that scope should be in a different
module.

Note: The msg_gen produces an infinite amount of messages for the
      duration of the bot's life. There's a get_reply method that
      waits for a particular server reply and returns it. It is very
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
crlf = '\r\n'.encode()
cr = '\r'.encode()

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
        self.channels = self._set_channels(channels)
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
    
    # Initialization
    
    def _connect(self):
        ''' Connects to server and configures irc details  '''
        self.irc.connect((self.host, self.port))
        self.set_nick(self.nick)
        self.send('USER %s 0 * :%s' % (self.user_name, self.realname))
        errors = self.join(self.channels)
        self._listen()
    
    def _set_channels(self, channels):
        ''' Sets channels as list '''
        if isinstance(channels, str):
            return [channels,]
        return channels
    
    def _listen(self):
        while self.alive:
            for msg in self.msg_gen():
                self.handle(msg)
    
    def msg_gen(self):
        ''' Provides messages until bot dies '''
        for msg in self.irc.recv(self.buffer).split(crlf):
            if not len(msg) > 3:
                continue
            try:
                yield Message(msg.decode())
            except Exception as e:
                self.log('%s %s\n' % (except_str, str(e)))

    # Sending Methods
   
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
        ''' Joins channel(s) and returns None or error messages '''
        
        # Error reply commands from IRC RFC 2812 for JOIN
        errors = ['403', '405', '407', '437', '461',
                  '471', '473', '474', '475', '476', '479']
        error_msgs = []
        
        if isinstance(channels, str):  # Forces list
            channels = [channels,]

        for channel in channels:
            self.send('JOIN %s' % channel)
            for reply in self.get_reply(kill=errors+['353']):  # Verify join success
                if reply.command in errors:
                    channels.remove(channel)
                    error_msgs.append(reply)
                    print(error_msgs)
        self.channels.append(channels)
        
        print(error_msgs)
        if error_msgs == []:
            return None
        return error_msgs
        
    def part(self, channels, message=''):
        ''' Parts channel(s) with optional message '''
        if not isinstance(channels, list):
            channels = [channels,]

        for channel in channels:
            self.send('PART %s %s' % (channel, message))
        self.channels.remove(channels)
    
    def log(self, message):
        ''' Logs messages to the console '''
        if not message is None:
            print(str(message))  #logs to console
    
    # Receiving methods
    
    def who(self, target):
        ''' Sends who command and returns reply '''
        self.send('WHO %s' % target)
        return self.get_reply('352', kill=['315', '401', '403'])
        # 352 RPL_WHOREPLY, 315 RPL_ENDOFWHO, 401 ERR_NOSUCHNICK,
        # 403 ERR_NOSUCHCHANNEL
    
    def names(self, target):
        ''' Sends names command and returns reply '''
        self.send('NAMES %s' % target)
        return self.get_reply('353', kill=['366', '402'])
        # 353 RPL_NAMREPLY, 366 RPL_ENDOFNAMES, 402 ERR_NOSUCHSERVER

    # Utils
    
    def get_reply(self, commands=[], kill=[]):
        ''' Generator to return server command replies
        
        The commands parameter is the server reply command for the
        message reply to be returned (ie. '352' for a RPL_WHOREPLY).
        
        The kill parameter is the server reply command that signifies
        StopIteration.  (ie. ['315', '401', '403'] for RPL_ENDOFWHO,
        ERR_NOSUCHNICK, and ERR_NOSUCHCHANNEL.  If None by default,
        StopIteration occurs on first command found in commands.
        
        '''
        while True:
            for msg in self.msg_gen():
                self.handle(msg)
                if msg.command in commands:
                    if kill is []:
                        return msg
                    yield msg
                if msg.command in kill:
                    return msg

    
    def handle(self, msg):
        ''' Handles Messages '''
        self.log('◀    %s' % (msg))
        SpaghettiHandler(self, msg)

    def set_msg_delay(self, seconds):
        ''' Sets delay for messages '''
        try:
            if not 0 <= seconds <= 10:
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