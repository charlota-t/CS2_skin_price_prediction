#prediction

import numpy as np
import pandas as pd
import sklearn 
import sklearn.datasets
from sklearn.linear_model import LinearRegression


#convert string to float
def convert_string(df, price_version): 
    price_as_float=[]
    for price in df[price_version]:
        replaced_price = price.replace("$", "")
        replaced_price = replaced_price.replace(",", "")
        splitted_price = replaced_price.split(" ")
        splitted_price = splitted_price[0]
        float_price = float(splitted_price)
        price_as_float.append(float_price)

    #replace string column by floats
    df[price_version] = pd.DataFrame(data = price_as_float)
    return df 


def predict_value(df, weapon, quality, year):
    # select rows with desired weapon 
    df_weapon = df.loc[df['Weapon_Type']] == weapon
    df_weapon.reset_index(drop = True)

    # test if there is a match with weapon type
    if df_weapon.shape[0] == 0:
        return 0, False
    
    # create a pivot table with weapon, quality and year 
    pivot = pd.pivot_table(df_weapon, values="Factory_New", index="Quality", columns="Year", aggfunc="mean", fill_value=0)

    # find the column names of the data frame
    col = (pivot.iloc[:,0])
    col_keys = col.keys()
    
    # find the column index which equals the selected column, if not found return -1
    i_found = -1
    for i in range(col_keys.size):
        if(col_keys[0]==quality):
            i_found = i
            
    # if there is a column, start regression
    if i_found>= 0:
        # find the year names in the pivot table
        row = (pivot.iloc[i_found])  
        row_keys = row.keys()

    # Convert the row with year into an array 
        x = np.asarray(row_keys)

    # Reshape row to column (transpose)
        x = x.reshape(-1,1) 

    # Convert the row with the values to an array        
        y = row.to_numpy()

    # Define the model and fit it with x & y
        model = LinearRegression().fit(x, y)

    # Predict the value for the year specified
        y_pred = model.intercept_ + model.coef_ * year

    # Test if we have a valid result
        isOk = True
        if i_found == -1 or y_pred < 0:
            isOk = False

    # return value and if we have a valid result
        return y_pred, isOk

df = pd.read_csv(r'C:\Users\charl\Downloads\allvalues2.csv', sep = ';', on_bad_lines= 'skip')
df = df.dropna()

convert_string(df, 'Factory_New')
# remove all store nan values
df = df.dropna()

df.reset_index(drop=True)

predict_value(df, 'R8 Revolver', 'Consumer Grade', 2024)
