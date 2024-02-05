import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
      
def scrape_fandom():   
#frequently updated website with all weapon skin names
    url = "https://counterstrike.fandom.com/wiki/Skins/List"
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features="html.parser")
    all_tables = soup.find_all("table", class_="wikitable") #we search for tables in the website as they contain all the info we need
    
    current_collection = "NaN"  # if we are not able to find the collection
    skins_info = [] # initializing skins_info
    for i in all_tables: 
    # find collection name above the table
        last_span = i.find_previous("span", class_="mw-headline")
        if last_span:
            current_collection = last_span.text.strip() 

        rows = i.find_all("tr")
        for j in rows[1:]:
            columns = j.find_all(["td", "th"])
            if len(columns) >= 3:  # making sure we only take valid rows
                skin_name = columns[1].get_text(strip=True)
                quality = columns[2].get_text(strip=True)
                weapon_type = columns[0].get_text(strip=True)
                skins_info.append([weapon_type, skin_name, quality, current_collection])
    return skins_info
    

def build_df(skins_info):
# creating the df with the corresponding column names
    with open('collection_dict.json') as json_file:
        collections_years = json.load(json_file) 
    df = pd.DataFrame(skins_info, columns=["Weapon type", "Skin", "Quality", "Collection"])
    df["Factory New"] = np.NaN
    df["Minimal Wear"] = np.NaN  # create empty columns for all wear values for future use
    df["Field-Tested"] = np.NaN
    df["Well-Worn"] = np.NaN
    df["Battle-Scarred"] = np.NaN
    df["Year"] = np.NaN  # create year column to add the year of release
    for i in range(0,len(df)):  # for each row add the year of release from the dictionary above
        df.loc[i, "Year"] = collections_years[df.loc[i, "Collection"]]  # searching by key and adding the value
   # df.merge(collection_df, on = "Collection", how = "left")
    return df  # we use return so that we can pass this variable to main
    
