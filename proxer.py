from logger import Logger
from pool import Pool
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib3 import Timeout
import cloudscraper

class Proxer:
    logger = Logger().logger
    pool_end,prox_list,head_list = Pool(logger).create_pools()
    pool_count = 0
    page_count = 0
    pool_repeat = 0 
    curr_prox = prox_list[pool_count]
    curr_head = head_list[pool_count]

    def proxy_changer(self):
        try:
            if (self.__class__.pool_count==self.pool_end-1):
                self.__class__.pool_repeat+=1
                self.__class__.pool_count=0
                if(self.__class__.pool_repeat>2):             # get new pool after 2 times 
                    self.__class__.pool_end,self.__class__.prox_list,self.__class__.head_list = Pool(self.__class__.logger).create_pools()
                    self.__class__.pool_count=0
                    self.__class__.page_count=0
                    self.__class__.pool_repeat=0
            else:
                self.__class__.pool_count+=1
            self.__class__.curr_prox = self.__class__.prox_list[self.__class__.pool_count]
            self.__class__.curr_head = self.__class__.head_list[self.__class__.pool_count]
        except Exception as error:
            self.__class__.logger.error(f'Proxer().proxy_changer() encounters an error. Passing. Please retry. error with type {type(error).__name__}: {error}')
            pass

    def open_site(self,url):
        self.__class__.page_count+=1
        if (self.__class__.page_count%2==0):
            self.proxy_changer()
        with requests.Session() as sess:
            retry = Retry(connect=5,backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            sess.mount('https://', adapter)
            sess.mount('https://', adapter)
            cfs = cloudscraper.create_scraper(sess=sess)
            page = cfs.get(url,headers=self.__class__.curr_head,proxies={'http':self.__class__.curr_prox,'https':self.__class__.curr_prox},timeout=Timeout(connect=30,read=120),verify=True)
        return page