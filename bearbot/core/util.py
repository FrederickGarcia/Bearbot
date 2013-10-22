'''
Created on Oct 22, 2013
@author: Garcia
'''

class Colors:
    
    # End of color 
    # 'this is ' bold + 'bold' + end + ' and this is not')
    end = '\u000F'
    
    # Format
    bold = '\u0002'
    underline = '\u001f'
    italics = '\u0016'
    
    # Shorthand
    b, u, i = bold, underline, italics
    
    # Colors
    red = '\u000304'
    black = '\u000301'
    green = '\u000309'
    dark_green = '\u000303'
    darkBlue = '\u000302'
    blue = '\u000312'
    cyan = '\u000310'
    aqua = '\u000311'
    yellow = '\u000308'
    olive = '\u000307'
    brown = '\u000305'
    light_gray = '\u000315'
    gray = '\u000314'
    magenta = '\u000313'
    purple = '\u000306'
    white = '\u000300'
    
    def parse(self):
        pass
