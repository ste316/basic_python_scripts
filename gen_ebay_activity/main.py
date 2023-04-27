from requests import get 
import re
from threading import Thread
from random import choice, randint
from time import sleep
from user_agent import get_random_agent

class genEbayVisualizzation:
    def __init__(self, link: str, timeout: float, visit: int):
        self.VISIT = visit
        self.TIMEOUT = timeout
        self.LINK = link
        self.proxy = []
        self.load_proxy()
        print(f'Generating {self.VISIT} visualizzation\n\tProduct link: {self.LINK}\n\tTimeout: {self.TIMEOUT}')

    def getPage(self):
        # add random param to avoid being cached
        # useful when running without proxies
        uncached_link = self.LINK+'?stegg='+str(randint(0,250)) 
        headers={
                'User-Agent' : get_random_agent(),
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding' : 'gzip, deflate, br',
                'Accept-Language' : 'it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection' : 'keep-alive',
                'Host' : self.LINK.split('/')[2] ,
                'Sec-Fetch-Dest' : 'document',
                'Sec-Fetch-Mode' : 'navigate',
                'Sec-Fetch-Site' : 'none',
                'Sec-Fetch-User' : '?1'
            }
        if len(self.proxy) == 0: get(uncached_link, headers=headers)
        else: get(uncached_link, headers=headers, proxies=self.choose_proxy())

    def choose_proxy(self):
        px = choice(self.proxy)
        if len(px.split(':')) == 2: # proxy without authentication
            return {
                'http': 'http://{}'.format(px),
                'https': 'https://{}'.format(px)
            }

        elif len(px.split(':')) == 4: # proxy with authentication
            splitted = px.split(':')
            return {
                'http': 'http://{0}:{1}@{2}:{3}'.format(splitted[2], splitted[3], splitted[0], splitted[1]),
                'https': 'https://{0}:{1}@{2}:{3}'.format(splitted[2], splitted[3], splitted[0], splitted[1])
            }

    def load_proxy(self):
        ipv6 = re.compile('^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)(?:%25(?:[A-Za-z0-9\\-._~]|%[0-9A-Fa-f]{2})+)?$')
        ipv4 = re.compile('^(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$')
        proxy = open('proxy.txt', 'r')
        if proxy != '': 
            print('Loading proxy')
            for line in proxy:
                if type(re.search(ipv4,line)) or type(re.search(ipv6,line)) == re.Match :
                    self.proxy.append(line)
            print(f'Found {len(self.proxy)} valid ip')
        
        if len(self.proxy) == 0: print('Using local IP')

    def genThread(self):
        thread = []
        for _ in range(self.VISIT):
            process = Thread(target = self.getPage)
            thread.append(process)
        return thread

    def run(self):
        thread = self.genThread()
        for (i, item) in enumerate(thread):
            item.start()
            print(f'Thread started: {i+1}', end='\r')
            sleep(self.TIMEOUT)

if __name__ == '__main__':
    link = 'ADD YOUR EBAY PRODUCT LINK'
    timeout = 0.5
    visit = 5
    a = genEbayVisualizzation(link, timeout, visit)
    a.run()
