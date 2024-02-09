import scrape_fandom
import scrape_skin_prices as ssp
import prediction

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random
import json
import sklearn 
import sklearn.datasets
from sklearn.linear_model import LinearRegression
from configparser import ConfigParser

config = ConfigParser()
config.read("utilities/config.ini") # reading the config file 
config_data = config["USER"] 
have_csv = config_data["have_csv"]  # selecting file creation mode or prediction mode

if have_csv == "False":  # if USER does not have the csv file with the data this calls the coresponding module and creates the data file
    skins_info = scrape_fandom.scrape_fandom()  
    df = scrape_fandom.build_df(skins_info)

    df.to_csv("utilities/allvalues.csv", index=False)
    
    ssp.read_all(df)
elif have_csv == "True": 
    weapon = config_data["Weapon"]  # reading the coresponding data from the config file
    quality = config_data["Quality"]
    year = int(config_data["Year"])
    prediction.print_prediction(weapon = weapon, quality = quality, year = year)  # predictiong according the selected data
