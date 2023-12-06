import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

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
print(df)

