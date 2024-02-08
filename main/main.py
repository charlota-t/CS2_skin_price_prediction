import scrape_fandom
import scrape_skin_prices as ssp

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

skins_info = scrape_fandom.scrape_fandom()  
df = scrape_fandom.build_df(skins_info)

df.to_csv("utilities/allvalues.csv", index=False)

ssp.read_all(df)

prediction.print_prediction('AK-47', 'Classified', 2024)
