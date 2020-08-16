from requests_module import Request
from bs4 import BeautifulSoup
from utils import get_resp_from_query
import time
from exceptions import AppNotFound, URLNotFound


class GooglePlayStoreScraper:
    origin_url = 'play.google.com'
    
    def __init__(self, query):
        self.query = query
        self.resp = get_resp_from_query(query)
        time.sleep(.5)
        self.query_soup = self.get_query_soup()
        self.app_url = self.get_first_link_from_search_results()
        if not self.app_url.startswith('https://'):
            self.app_url = 'https://' + self.app_url
        
        
        self.detail_page_resp = Request.get(self.app_url)
    
    def get_query_soup(self):
        soup = BeautifulSoup(self.resp.text, 'lxml')
        return soup
    
    
    def get_first_link_from_search_results(self):
        first_card = self.query_soup.find('div', class_ = 'Vpfmgd')
        if first_card:
            url = self.origin_url + first_card.find('a').get('href') if first_card.find('a') else None
            if url:
                return url
            
            else:
                raise URLNotFound('Could not find the url of %s' % (self.query))
                
        else:
            raise AppNotFound('Could not find any app by the name "%s"'  % (self.query))
            
    
    def get_all_app_details(self):
        details_dict = {'application_name' : None,
                        'developer_name' : None, 
                        'developer_url' : None,
                        'genre' : None, 
                        'genre_url' : None,
                        'average_rating' : None,
                        'total_rating' : None,
                        'description' : None,
                        'price' : None,
                        'application_url': None
                        
                       
                       
                       
                       }
        
        app_url = self.get_first_link_from_search_results()
        if not app_url.startswith('https://'):
            app_url = 'https://' + app_url
            
        resp = Request.get(app_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        
        details_dict['application_name'] = soup.find('h1', class_ = 'AHFaub').text
        
        details_dict['application_url'] = app_url
        
        if soup.find('span', class_ = 'T32cc'):
            
            details_dict['developer_name'] = soup.find('span', class_ = 'T32cc').text
        
            developer_a_tag = soup.find('span', class_ = 'T32cc').find('a')
            details_dict['developer_url'] = self.origin_url + developer_a_tag.get('href') if developer_a_tag else None
            
            
        
        strip_line = soup.find('div', class_ = 'qQKdcc')
        
        details_dict['genre'] = strip_line.find('a', attrs = {'itemprop' : 'genre'}).text if strip_line and strip_line.find('a', attrs = {'itemprop' : 'genre'}) else None
        
        details_dict['genre_url'] = self.origin_url + strip_line.find('a', attrs = {'itemprop' : 'genre'}).get('href') if strip_line and strip_line.find('a', attrs = {'itemprop' : 'genre'}) else None
        
        ratings_div = soup.find('div', class_ = 'K9wGie')
        
        details_dict['average_rating'] = ratings_div.find('div', class_ = 'BHMmbe').text if ratings_div and ratings_div.find('div', class_ = 'BHMmbe') else None
        
        details_dict['total_rating'] = ratings_div.find('span', class_ = 'EymY4b').text if ratings_div and ratings_div.find('span', class_ = 'EymY4b') else None
        
        description_div = soup.find('div', attrs = {'itemprop' : 'description'})
        
        details_dict['description'] = description_div.text if description_div else None
        
        price_span = soup.find('span', class_ = 'oocvOe')
        
        details_dict['price'] = price_span.text if price_span else None
        
        if details_dict['price'] == 'Install':
            details_dict['price'] = 'Free'
        
        footer_details = self.get_footer_details()
        
        details_dict.update(footer_details)
        
        
        
        
        return details_dict
    
        
        
    def get_footer_details(self):
        resp = self.detail_page_resp
        soup = BeautifulSoup(resp.text, 'lxml')
        
        footer_data = soup.find_all('div', class_ = 'BgcNfc')
        
        key_names = [item.text for item in soup.find_all('div', class_ = 'BgcNfc')]
        
        footer_dict = {}
        for data, i in zip(footer_data, range(len(footer_data))):
            footer_dict[key_names[i]] = data.findNext('span').text if data.findNext('span') else None
            
        if 'Developer' in footer_dict:
            del(footer_dict['Developer'])
       
        return footer_dict
    

Scraper = GooglePlayStoreScraper



