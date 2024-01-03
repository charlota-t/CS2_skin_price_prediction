import scrape_fandom
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import random

df = scrape_fandom.scrape()  

print(df)
df.to_csv("allvalues.csv")