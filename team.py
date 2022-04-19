from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from pandas import DataFrame
from datetime import timedelta, datetime

#input start Data, end Data to scrape
startDate_date = '2021-12-01'
endDate_date = '2021-12-06'

columns = ['Date', 'Team', '2021', 'Home', 'Away']
file = './teamrankings.csv'
flag = False

def getDate():
    global flag, startDate_date, endDate_date
    startDate_str = startDate_date.replace('-', '')
    startDate_str = startDate_str.replace(' ', '')
    try:
        temp_startDate = int(startDate_str)
        temp_startDate_str = startDate_str[0:4] + '-' + startDate_str[4:6] + '-' + startDate_str[6:8]
        startDate_date = datetime.strptime(temp_startDate_str, '%Y-%m-%d').date()
        if len(startDate_str) == 8:
            endDate_str = endDate_date.replace('-', '')
            endDate_str = endDate_str.replace(' ', '')
            try:
                temp_endDate = int(endDate_str)
                if len(endDate_str) == 8:
                    temp_endDate_str = endDate_str[0:4] + '-' + endDate_str[4:6] + '-' + endDate_str[6:8]
                    endDate_date = datetime.strptime(temp_endDate_str, '%Y-%m-%d').date()
                    flag = True
                else:
                    print('Wrong Date Format.\n')
                    print('Date Format example: 2021-01-01')
            except:
                print('Please input only numbers')
           
        else:
            print('Wrong Date Format.\n')
            print('Date Format example: 2021-01-01')
    except:
        print('Please input only numbers')

def scraping():
    global flag, startDate_date, endDate_date
    isData = False
    driver = webdriver.Chrome('chromedriver.exe')
    driver.maximize_window()

    while endDate_date >= startDate_date:
        scrap_date = startDate_date.strftime('%Y%m%d') #convert date to str
        scrap_url = 'https://www.teamrankings.com/ncaa-basketball/stat/three-pointers-attempted-per-game?date=' + scrap_date
        driver.get(scrap_url)
        time.sleep(2)
        source = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            table = source.find('table', {'class', 'tr-table' and 'datatable' and 'scrollable' and 'dataTable' and 'no-footer'})
            tbody = table.find('tbody')
            lists = tbody.find_all('tr')
            for list in lists:
                isData = True
                team_panel = list.find('td', {'class', 'text-left' and 'nowrap'})
                team = team_panel.find('a').text.strip()
                season = list.find_all('td', {'class', 'text-right'})[0].text.strip()
                home = list.find_all('td', {'class', 'text-right'})[3].text.strip()
                away = list.find_all('td', {'class', 'text-right'})[4].text.strip()

                c = {
                    'Date': [startDate_date],
                    'Team': [team],
                    '2021': [season],
                    'Home': [home],
                    'Away': [away]
                }

                df = DataFrame(c, columns = columns)
                if os.path.exists(file):
                    df.to_csv(file, encoding='utf-8', header=False, index=False, mode='a')
                else:
                    df.to_csv(file, encoding='utf-8', header=True, index=False)

                print(startDate_date, team, season, home, away)
        
        except:
            driver.quit()

        startDate_date += timedelta(days=1)

    if isData == True:
        print('Datas are saved succefully!')  
        driver.quit()
        flag = False

def main():
    getDate()
    if flag == True:
        scraping()

main()
