#tree model

import numpy as np
import pandas as pd
import sklearn 
import sklearn.datasets
from sklearn import tree
from sklearn.model_selection import train_test_split

df = pd.read_csv(r"utilities/allvalues.csv", sep = ';', on_bad_lines= 'skip')

#add weights to the quality type, the less frequent, the rarer the quality
count_quality = df['Quality'].count()
value_count_quality = df['Quality'].value_counts()
weights_quality = value_count_quality / count_quality 
df['Weights_quality'] = df['Quality'].map(weights_quality)

count_weapons = df['Weapon_Type'].count()
value_count_weapons = df['Weapon_Type'].value_counts()
weights_weapon = value_count_weapons / count_weapons
df['Weights_weapon'] = df['Weapon_Type'].map(weights_weapon)  

#convert string to float
def convert_string(df): 
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
    return df 

def test_mode(df):
    #Define a parameter to get into test mode 
    isTest = False

    #For testing, select small number of rows
    if(isTest):
        df=df.head(20)
        print(df)

# define tree model
def tree_model(df):
    #identify variables needed, with x(variables) and y(target)
    variables = ['Weights_weapon', 'Weights_quality', 'Year']
    target = ['Factory_New']

    #assign values to identified variables
    tree_variables = df[variables]
    tree_target = df[target]

    #assign train and test variables
    x_train, x_test, y_train, y_test = train_test_split(tree_variables, tree_target, test_size=0.2)

    #Define and train tree regressor
    regression_tree = tree.DecisionTreeRegressor(max_depth=3)
    regression_tree.fit(x_train, y_train)

    #Define and print R^2 for train set
    R_squared_train = regression_tree.score(x_train, y_train)
    print('R^2 train set =', R_squared_train)

    #Define and print R^2 for test set
    R_squared_test = regression_tree.score(x_test, y_test)
    print('R^2 test set =', R_squared_test)

    #Predict and print the y value for x in test set
    y_predict = regression_tree.predict(x_test)
    print('predicted y value for x =', y_predict)

#drop rows with NaN
df = df.dropna()
#print(df.head(20))
convert_string(df)
#drop rows with NaN again
df = df.dropna()
test_mode(df)
tree_model(df)



