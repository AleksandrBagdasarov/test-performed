''' 
This assignment tests my skills when applying for a job.
The application collects some data from finance.yahoo.com.
For the application to work correctly, you need google chrome
or change the settings of the selenium module in the file
"download_news.py"
line 5, 6, 15, 16, 17
'''

from scrap_yahoo.download_data import download_data 
from scrap_yahoo.download_news import download_news
from scrap_yahoo.add_3day_before_change_column import add_3day_before_change_column


space = '\n'
# company_names = input(f'{space * 10}Enter The Name Separated By "," :').upper().replace('  ', ' ').split(',')
company_names = ['PD','ZUO','PINS','ZM','PVTL','DOCU','CLDR','RUN',]

def start(company_names):

    for company_name in company_names:
        company_name = company_name.strip()

        download_news(company_name)

        if download_data(company_name) != False:
            add_3day_before_change_column(company_name)


if __name__ == "__main__":
    start(company_names)


try:
    with open('errors.txt', 'r') as errors_file:
        for line in errors_file:
            print(line, end='')
except FileNotFoundError:
    print('\nSuccess')
