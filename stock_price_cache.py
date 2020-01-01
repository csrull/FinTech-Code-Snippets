from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl, re, datetime, pandas as pd
import sqlite3, time
conn = sqlite3.connect('portfoliodb.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Price (COB DATE, Ticker VARCHAR(5), Price Numeric)')
today = datetime.date.today()
#-------Set Up--------------------------
Tickers = ('TSTL','SOLI')
#---------------------------------------
#Function that tells you whether the date passed is a business date
def is_business_day(date):
    return bool(len(pd.bdate_range(date, date)))
#Checks to find out when was the last business date if today is not a business day
def last_business_day(date):
    i=0
    while (is_business_day(today - datetime.timedelta(days = i)) == False):
        i = i+1
    return(today - datetime.timedelta(days = i))
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
#Calls the lse website to get EOD date
def EOD_Price_Call(Ticker):
    url = 'http://www.lse.co.uk/SharePrice.asp?shareprice=' + Ticker
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup('span')
    #print(soup.prettify)
    for line in tags:
        if re.search('"sp_sharePrice sp_' + Ticker + '_MID" data-field="sharePrice"',str(line)):
            return(Ticker, re.findall('([0-9]+.[0-9]+)', str(line))[0])
def UpdateDB(date):
    NoOfDBRecords = 0
    cur.execute('SELECT * FROM Price WHERE COB = ?', (date, ))
    try:
        cur.fetchone()[0]
        print('Entry in the db already exists')
    except:
        print('Inputing in the DB')
        for tick in Tickers:
            temp = EOD_Price_Call(tick)
            cur.execute('INSERT INTO Price VALUES(?, ?, ?)', (date,temp[0],temp[1]))
            print('Input',date,temp[0],temp[1])
            time.sleep(3)
        conn.commit()
#Check if today is a business days - if not determine the last business days
if (is_business_day(today) == True):
    #print('if')
    UpdateDB(today)
else:
    #use last_business_day function
    print('else')
    UpdateDB(last_business_day(today))
cur.close()
