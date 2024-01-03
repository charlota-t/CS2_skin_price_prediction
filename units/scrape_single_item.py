import requests
from bs4 import BeautifulSoup
import numpy as np

def scrape_item(name_part1,name_part2, weapon): #creating a function for scraping a item from the steam market with variables
    url = "https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Quality%5B%5D=tag_normal&appid=730&q="+str(weapon)+"+%7C+"+str(name_part1)+"+"+str(name_part2)

    # Scraping the prices and conditions from the Steam market
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
    
scrape_item("blue","laminate","ak-47")