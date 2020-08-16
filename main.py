# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:46:52 2020

@author: Piyush
"""

from scraper import GooglePlayStoreScraper



APPLICATION_NAME = 'subway surfers'




def main():
    app_name = APPLICATION_NAME
    
    scraper = GooglePlayStoreScraper(app_name)
    details = scraper.get_all_app_details()
    
    return details