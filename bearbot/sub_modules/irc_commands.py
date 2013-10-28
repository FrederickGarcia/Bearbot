'''Caters to IRC commands other than PRIVMSG
Created on 29/10/2013

@author: Evan
'''

''' responds to ping command'''
def ping_(handler, msg):
    handler.bot.send('PONG %s' % msg.params) 