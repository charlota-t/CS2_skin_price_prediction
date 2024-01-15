import scrape_fandom
import scrape_skin_prices as ssp
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random

df = scrape_fandom.scrape()  

df.to_csv("allvalues.csv", index=False)

ssp.request_all(df)