'''responds to standard ctcp requests
Created on 29/10/2013

@author: Evan, Garcia
'''

# TODO add DCC support

from time import strftime

from bearbot.core import bot

C = '\001'  # CTCP token
CTCP_COMMANDS = {
        'PING': '<data> - Returns CTCP PING with data.',
        'VERSION': "No arguments - Returns Bearbot's version number and platform Bearbot is currently on.",
        'SOURCE': 'No arguments - Returns the github repository for Bearbot.',
        'TIME': 'No arguments - Returns the local time of the system Bearbot is running on.',
        'CLIENTINFO': 'No arguments - Returns a list of CTCP commands and their descriptions.',
        'USERINFO': 'No arguments - Returns an arbitrary reply.',
        'FINGER': 'No arguments - FINGER command is deprecated.',
        'DCC': 'Bearbot does not support DCC currently.',
        'ERRMSG': 'Returns an error message if CTCP command is unavailable.'
    }
ERRMSG = ' - Invalid CTCP command. Check CLIENTINFO for valid commands.'

def ctcp_(handler, msg):

    # TODO needs is_ctcp prior to ctcp_ call
    
    # Return early if not CTCP
    if not msg.trailing.startswith(C):
        return

    cmd = msg.trailing.strip(C)
    
    def reply(reply_msg):
        handler.bot.notice(msg.nick, '%s%s %s%s' % (C, cmd, reply_msg, C))
    
    if cmd.startswith('PING'):
        handler.bot.notice(msg.nick, msg.content)
    elif cmd == 'VERSION':
        reply(handler.bot.version)
    elif cmd == 'SOURCE':
        reply(bot.source)
    elif cmd == 'TIME':
        reply(strftime('%Y-%m-%d %H:%M:%S'))
    elif cmd == 'CLIENTINFO':
        for command, description in CTCP_COMMANDS.items():
            reply('[%s] %s' % (command, description))
    elif cmd == 'USERINFO':
        reply("I'm a cybernetic bear")
    elif cmd == 'FINGER':
        reply('Deprecated. Use USERINFO.')
    elif 'DCC' in cmd:  # For DCC, XDCC, RDCC
        # TODO call a DCC parsing function which calls a DCC module to handle
        # DCC commands.  Will presumably ask for permission.
        handler.bot.notice(msg.nick, 
                '%sERRMSG %s - DCC is unsupported currently.%s' % (C, cmd, C))
    else:
        handler.bot.notice(msg.nick, '%sERRMSG %s %s%s' % (C, cmd, ERRMSG, C))

'''what a weird protocol! - Evan'''
