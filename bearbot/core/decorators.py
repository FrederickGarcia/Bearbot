''' User Decorators

These make writing commands simple by providing the ability to add
common functionality to commands.

* = to be added
@no_access*    - Command accessible to all users
@admin*        - Command accessible only to highest access level
@owner         - Command accessible only to the owner
@requires_args - Command that requires arguments
@no_args       - Command require no arguments
@as_string     - Parses arguments to string, @requires_args

'''

from functools import wraps

# Argument decorators

def no_args(cmd_def):
    ''' Returns error message to user if arguments are given '''
    @wraps(cmd_def)
    def new_cmd_def(cmd):
        if cmd.args is None:
            cmd_def(cmd)
        else:
            cmd.reply('Invalid entry. This command accepts no arguments.')
    return new_cmd_def

def one_arg(cmd_def):
    ''' Checks for one argument '''
    @wraps(cmd_def)
    def new_cmd_def(cmd):
        if cmd.args is None or len(cmd.args) > 1:
            cmd.reply('Invalid entry. This command requires one argument.')
        else:
            cmd_def(cmd)
    return new_cmd_def

# One or many args
def requires_args(cmd_def):
    ''' Returns error message to user if no arguments are given '''
    @wraps(cmd_def)
    def new_cmd_def(cmd):
        if not cmd.args is None:
            cmd_def(cmd)
        else:
            cmd.reply('Invalid entry. This command requires arguments.')
    return new_cmd_def

# Access decorators

def owner(cmd_def):
    ''' Sets the command to only be used by the owner '''
    @wraps(cmd_def)
    def new_cmd_def(cmd):
        if cmd.msg.nick == cmd.bot.owner:
            cmd_def(cmd)
        else:
            cmd.notify('You do not have permission to run this command.')
    return new_cmd_def

# More decorators

def as_string(cmd_def):
    ''' Turns the argument list into a string '''
    @requires_args
    @wraps(cmd_def)
    def new_cmd_def(cmd):
        cmd.args = (' ').join(cmd.args)
        cmd_def(cmd)
    return new_cmd_def