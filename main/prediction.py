#prediction

import numpy as np
import pandas as pd
import sklearn 
import sklearn.datasets
from sklearn.linear_model import LinearRegression

pd.options.mode.chained_assignment = None  # default = 'warn'

#convert string to float
def convert_string(df, price_version): 
    price_as_float = []
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

def predict_price_value(df, price_version, weapon, quality, year):

    # set default predicted price 
    y_pred = 0

    # create local copy
    df_local = df.copy()
    
    # convert strings
    df_local = df.dropna()
    convert_string(df_local, price_version)
    
    # select rows with desired weapon 
    df_weapon = df_local.loc[df_local['Weapon type'] == weapon]
    df_weapon.reset_index(drop = True)

    # test if there is a match with weapon type
    if df_weapon.shape[0] == 0:
        return y_pred, False
    
    # create a pivot table with weapon, quality and year 
    if(quality == 'All'):
        pivot = pd.pivot_table(df_weapon, values = price_version, index = None, columns = "Year", aggfunc = "mean", fill_value = 0)
        quality = price_version
    else:    
        pivot = pd.pivot_table(df_weapon, values = price_version, index = "Quality", columns = "Year", aggfunc = "mean", fill_value = 0)

    # find the column names of the data frame
    col = (pivot.iloc[:,0])
    col_keys = col.keys()
    
    # find the column index which equals the selected column, if not found return -1
    i_found = -1
    for i in range(col_keys.size):
        if(col_keys[i] == quality):
            i_found = i
            
    # if there is a column, start regression
    if i_found >= 0:
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

    # test if we have a valid result
    isOk = True
    if i_found == -1 or y_pred < 0:
        isOk = False

    # For testing only
    print('Weapon type: ', weapon)
    print('Quality; ', quality)
    if(isOk):
        print('Predicted price: ', y_pred)
    else:
        print('No prediction possible')

    # return value and if we have a valid result
    return y_pred, isOk

df = pd.read_csv(r'C:\Users\charl\Downloads\allvalues2.csv', sep = ';', on_bad_lines= 'skip')

predicted_price, isOk=predict_price_value(df, 'Factory New', 'AK-47', 'All', 2024)

predicted_price, isOk=predict_price_value(df, 'Factory New', 'AK-47', 'Consumer Grade', 2024)

predicted_price, isOk=predict_price_value(df, 'Factory New', 'AK-47', 'Classified', 2024)
