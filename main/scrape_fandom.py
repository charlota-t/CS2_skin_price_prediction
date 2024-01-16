import requests
from bs4 import BeautifulSoup
import pandas as pd

collections_years = {"Anubis Collection":2023, "Ancient Collection":2020, "Assault Collection":2013, "Aztec Collection": 2013,"Baggage Collection":2014,
                     "Bank Collection":2014, "Blacksite Collection": 2018, "Cache Collection":2014, "Canals Collection": 2019, "Cobblestone Collection":2014,
                     "Dust Collection": 2013, "Dust II Collection": 2021, "Inferno Collection": 2013, "Italy Collection": 2013, "Lake Collection": 2013,
                     "Militia Collection":2013, "Mirage Collection": 2013, "Nuke Collection": 2013, "Office Collection": 2013, "Overpass Collection": 2014, 
                     "Safehouse Collection": 2013, "St. Marc Collection":2019, "Train Collection": 2013, "Vertigo Collection": 2013, "2018 Inferno Collection":2018,
                     "2018 Nuke Collection": 2018, "2021 Dust II Collection": 2021, "2021 Mirage Collection":2021, "2021 Train Collection":2021,
                     "2021 Vertigo Collection":2021, "Chop Shop Collection":2015, "Gods and Monsters Collection":2015, "Rising Sun Collection":2015,
                     "Alpha Collection":2013, "Norse Collection": 2019, "Control Collection": 2020, "Havoc Collection": 2020, "CS:GO Weapon Case":2013,
                     "eSports 2013 Case":2013, "Operation Bravo Case":2013, "CS:GO Weapon Case 2": 2013, "Winter Offensive Weapon Case":2013, 
                     "eSports 2013 Winter Case":2013, "CS:GO Weapon Case 3": 2014, "Operation Phoenix Weapon Case": 2014, "Huntsman Weapon Case":2014,
                     "Operation Breakout Weapon Case": 2014, "eSports 2014 Summer Case":2014, "Operation Vanguard Weapon Case": 2014, "Chroma Case": 2015,
                     "Chroma 2 Case":2015, "Falchion Case": 2015, "Shadow Case":2015, "Revolver Case":2015, "Operation Wildfire Case":2016, "Chroma 3 Case":2016,
                     "Gamma Case": 2016, "Gamma 2 Case": 2016, "Glove Case": 2016, "Spectrum Case":2017, "Operation Hydra Case":2017, "Spectrum 2 Case": 2017, 
                     "Clutch Case": 2018, "Horizon Case": 2018, "Danger Zone Case": 2018, "Prisma Case":2019, "CS20 Case": 2019, "Shattered Web Case": 2019,
                     "Prisma 2 Case": 2020, "Fracture Case": 2020, "Broken Fang Case": 2020, "Snakebite Case":2021, "Operation Riptide Case": 2021, 
                     "Dreams & Nightmares Case": 2021, "Recoil Case": 2022, "Revolution Case": 2023                     
    }



        
        

def scrape():    
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
# creating the df with the corresponding column names

    df = pd.DataFrame(skins_info, columns=["Weapon type", "Skin", "Quality", "Collection"])
    df["Factory New"] = ""
    df["Minimal Wear"] = "" #create empty columns for all wear values for future use
    df["Field-Tested"] = ""
    df["Well-Worn"] = ""
    df["Battle-Scarred"] = ""
    df["Year"] = ""  # create year column to add the year of release
    for i in range(0,len(df)):  # for each row add the year of release from the dictionary above
        df.loc[i, "Year"] = collections_years[df.loc[i, "Collection"]]  # searching by key and adding the value
        
    return df  # we use return so that we can pass this variable to main
    
#print(df) if used as a unit 

