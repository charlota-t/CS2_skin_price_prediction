#Linear regression model 

import numpy as np
import pandas as pd
import sklearn 
import sklearn.datasets
from sklearn.linear_model import LinearRegression

df = pd.read_csv(r'C:\Users\charl\Downloads\allvalues2.csv', sep = ';', on_bad_lines= 'skip')

#drop rows with NaN
df = df.dropna()

#add columns to df for weapon_type and quality to give a value to the names
df.Weapon_Type = pd.Categorical(df.Weapon_Type)
df['Weapon_Code'] = df.Weapon_Type.cat.codes

df.Quality = pd.Categorical(df.Quality)
df['Quality_Code'] = df.Quality.cat.codes

#convert string to float
price_as_float=[]
for price in df.Factory_New:
    replaced_price = price.replace("$", "")
    replaced_price = replaced_price.replace(",", "")
    splitted_price = replaced_price.split(" ")
    splitted_price = splitted_price[0]
    float_price = float(splitted_price)
    price_as_float.append(float_price)

#replace string column by floats
df['Factory_New'] = pd.DataFrame(data = price_as_float)

#drop rows with NaN again
df = df.dropna()

#identify variables needed, with x(variables) and y(target)
variables = ['Weapon_Code', 'Quality_Code']
target = ['Factory_New']

#assign values to identified variables
assigned_variables = df[variables]
assigned_target = df[target]

#create linear regression model and fit it
used_model = LinearRegression().fit(assigned_variables, assigned_target)

#assign R^2 to check correlation
r_sq = used_model.score(assigned_variables, assigned_target)
print(f"R squared: {r_sq}")
