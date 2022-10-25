from bs4 import BeautifulSoup
import regex as re

# just to get all the get_* soup functions in one place!
class NovelParser:
    def parse_max_page(self, soup):
        max_page = int(soup.find('a',{'class':'next_page'}).previous_sibling.text)       # get max page number of wanted search result
        return max_page
    
    def parse_titles(self, soup):
        all_titles = []
        titles = soup.find_all('div',{'class':'search_title'})
        for title in titles:
            title_str = title.find('a').text
            all_titles.append(title_str)
        return all_titles

    def parse_details(self,soup):
        nvl_dict = {}                                                                                                # empty dictionary for details later
        title = soup.find('div',class_='seriestitlenu').text
        description = soup.find('div',id='editdescription').text.replace('\n',' ')
        genres = soup.find('div',id='seriesgenre').text.strip().replace('\n','').split(sep=' ')
        tags = [tag.text for tag in soup.find('div',id='showtags').find_all('a')]
        nvl_dict = {
            'title':title,
            'description':description,
            'genres':genres,
            'tags':tags
        }
        nvl_dict['overall_rates'] = float(re.findall(r'\d.\d',soup.find('span',{'class':'uvotes'}).text)[0])
        row_rates = soup.find('table',id='myrates').find_all('tr')
        for row in row_rates:
            rate = int(re.findall(r'\d{1,5}',row.text)[0])
            vote = int(re.findall(r'\d+',row.text)[2])
            nvl_dict[f'{rate}_star_votes'] = vote
        if (soup.find(lambda tag: tag.name=='h5' and tag.text=='Recommendations').next_sibling.text=='N/A'):
            nvl_dict['rec_list'] = []
        else:
            rec = soup.find(lambda tag: tag.name=='h5' and tag.text=='Recommendations').find_all_next(name='a',class_='genre',limit=10)
            nvl_dict['rec_list'] = [r.text for r in rec]
        return nvl_dict