# Python Imports
from bs4 import BeautifulSoup
import requests
import csv
import re
import datetime


def get_hanary_hub_gas_prices(url, interval):
    """
        Function takes two parameters
        First parameter is url, where data needed to parsed
        Second parameter decides wheather it is monthly data or daily data
        
        Function return list of natural gas prices records

    """
    page = requests.get(url)
    page_text = BeautifulSoup(page.text, 'html.parser')
    records = []
    table_element = 'B4|B3'
    if interval == 'daily':
        table_element = 'B6|B3'
    print('Getting ' + interval + ' data.')

    for txt in page_text.find_all('td'):
        x = re.findall(table_element, str(txt))
        if x:
            records.append(txt)
    return records


def create_gas_prices_csv_file(file_name, records, interval):
    """
        Function takes three parameters
        First parameter is file_name, where data needed to write
        Second parameter contains data to be written
        Third parameter decides wheather it is monthly data or daily data
    """
    with open(file_name,'w') as gas_price:
        field_name = ['date', 'price']
        writer = csv.DictWriter(gas_price, fieldnames = field_name)
        writer.writeheader()
        columns_to_parse = 13
        if interval == "daily":
            columns_to_parse = 6
        print('Writing ' + interval + ' data in ' + file_name)
        for colomn in range(0, len(records), columns_to_parse):
            if interval == 'monthly':
                raw_year = records[colomn].contents[0]
                year = int(raw_year[-4:])
                for i in range(1, columns_to_parse):
                    month = datetime.date(year, i, 1)
                    date_to_insert = month.strftime("%Y-%b-%d")
                    if records[colomn+i].contents:
                        writer.writerow({'date':date_to_insert, 'price':records[colomn+i].contents[0]})
                    else:
                        writer.writerow({'date':date_to_insert, 'price':''})
            else:
                date_interval = (records[colomn].contents[0]).split('to')
                start_date = date_interval[0].split()
                raw_year = start_date[0]
                year = raw_year[-4:]
                if len(start_date) == 3:
                    month = start_date[1][0:len(start_date[1])-1]
                    day = int(start_date[2])
                else:
                    start_date = start_date[1].split('-')
                    month = start_date[0]
                    day = int(start_date[1])
                date_str = year + "-" + month + "-" + str(day)
                date = datetime.datetime.strptime(date_str, "%Y-%b-%d")
                for i in range(1, columns_to_parse):
                    date_to_insert = date.strftime("%Y-%b-%d")
                    if records[colomn+i].contents:
                        writer.writerow({'date':date_to_insert, 'price':records[colomn+i].contents[0]})
                    else:
                        writer.writerow({'date':date_to_insert, 'price':''})
                    date += datetime.timedelta(days = 1)
    print('Done')