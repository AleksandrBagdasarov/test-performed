import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv


def _make_url_by_company_name(company_name):
    '''
    There are exclusions for link building for different companies.
    Selenium searches the site by name and returns the generated link by the site itself.
    '''
    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://finance.yahoo.com')
    input_company_name = driver.find_element_by_id('yfin-usr-qry')
    input_company_name.send_keys(f'{company_name}')
    input_company_name.send_keys(Keys.ENTER)
    url = driver.current_url

    return url


def _scrap_data_from_url(url):
    '''
    The beautiful soup library finds the news tag on the site,
    and saves the first three to the list of dictionaries.
    '''
    data_from_scraping = []
    host = 'https://finance.yahoo.com' # Links to own site do not contain host
    source = requests.get(f'{url}').text
    soup = BeautifulSoup(source, features='lxml')
    for h3 in soup.find_all('h3', class_='Mb(5px)')[:3]:
        news_src = h3.find('a', class_='Fw(b) Fz(18px) Lh(23px) LineClamp(2,46px) Fz(17px)--sm1024 Lh(19px)--sm1024 LineClamp(2,38px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled')['href']
        title = h3.a.text
        if news_src[1:5] == 'news':
            news_src = host + news_src
            data_from_scraping.append({'link': news_src,
                                        'title': title,
                                        })
        else:
            data_from_scraping.append({'link': news_src,
                                        'title': title,
                                        })

    return data_from_scraping


def _make_news_csv_file(data_from_scraping, company_name):
    '''
    Saves data from a list of dictionaries to a csv file
    '''
    with open(f'downloads/{company_name} News.csv', 'w', newline='') as csv_file:
        fieldnames = ['link', 'title']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        for line in data_from_scraping:
            csv_writer.writerow(line)


def download_news(company_name):
    url = _make_url_by_company_name(company_name)
    data_from_scraping = _scrap_data_from_url(url)
    _make_news_csv_file(data_from_scraping, company_name)
