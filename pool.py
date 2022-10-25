import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
import random

class Pool:
    def __init__(self,logger):
        self.logger = logger
        self.proxy_pool()
        self.accepts_pool()
        
    # get proxies pool
    # this one is free and slow af so you should def invest in a better one if you can afford it xx
    # (it was so slow i haven't finished running the script btw)
    # (and also i'm trying to scrape like 3k+ pages in one go without setting up proper precautions before)
    def proxy_pool(self):
        try:
            url = 'https://www.sslproxies.org/'
            with requests.Session() as res:                                                             # immediately close after done
                proxies_page = res.get(url)
            soup = BeautifulSoup(proxies_page.text,'html.parser')
            proxies_table = soup.find(lambda tag: tag.name=='table' and 'IP Address' in tag.text)       # find table that has 'IP Address' in it
            proxies_table_body = proxies_table.find('tbody')                                            # find the body of the table
            proxies = []
            for row in proxies_table_body.find_all('tr'):
                proxies.append('{}:{}'.format(row.find_all('td')[0].string.replace(' ',''), row.find_all('td')[1].string))  # get the IP address and port
        
        # in case connection failed, use pre-defined IP
        # from different sources, so hopefully they dont fail at the same time
        # (setting up flags: moments before disaster (hasnt happened yet))
        except Exception as error:
            self.logger.error(f"proxy_pool() encounters an error. Reverting back to pre-defined IP and Port. error with type {type(error).__name__}: {error}")        # save error in a file
            proxies = [
                '145.239. 85.58:9300',   # from vpnoverview
                '8.219.74.58:8080',      # from free-proxy-list
                '103.152.112.145:80',    # from freeproxylist
                '195.201.61.51:8000'     # from javatpoint
            ]
        self.proxies = proxies

    # get accept values pool
    def accepts_pool(self):
        try:
            url = 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation/List_of_default_Accept_values'
            with requests.Session() as res:                                                                 # immediately close after done
                accepts_page = res.get(url)
            soup = BeautifulSoup(accepts_page.text,'html.parser')
            accepts_table = soup.find('h2',id='default_values').parent                                      # find table with default_values as an id
            accepts_table_body = accepts_table.find('tbody')                                                # find the body of the table
            accepts = {}                                                                                    # dictionary will accept 'firefox' or 'chrome' as keys and accepts string as the value
            accepts['Firefox'] = accepts_table_body.find(lambda tag: tag.name=='td' and 'Firefox' in tag.text).next_sibling.next_sibling.text   # for firefox
            accepts['Chrome'] = accepts_table_body.find(lambda tag: tag.name=='td' and 'Chrome' in tag.text).next_sibling.next_sibling.text     # for chrome
        
        # in case connection failed, use pre-defined accept values
        except Exception as error:
            self.logger.error(f"accepts_pool() encounters an error. Reverting back to pre-defined accept values. error with type {type(error).__name__}: {error}")        # save error in a file
            accepts = {
                'Firefox':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Chrome':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
            }
        self.accepts = accepts

    # get user agent values pool
    def user_agent_pool(self):
        try:
            ua = UserAgent()                            # create useragent instance
            if random.random() > 0.5:                   # create randomness to avoid block
                random_user_agent = ua.chrome           # get ua for chrome
            else:
                random_user_agent = ua.firefox          # get ua for firefox
        
        # in case connection failed, use pre-defined valid user-agent
        except FakeUserAgentError as error:
            self.logger.error(f"FakeUserAgent didn't work. Generating headers from the pre-defined set of headers. error with type {type(error).__name__}: {error}")        # save error in a file
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
                "Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"]  # Just for case user agents are not extracted from fake-useragent package
            random_user_agent = random.choice(user_agents)
        self.random_user_agent = random_user_agent

    # get headers pool, where header = user-agents and accept values
    def header_pool(self):
        self.user_agent_pool()
        valid_accept = self.accepts['Firefox'] if self.random_user_agent.find('Firefox') > 0 else self.accepts['Chrome']
        headers = {
            'User-Agent':self.random_user_agent,
            'Accept':valid_accept
        }
        return headers

    # create proxies and headers pool so it can be rotated
    def create_pools(self):
        self.headers = [self.header_pool() for ind in range(len(self.proxies))]
        return len(self.proxies), self.proxies, self.headers