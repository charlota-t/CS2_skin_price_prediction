import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random

def scrape():
    url = "https://counterstrike.fandom.com/wiki/Skins/List"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="html.parser")
    all_tables = soup.find_all("table", class_="wikitable") #we search for tables in the website as they contain all the info we need

    current_collection = "NaN"  #if we are not able to find the collection
    skins_info = [] #initializing skins_info
    for i in all_tables: 
    # find collection name above the table
        last_span = i.find_previous("span", class_="mw-headline")
        if last_span:
            current_collection = last_span.text.strip() 

        rows = i.find_all("tr")
        for j in rows[1:]: #skipping the first row as it contains the header of the table
            columns = j.find_all(["td", "th"])
            if len(columns) >= 3: #making sure we only take valid rows
                skin_name = columns[1].get_text(strip=True) 
                quality = columns[2].get_text(strip=True)
                weapon_type = columns[0].get_text(strip=True)
                skins_info.append([weapon_type, skin_name, quality, current_collection])
#creating the df with the corresponding column names
    global df
    df = pd.DataFrame(skins_info, columns=["Weapon type", "Skin", "Quality", "Collection"])
scrape()

def create_url(name_parts, weapon_parts): #creating a function to build the url from the information in the dataframe
    weapon = '+'.join(weapon_parts) #joining name_parts and weapon_parts with a + symbol which is needed for the url
    skin = '+'.join(name_parts)

    # Constructing the URL
    url = f"https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=tag_normal&appid=730&q={weapon}+%7C+{skin}"
    return url

def request_all():
    for i in range(0,len(df)):
        weapon_type = df.loc[i,"Weapon type"] 
        skin_name = df.loc[i,"Skin"]
        #spliting the weapon_type and skin_name into separate words to construct the url        
        weapon_words = weapon_type.split() 
        skin_words = skin_name.split() 
        

        # Constructing URL based on the number of words
        url = create_url(skin_words, weapon_words)
        print(url)
        #Scraping the prices and conditions from the Steam market
        request = requests.get(url)
        soup = BeautifulSoup(request.text, features="html.parser")

        items = soup.find_all("div", class_="market_listing_row")
        for item in items:
            item_name = item.find("span", class_="market_listing_item_name").get_text(strip=True) 
            condition = item_name.split("(")[-1].strip(")")  # extracting conditions 
            prices = item.find_all("span", class_="sale_price") #extracting prices for all conditions at once which saves us requests
            prices_text = np.array(prices) #creating a numpy array from the prices
            prices_clean = np.char.strip(prices_text, "\r\n\t\t\t\t\t\t") #Cleaning the exctracted values
    
            # Printing conditions and coresponding prices
            print(condition+":")
            print(prices_clean)
            #note that these are sale prices, eg an ammount that seller receives after the sale
        time.sleep(random.uniform(8,9)) #wait 8 to 9 seconds due to request rate limiter on steam market

request_all()