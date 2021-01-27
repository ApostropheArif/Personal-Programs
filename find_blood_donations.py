#! python3

"""
Author: ApostropheArif
Created on Fri Jan  8 16:24:27 2021

This is a program to check Pusat Darah Negara's blood donation campaigns.
As the campaign calendar is updated weekly, the program will only retrieve the campaigns within the current week.
Users need to input the location of interest and any hits will be displayed.

"""
       
import bs4, datetime, requests, tabulate
import pandas as pd

print("Check this week's blood donation campaigns. Jom derma darah!".center(70, '-'))
event_id = 4414 # 4414 is the event ID on January 1, 2021. The ID is used to generate the URLs of the campaign calendars.
months = {1:'Januari', 2:'Februari', 3:'Mac', 4:'April', 5:'Mei', 6:'Jun', 
          7:'Julai', 8:'Ogos', 9:'September', 10:'Oktober', 11:'November', 12:'Disember'}

today = datetime.datetime.today()
weekstart = today - datetime.timedelta(today.weekday()) # today.weekday() returns an integer with 0 representing Monday and so on
weekend = weekstart + datetime.timedelta(6)

weekstart_text = f'{weekstart.day} {months[weekstart.month]} {weekstart.year}'
weekend_text = f'{weekend.day} {months[weekend.month]} {weekend.year}'

lookup_area = input('Please enter the area that you want to check: ')
print(f'''\nThank you. Please wait while the program checks. 
Any donation campaigns being held in {lookup_area} within this week will be displayed below:\n''')

pull_campaign_info_flag = False # Used to control retrieving information from the web pages
while True:
    url = f'http://pdn.gov.my/index.php?option=com_jevents&task=icalrepeat.detail&evid={event_id}'
    
    try:
        res = requests.get(url)
    except ConnectionError:
        print('The URL provided is not valid. Please try again.')
        
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    campaign_date = soup.select('.repeat') # CSS selector to capture date information
    
    if campaign_date: # campaign_date will not be True if the selection was unsuccessful        
        if weekstart_text in campaign_date[0].text:
            pull_campaign_info_flag = True
        
        if pull_campaign_info_flag:
            table = pd.read_html(url, attrs={'id':'dgMobRoster'}) # read_html returns a list of DataFrames. Since we have specified the table ID, the list contains only 1 DataFrame.
            table = table[0] # Converting the variable to a DataFrame
            campaigns = table[table['Lokasi Derma Darah'].str.contains(lookup_area.upper())]
            
            if len(campaigns)>0:
                print(campaign_date[0].text)
                campaigns = campaigns[['Penganjur', 'Lokasi Derma Darah', 'Waktu Mula', 'Waktu Tamat']]
                campaigns['Lokasi Derma Darah'] = campaigns['Lokasi Derma Darah'].str.wrap(50)
                print(tabulate.tabulate(campaigns, headers='keys', tablefmt='pretty', showindex=False))
            
        if weekend_text in campaign_date[0].text:
            break
       
    event_id+=1
    
print("That's all folks!")