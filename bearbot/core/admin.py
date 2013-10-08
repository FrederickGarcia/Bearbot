'''
Created on Sep 27, 2013
Garcia

This module will contain administrative functions. Currently it depends on a proper
event/handler system and cannot be completed. Also, a separate database module may
be in the future.
'''

#Built-in
import sqlite3

#Core
from bearbot.core import command

db = sqlite3.connect('bearbot.db')
c = db.cursor()

#This creates the tables and will only need to be ran once.
def init_user_tables():
    assert c.executescript('''
        CREATE TABLE users(
            user_id INTEGER PRIMARY KEY NOT NULL, 
            nick CHAR(50) NOT NULL,
            password CHAR(12) NOT NULL,
            acess_level INT
        );
        CREATE TABLE access_levels(
            nick CHAR(50) FOREIGN KEY NOT NULL, 
            host_mask CHAR(50) NOT NULL
        );
    ''')

    print('user and access_levels database tables created successfully.')

#Adds user to user table in the database
def add_user(nick):
    if not user_exists(nick):
        c.execute("INSERT INTO users (nick) VALUES (?);", nick)
        db.commit()

#Checks if user exists in the database already
def user_exists(nick):
    c.execute('SELECT * FROM users WHERE nick=?', nick)
    if c.fetchone() == nick:
        return True
    return False

def set_access(nick, access_lvl):
    pass

def get_access(nick):
    #return access_lvl
    pass

def get_access_dic():
    #return access_dic
    pass

def register_host(nick, password):
    pass

#/access *[nick] *[9999] - sets, lists, and gets access levels for users
#/access - lists all access levels
#/access [nick] - returns user access level
#/access [nick] [9999] - sets user access level
def access(cmd):
    if cmd.args == None:
        cmd.reply('Access levels: %s' % (', ').join(get_access_dic()))
    if len(cmd.args) == 1:
        cmd.reply('%s has access level: %s' % (cmd.args[0], get_access(cmd.args[0])))
    if len(cmd.args) == 2:
        set_access(cmd.args[0], cmd.args[1])
        cmd.reply('%s access level set to: %s' % (cmd.args[0], cmd.args[1]))
    if len(cmd.args) > 2:
        cmd.reply('Improper syntax. Requires: /access *[nick] *[9999] (*optional)')
        
def register(cmd):
    pass


init_user_tables()
db.close()

def main():
    pass

if __name__ == '__main__':
    main()
