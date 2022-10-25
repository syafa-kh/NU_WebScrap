import os
from logger import Logger
from proxer import Proxer
from novelparser import NovelParser
import pandas as pd
from bs4 import BeautifulSoup
import regex as re

# this main function is a behemoth and not very easy to read but it works!
def main():
    only_alphanumeric = re.compile('[^a-zA-Z\d\s-]+')
    logger = Logger().logger
    running = True
    max_page = 0
    curr_page = 0
    all_titles_lst = []
    max_novel = 0
    curr_novel = 0
    novel_details_df = pd.DataFrame()
    while running:
        if (os.path.isfile('titles.txt')):
            with open('titles.txt','r') as f:
                all_titles_lst = [t.rstrip() for t in f.readlines()]
            max_novel = len(all_titles_lst)
            max_page = 9999
            curr_page = 9999
        if (max_page==0):
            try:
                url = 'https://www.novelupdates.com/series-finder/?sf=1&org=495&rl=1&mrl=min&sort=sdate&order=desc'
                page = Proxer().open_site(url)
            except Exception as error:
                logger.error(f'Proxer().open_site() encounters an error. Passing. Please retry. error with type {type(error).__name__}: {error}')
                continue
            soup = BeautifulSoup(page.text,'html.parser')
            if (soup.find(lambda tag: tag.name=='a' and 'Cloudflare' in tag.text)):
                continue
            try:
                max_page = NovelParser().parse_max_page(soup)
                print(f'SUCCESSFULLY FETCHED MAX_PAGE: {max_page}')
                continue
            except Exception as error:
                logger.error(f'NovelParser().parse_max_page() encounters an error. Passing. Please retry. error with type {type(error).__name__}: {error}')
                continue
        elif ((max_page!=0) & (curr_page!=max_page)):
            try:
                curr_page+=1
                url_page = f'https://www.novelupdates.com/series-finder/?sf=1&org=495&rl=1&mrl=min&sort=sdate&order=desc&pg={curr_page}'
                page_page = Proxer().open_site(url_page)
            except Exception as error:
                logger.error(f'Proxer().open_site() encounters an error. Passing. Please retry. error with type {type(error).__name__}: {error}')
                curr_page-=1
                continue
            soup_page = BeautifulSoup(page_page.text,'html.parser')
            if (soup_page.find(lambda tag: tag.name=='a' and 'Cloudflare' in tag.text)):
                curr_page-=1
                continue
            # for some reason sometimes soup increase the actual max_page by 1, so it needs to be checked,
            # otherwise this will cause an infinite loop
            if ((curr_page==max_page) & (soup_page.find(lambda tag: tag.name=='div' and 'No results' in tag.text)==True)):
                continue
            try:
                titles_page = NovelParser().parse_titles(soup_page)
                all_titles_lst.extend(titles_page)
                if (curr_page==max_page):
                    all_titles_lst = [*set(all_titles_lst)]             # only use unique titles
                    max_novel = len(all_titles_lst)
                    with open('titles.txt','w') as f:
                        for t in all_titles_lst:
                            f.write(f'{t}\n')
                        print('SAVED TO TITLES.TXT')
                print(f'SUCCESSFULLY FETCHED TITLES FROM PAGE {curr_page}/{max_page}')
                continue
            except Exception as error:
                logger.error(f'NovelParser().parse_titles() encounters an error while fetching page {curr_page}/{max_page}. Passing. Please retry. error with type {type(error).__name__}: {error}')
                curr_page-=1
                continue
        elif ((curr_page==max_page) & (curr_novel!=max_novel)):
            try:
                title = all_titles_lst[curr_novel]
                title_link = only_alphanumeric.sub('',title.lower().rstrip())
                title_link = title_link.replace(' ','-')
                curr_novel+=1
                url_novel = f'https://www.novelupdates.com/series/{title_link}'
                page_novel = Proxer().open_site(url_novel)
            except AttributeError as error:
                logger.error(f'Probably not available or something. Check this title: {title}, here: {url_novel}.')
                continue
            except Exception as error:
                logger.error(f'Proxer().open_site() encounters an error. Passing. Please retry. error with type {type(error).__name__}: {error}')
                curr_novel-=1
                continue
            soup_novel = BeautifulSoup(page_novel.text,'html.parser')
            if (soup_novel.find(lambda tag: tag.name=='a' and 'Cloudflare' in tag.text)):
                curr_novel-=1
                continue
            try:
                detail_page = NovelParser().parse_details(soup_novel)
                novel_details_df = pd.concat([novel_details_df,pd.DataFrame.from_dict(detail_page,orient='index').T]).reset_index(drop=True)
                if (curr_novel == max_novel):
                    novel_details_df.to_csv('NU_20221023')
                print(f'SUCCESSFULLY FETCHED NOVEL {curr_novel}/{max_novel}')
            except Exception as error:
                logger.error(f'NovelParser().parse_details() encounters an error while fetching novel {curr_novel}/{max_novel}. Passing. Please retry. error with type {type(error).__name__}: {error}')
                curr_novel-=1
                continue
        elif ((curr_page==max_page) & (curr_novel==max_novel)):
            running = False
        else:
            logger.error('Loop is not ending')
            running = False


if __name__=='__main__':
    main()