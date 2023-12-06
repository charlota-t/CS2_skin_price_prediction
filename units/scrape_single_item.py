import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
#creating an empty array for the price converter to append to
array = []
def converter(file):  #note that one singular formating can't be used for all currencies because each of them is formated differently
    for j in file:
        for i in j:
            if i.startswith("$") & i.endswith("USD"):
                i = i.replace("$", "")
                i = i.replace("USD", "")
                i = float(i)
                print("$",round(i,2),"USD")
            elif i.endswith("₴"):
                i = i.replace("₴" , "")
                i = i.replace(",", ".")
                i = i.replace(" ", "")
                i = float(i)
                i = i*0.027429796
                print("$",round(i,2),"USD")
            elif i.startswith("¥ "):
                i = i.replace("¥ ", "")
                i = i.replace(",", "")
                i = float(i)
                y = i*0.006756441
                i = i*0.14055287
                print("$",round(i,2),"USD or", round(y,2),"USD")
            elif i.startswith("₩ "):
                i = i.replace("₩ ", "")
                i = i.replace(",", "")
                i = float(i)
                i = i*0.00076791519
                print("$",round(i,2),"USD")         
            elif i.startswith("CHF "):
                i = i.replace("CHF ", "")
                i = i.replace("--","00")
                i = float(i)
                i = i*1.1448816
                print("$",round(i,2),"USD")     
            elif i.endswith("₸"):
                i = i.replace("₸","")
                i = i.replace(",", ".")
                i = i.replace(" ", "")
                i = float(i)
                i = i*0.0021677483
                print("$",round(i,2),"USD")  
            elif i.endswith("pуб."):
                i = i.replace("pуб.","")
                i = i.replace(",", ".")
                i = float(i)
                i = i*0.011110017
                print("$",round(i,2),"USD")  
            elif i.endswith("€"):
                i = i.replace("€","")
                i = i.replace(",", ".")
                i = i.replace("--","00")
                i = float(i)
                i = i*1.0900791
                print("$",round(i,2),"USD") 
            elif i.startswith("£"):
                i = i.replace("£", "")
                i = float(i)
                i = i*1.2644539
                print("$",round(i,2),"USD")
            elif i.startswith("฿"):
                i = i.replace("฿", "")
                i = float(i)
                i = i*0.028504166
                print("$",round(i,2),"USD")
            elif i.endswith("₫"):
                i = i.replace("₫","")
                i = i.replace(".", "")
                i = float(i)
                i = i*0.000041200184
                print("$",round(i,2),"USD")
            elif i.startswith("₹ "):
                i = i.replace("₹ ", "")
                i = i.replace(",", "")
                i = float(i)
                i = i*0.012000527
                print("$",round(i,2),"USD")
            elif i.endswith(" TL"):
                i = i.replace(" TL","")
                i = i.replace(".", "")
                i = i.replace(",", ".")
                i = float(i)
                i = i*0.03459303
                print("$",round(i,2),"USD")
            elif i.startswith("CDN$ "):
                i = i.replace("CDN$ ", "")
                i = float(i)
                i = i*0.7392775
                print("$",round(i,2),"USD")
            elif i.endswith(" kr"):
                i = i.replace(" kr","")
                i = i.replace(".", "")
                i = i.replace(",", ".")
                i = float(i)
                i = i*0.095753654
                print("$",round(i,2),"USD")
            elif i.startswith("A$ "):
                i = i.replace("A$ ","")
                i = float(i)
                i = i*0.66183303
                print("$",round(i,2),"USD")
            elif i.startswith("R$ "):
                i = i.replace("R$ ","")
                i = i.replace(",",".")
                i = float(i)
                i = i*0.20316714
                print("$",round(i,2),"USD")
            else:
                print("I don't know that yet")
        global array        
        array= np.append(array,i) #appending the result of price conversion into a np array


url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Blue%20Laminate%20%28Factory%20New%29" 
#note that the url includes the name of the skin and is not randomly generated which means that if we have all the skin names we can search each of them

#scraping the prices from the steam market
request = requests.get(url)
soup = BeautifulSoup(request.text, features="html.parser")
prices = soup.find_all("span", {"class":"market_listing_price_with_fee" })
prices_text = np.array(prices)
prices_clean = np.char.strip(prices_text, "\r\n\t\t\t\t\t\t")

#using the above creatid price converter on the prices scraped from the steam market
converter(prices_clean)