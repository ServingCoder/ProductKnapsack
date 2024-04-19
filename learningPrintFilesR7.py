# parse csv file with csv library
import csv
# get os direcotry with os library
import os
# read csv file with pandas library
import pandas as pd

def learningPandasTest(csv_file):
    ''' 
        A function that demos basic Pandas functions for changing data
        inputs: csv_file, a csv file
               columns_of_intrest: an array of strings coresponding to the names of the
                                   columns you want to run the test on
        outputs: none, operations done in place
    '''
    sub_csv = csv_file
    getTop10(sub_csv)
    getInfo(sub_csv)
    print('-----------------')
    print('Altering our dataset')
    sub_csv.loc[[1,3,5], 'MRPNum'] = 'missing'
    getTop10(sub_csv)
    getInfo(sub_csv)
    print('-----------------')
    print('Convert the word "missing" back to a number')
    # catch the errors with coerce
    sub_csv['MRPNum'] = pd.to_numeric(sub_csv['MRPNum'], errors='coerce')
    getTop10(sub_csv)
    getInfo(sub_csv)
    # side note, you can also ask to downcast to smallest type using to_numeric
    # you can gain performance by storing a float32 instead of float64
    # especially when working with large datasets

def getInfo(csv_file):
    ''' 
        A function that prints the data types of your dataset
        inputs: csv_file, a csv file
    '''
    print('-----------------')
    print('Info of our dataset')
    print(csv_file.dtypes)
    # an optional function that provides info on your data
    # print(my_csv.info())

def getTop10(csv_file):
    ''' 
        A function that prints the first 10 rosws of your dataset
        inputs: csv_file, a csv file
    '''
    print('-----------------')
    print('First 10 elements of dataset')
    print(csv_file.head(10))

def centsToDollarsCSV(csv_file, convert_column):
    ''' 
        A function that converts a column of data from cents to dollars
        inputs: csv_file, a csv file
        columns_of_intrest: an array of strings coresponding to the names of the
                                   columns you want to run the conversion on
    '''
    # note: working with series means changing on a per column basis
    #       working on a dataset means you change the whole thing
    #       a column in a dataFrame is a pandasSeries object
    sub_csv = csv_file[convert_column]
    # you do not need to call centsToDollars(), remove brakets
    sub_csv = sub_csv.apply(centsToDollars)
    return sub_csv

def centsToDollars(value):
    ''' 
        A function that converts a singluar piece of data from cents to dollars
        inputs: value, the value being converted
        output: value, the convereted value
    '''
    value = value/100
    return value

def getCSVFile(path):
    ''' 
        A function returns the pandas DataFile of the provided CSV file
        inputs: name of .csv file in current directory
        output: panda object
    '''
    return pd.read_csv(path)

def main():
    # get the csv file
    file_path = "FashionDataset.csv"
    # create a pandas DataFrame using the csv file
    my_csv = getCSVFile(file_path)
    getTop10(my_csv)
    # specify the column
    MRP_col = 'MRPNum'
    # perfom cents to dollar conversion on column of data
    my_csv[MRP_col] = centsToDollarsCSV(my_csv, MRP_col)
    Discount_col = 'SellPrice'
    # perfom cents to dollar conversion on column of data
    my_csv[Discount_col] = centsToDollarsCSV(my_csv, Discount_col)
    #repeat this process again to change Nan to 0
    #next, create 
    getTop10(my_csv[MRP_col])
    getTop10(my_csv[Discount_col])
    #getInfo((my_csv[column_of_interest]))

    budget = float(input("Type in your budget i.e 30: "))
    #collect all products that are normally in the budget, or that after applying the max possible discount they are within the budget
    in_budget_products = my_csv[(my_csv[MRP_col] < budget) | ((my_csv[MRP_col] > budget) & (my_csv[Discount_col] < budget))]
    getTop10(in_budget_products[MRP_col])
    getTop10(in_budget_products[Discount_col])
    



main()


# Convert the column 'SellPrince' from string to float
#sub_csv['SellPrice'] = sub_csv['SellPrice'].astype(float)
# convert cents into dollarse
#sub_csv['SellPrice'] = sub_csv['SellPrice']/100
#print(sub_csv.head(10))
#print(old_data)
#print(type(old_data))

#float(sub_csv['SellPrice'])/100
#print(sub_csv.head(10))
