import re
import urllib.request
import json

class Parser:
    def __init__(self, filename):
        self.file = open(filename)
        self.ips = []

    def parse(self):
        for line in self.file:
            regIp = '(\d+\.\d+\.\d+\.\d+)'

            destIps = re.search('Dst: ' + regIp, line)
            srcIps = re.search('Src: ' + regIp, line)

            if (destIps):
                self.addIp(destIps.group(1), 'dest')

            if (srcIps):
                self.addIp(srcIps.group(1), 'src')

    def collectData(self):
        output = open('output.txt', 'w')

        ips = sorted(self.ips, key = lambda item: item['count'], reverse = True)

        for ip in ips:
            response = json.loads(urllib.request.urlopen('http://ip-api.com/json/' + ip['ip']).read())

            if 'org' not in response:
                continue

            output.write('{} -- {} -- {} occurances'.format(ip['ip'], response['org'], ip['count']))
            output.write('\n')

    def addIp(self, ip, designation):
        if (self.isLocalIp(ip)):
            return

        existing = filter(lambda item: item['ip'] == ip, self.ips)
        item = next(existing, None)
        if (item):
            item[designation] = True;
            item['count'] += 1
        else:
            self.ips.append({
                'ip': ip,
                'count': 1,
                designation: True
            })

    def isLocalIp(self, ip):
        if '127.0.0.1' == ip:
            return True

        if '255.255.255.255' == ip:
            return True

        if re.search('^192\.168', ip):
            return True

        return False