import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random

#frequently updated url with the list of all skins 
url = "https://counterstrike.fandom.com/wiki/Skins/List"
request = requests.get(url)
soup = BeautifulSoup(request.text, features="html.parser")

qualities = ("common","uncommon", "rare", "mythical", "legendary","ancient") #CS2 qualities (does not inqlude knifes and gloves as they are too unpredictable in price)
not_wanted = ("Consumer Grade", "Industrial Grade", "Mil-Spec", "Restricted", "Classified","Covert" )
#CS2 weapons, does not change
all_weapons = ("Desert Eagle" , "R8 Revolver", "Dual Berettas", "Five-SeveN", "Glock-18", "P2000" ,"USP-S", "P250", "CZ75-Auto", "Tec-9", "MAG-7", "Nova" ,"Sawed-Off", "XM1014", "PP-Bizon", "MAC-10", "MP7", "MP5-SD", "MP9", "P90", "UMP-45", "AK-47" ,"AUG", "FAMAS", "Galil AR", "M4A4", "M4A1-S", "SG 553", "M249", "Negev", "AWP", "G3SG1", "SCAR-20", "SSG 08")

#creating an empty list to add the skin names scraped from the url to
list = []
#scraping the site for the skins names and removing unwanted scraped elements
items = soup.find_all("span", {"class":qualities}) 
for j in items:
    for i in j:  
        if i == "Consumer Grade":
            pass
        elif i == "Industrial Grade":
            pass
        elif i == "Mil-Spec":
            pass
        elif i == "Restricted":
            pass
        elif i == "Classified":
            pass
        elif i == "Covert":
            pass
        elif i == "x":
            pass
        elif str(i) == '<b>*</b>':
            pass
        else:
         list.append(str(i))
#converting created list into np array
skins_array = np.array(list)
#scraping the site for the weapon names
weapons = soup.find_all("a", {"title":all_weapons }) 
#creating list2 to add the weapon names scraped from the url to
list2 = []
#scraping the weapon names
for j in weapons:
    for i in j:
       list2.append(str(i)) 
#converting list2 into array
weapons_array = np.array(list2)
#creating a pd dataframe from list and list2
df = pd.DataFrame()
df['Weapon type'] = pd.Series(weapons_array)
df['Skin'] = pd.Series(skins_array)
#print(df)

#for i in df["Skin"]:
#    for j in df["Weapon type"]
#    print(j, len(j.split()), i, len(i.split()))
def create_url(name_parts, weapon_parts):
    weapon = '+'.join(weapon_parts)
    skin = '+'.join(name_parts)

    # Constructing the URL
    url = f"https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=tag_normal&appid=730&q={weapon}+%7C+{skin}"
    return url

def request_all():
    for i in range(0,len(df)):
        weapon_type = df.loc[i,"Weapon type"] 
        skin_name = df.loc[i,"Skin"]
                
        weapon_words = weapon_type.split() #spliting the weapon_type and skin_name into separate words to construct the url
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
            condition = item_name.split('(')[-1].strip(')')  # Extracting conditions
            prices = item.find_all("span", class_="sale_price") #Extracting prices
            prices_text = np.array(prices) #Creating a numpy array from the prices
            prices_clean = np.char.strip(prices_text, "\r\n\t\t\t\t\t\t") #Cleaning the exctracted values
    
            # Printing conditions and coresponding prices
            print(condition+":")
            print(prices_clean)
            #note that these are sale prices, eg an ammount that seller receives after the sale
        time.sleep(random.uniform(6,7)) #wait 6 to 7 seconds due to request rate limiter on steam market

request_all()


