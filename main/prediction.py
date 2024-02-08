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

def create_pivot_table(df, price_version, weapon, quality):

    # create local copy and drop NaN values
    df_local = df.copy()
    df_local = df_local.dropna()

    convert_string(df_local, price_version)

    # remove all store nan values
    df_local = df_local.dropna()
    df_local.reset_index(drop=True)
    
    # select rows with desired weapon 
    df_weapon = df_local.loc[df_local['Weapon type'] == weapon]
    df_weapon.reset_index(drop = True)

    # test if there is a match with weapon type
    if df_weapon.shape[0] == 0:
        return y_pred, False
    
    # create a pivot table with weapon, quality and year 
    quality_name_in_pivot = quality
    if(quality == 'All'):
        pivot = pd.pivot_table(df_weapon, values = price_version, index = None, columns = "Year", aggfunc = "mean", fill_value = 0)
        quality_name_in_pivot = price_version
    else:    
        pivot = pd.pivot_table(df_weapon, values = price_version, index = "Quality", columns = "Year", aggfunc = "mean", fill_value = 0)

    return pivot, quality_name_in_pivot

def predict_y(df, price_version, weapon, quality, year):
    y_pred = 0
    pivot, quality_name_in_pivot = create_pivot_table(df, price_version, weapon, quality)

    # find the column names of the data frame
    col = (pivot.iloc[:,0])
    col_keys = col.keys()

    # find the column index which equals the selected column, if not found return -1
    i_found = -1
    for i in range(col_keys.size):
        if(col_keys[i] == quality_name_in_pivot):
            i_found = i
            
    # if there is a column, start regression
    if i_found >= 0:
        # find the year names in the pivot table
        row = (pivot.iloc[i_found])  
        row_keys = row.keys()
 
        x = np.asarray(row_keys)
        x = x.reshape(-1,1)        
        y = row.to_numpy()

    # Define the model and fit it with x & y
        model = LinearRegression().fit(x, y)

    # Predict the value for the year specified
        y_pred = model.intercept_ + model.coef_ * year

    # test if there is a valid result
    is_ok = True
    if i_found == -1 or y_pred < 0:
        is_ok = False

    # return value and if we have a valid result
    return y_pred, is_ok

def print_prediction(df, weapon, quality, year):
    column_name = list(df)
    # print price for all 5 different prices 
    for column in column_name[4:]:
        if column != 'Year':
            y_pred, is_ok = predict_y(df, column, weapon, quality, year)
            print(f'For the {column} price, weapon type {weapon} and quality {quality},')
            if(is_ok): # check if there is a valid result
                print(f'the predicted price for year {year} is: ', y_pred)
            else:
                print('there is no prediction possible')
        else:
            break 

df = pd.read_csv(main/utilities/allvalues.csv, sep = ';', on_bad_lines= 'skip')

print_prediction(df, 'USP-S', 'All', 2024)


