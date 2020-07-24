from datetime import datetime
import requests
import time
import traceback


def _get_first_trade_in_seconds(company_name):
    ''' 
    Getting information about the date
    of the first trade from json object.
    '''
    first_trade_date_url = f'https://query2.finance.yahoo.com/v7/finance/quote?formatted=true&crumb=%2FzVJpzZBXoL&lang=en-US&region=US&symbols={company_name}&fields=messageBoardId%2ClongName%2CshortName%2CmarketCap%2CunderlyingSymbol%2CunderlyingExchangeSymbol%2CheadSymbolAsString%2CregularMarketPrice%2CregularMarketChange%2CregularMarketChangePercent%2CregularMarketVolume%2Cuuid%2CregularMarketOpen%2CfiftyTwoWeekLow%2CfiftyTwoWeekHigh%2CtoCurrency%2CfromCurrency%2CtoExchange%2CfromExchange&corsDomain=finance.yahoo.com'
    response = requests.get(first_trade_date_url)
    json_response = response.json()
    try:
        first_trade_date_in_seconds = (json_response['quoteResponse']['result'][-1]['firstTradeDateMilliseconds']) // 1000
        return first_trade_date_in_seconds
    except Exception:
        # Something is wrong? Make sure the company name is correct and there is historical data for it.
        with open('errors.txt', 'a') as errors_file:
            errors_file.write(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -> {company_name}\n{traceback.format_exc()}')
            errors_file.write('Something is wrong, make sure the company name is correct and there is historical data for it.')

        return False

    
def _download_csv_file(first_trade_date_in_seconds, company_name):
    ''' 
    The function downloads a file with data
    for the period from the specified time to today.
    '''
    # Maximum period specified
    utc_now_in_seconds = int(time.mktime(datetime.utcnow().timetuple()))
    download_history_urls = f'https://query1.finance.yahoo.com/v7/finance/download/PD?period1={first_trade_date_in_seconds}&period2={utc_now_in_seconds}&interval=1d&events=history'
    r = requests.get(download_history_urls)
    with open(f'downloads/{company_name}.csv', 'wb') as csv_file:
        csv_file.write(r.content)


def download_data(company_name):
    first_trade_date_in_seconds = _get_first_trade_in_seconds(company_name)
    if first_trade_date_in_seconds == False:
        return False
    else:
        _download_csv_file(first_trade_date_in_seconds, company_name)
        