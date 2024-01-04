import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():    
#frequently updated website with all weapon skin names
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
        for j in rows[1:]:
            columns = j.find_all(["td", "th"])
            if len(columns) >= 3: #making sure we only take valid rows
                skin_name = columns[1].get_text(strip=True)
                quality = columns[2].get_text(strip=True)
                weapon_type = columns[0].get_text(strip=True)
                skins_info.append([weapon_type, skin_name, quality, current_collection])
#creating the df with the corresponding column names

    df = pd.DataFrame(skins_info, columns=["Weapon type", "Skin", "Quality", "Collection"])
    df["Factory New"] = ""
    df["Minimal Wear"] = "" #create empty columns for all wear values for future use
    df["Field-Tested"] = ""
    df["Well-Worn"] = ""
    df["Battle-Scarred"] = ""
    return(df) #we use return so that we can pass this variable to main
#print(df) if used as a unit 