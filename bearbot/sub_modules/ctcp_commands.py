'''responds to standard ctcp requests
Created on 29/10/2013

@author: Evan
'''

#TODO Add the missing requests
def ctcp_(handler, msg):
    if msg.trailing.startswith('\001' 'VERSION'):
        #TODO get version string from bot
        handler.bot.notify(msg.nick, '\001' 'VERSION ' 'bearbot 0.1a test' '\001')
    elif msg.trailing.startswith('\001' 'PING'):
        handler.bot.notify(msg.nick, msg.content)

'''what a weird protocol! - Evan'''