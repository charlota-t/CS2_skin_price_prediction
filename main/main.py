import scrape_fandom
import scrape_skin_prices as ssp
import scrape_skin_prices_modules as sspm
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random
import json

skins_info = scrape_fandom.scrape_fandom()  
df = scrape_fandom.build_df(skins_info)

df.to_csv("allvalues.csv", index=False)

sspm.read_all(df)
#ssp.request_all(df)