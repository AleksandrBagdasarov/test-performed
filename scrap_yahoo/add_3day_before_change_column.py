import csv
import datetime
import traceback

def _calculate_new_column(company_name):
    ''' 
    This function reads the file line by line, creating a dictionary, and a list of dictionaries.
    The dictionary is needed to calculate the new column.
    The list of dictionaries is processed by the file writing function.
    '''
    data_from_file = []
    date_and_close_values_from_file = {}

    three_days = datetime.timedelta(days=3)

    with open(f'downloads/{company_name}.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for row in reader:
            try:
                date_key = datetime.datetime.strptime(row['Date'].replace('-',''), '%Y%m%d').date() - three_days
                date_and_close_values_from_file[row['Date']] = row['Close']
                if str(date_key) in date_and_close_values_from_file:
                    _3day_before_change = float(row['Close']) / float(date_and_close_values_from_file[str(date_key)])
                    data_from_file.append({'Date': row['Date'],
                                            'Open': row['Open'],
                                            'High': row['High'],
                                            'Low': row['Low'],
                                            'Close': row['Close'],
                                            'Adj Close': row['Adj Close'],
                                            'Volume': row['Volume'],
                                            '3day_before_change': _3day_before_change,})
                else:
                    _3day_before_change = '-'
                    data_from_file.append({'Date': row['Date'],
                                            'Open': row['Open'],
                                            'High': row['High'],
                                            'Low': row['Low'],
                                            'Close': row['Close'],
                                            'Adj Close': row['Adj Close'],
                                            'Volume': row['Volume'],
                                            '3day_before_change': _3day_before_change,})
            except Exception:
                with open('errors.txt', 'a') as errors_file:
                    errors_file.write(f'\n\n{company_name}\n{traceback.format_exc()}')

        return data_from_file


def _open_csv_and_write_new_data(company_name, data_from_file):
    ''' 
    The function writes a list of dictionaries to a file.
    Each dictionary is a new line.
    '''
    with open(f'downloads/{company_name}.csv', 'w', newline='') as csv_file:
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', '3day_before_change']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        for line in data_from_file:
            csv_writer.writerow(line)


def add_3day_before_change_column(company_name):
    data_from_file = _calculate_new_column(company_name)
    _open_csv_and_write_new_data(company_name, data_from_file)
