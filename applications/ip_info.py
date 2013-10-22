'''
Created on Oct 21, 2013
@author: Garcia
'''

import json
from urllib import request, error

from bearbot.core.command import *
from bearbot.core.util import Colors

c = Colors.blue + Colors.bold
e = Colors.end
 
class IPError(Exception):
    pass
 
class IP(object):
    ''' Information about the IP address 
    
    Uses Telize RESTful API to create an object with geolocational and
    ISP information about an IP address
    '''
   
    def __init__(self, ip_address):
        self.ip = ip_address
        
        self.response = self.__fetch(self.ip)
        for k, v in self.response.items():
            setattr(self, k, v)
   
    def __fetch(self, url):
        req = request.Request('http://www.telize.com/geoip/%s' % self.ip)
        req.add_header('User-Agent', 'Mozilla/5.0')
       
        try:
            res = request.urlopen(req).read().decode('utf-8')
            return json.loads(res)
        except error.HTTPError as e:
            raise IPError(e.code)
        except error.URLError as e:
            raise IPError(e.reason)

def is_valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4 or\
                len(host_bytes) == 8 and len(valid) == 8
    except:
        return False

@one_arg
def ip_info(cmd):
    ''' ip [ip address] Provides information about an IP address '''
    ip_address = cmd.args[0]
    
    if not is_valid_ip(ip_address):
        cmd.reply('%s is not a valid IP address.' % ip_address)
        return
    if '192.168.' in ip_address or '127.0.' in ip_address:
        cmd.reply('Self referencing IP is invalid.')
        return

    ip = IP(ip_address)

    cmd.reply('Results for %s%s%s:\n'\
              '    %sCountry:%s %s (%s)    %sContinent:%s %s\n'\
              '    %sLatitude:%s %s    %sLongitude:%s %s\n'\
              '    %sDMA Code:%s %s    %sArea Code:%s %s    %sASN:%s %s\n'\
              '    %sISP:%s %s' % 
              (c, ip.ip, e, c, e, ip.country, ip.country_code3,
               c, e, ip.continent_code, c, e, ip.latitude, c, e, ip.longitude,
               c, e, ip.dma_code, c, e, ip.area_code, c, e, ip.asn, c, e,
               ip.isp))

command_dic.update({'ip': ip_info})

def main():
    ''' Test stub '''
    pass

if __name__ == '__main__':
    main()