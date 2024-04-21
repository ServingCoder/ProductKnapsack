# parse csv file with csv library
import csv
# get os direcotry with os library
import os
# read csv file with pandas library
import pandas as pd
# use numpy select with numpy library
import numpy as np

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

def convertCSVCenttoDollar(csvFile):
    ''' 
        A function what changes two columns,  MRPNum and SellPrice, from cents to dollars.
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # specify the Sell Price column with applied discounts
    MRP_col = "MRPNum"
    Discount_col = "SellPrice"
    # perfom cents to dollar conversion on column of data
    csvFile[MRP_col] = centsToDollarsCSV(csvFile, MRP_col)
    # perfom cents to dollar conversion on column of data
    csvFile[Discount_col] = centsToDollarsCSV(csvFile, Discount_col)
    return csvFile

def productsInBudgetCSV(csvFile):
    ''' 
        A function that returns a DataFrame of products within the customer's budget
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # obtain budget from the user
    budget = float(input("Type in your budget i.e 30: "))
    # specify the Sell Price column to compare discounts
    MRP_col = "MRPNum"
    Discount_col = "SellPrice"
    # collect all products that are normally in the budget, or that after applying the max possible discount they are within the budget
    in_budget_products = csvFile[(csvFile[MRP_col] <= budget) | (csvFile[Discount_col] < budget)]
    # save to a new csv file
    #in_budget_products.to_csv('FashionDatasetChanged.csv', header=True, index=True)
    return in_budget_products, budget

def optimizedDiscountCSV(csvFile, budget):
    ''' 
        A function that creates a new column in the DataFrame OPTDiscountPercentOff
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # Given in_budget_products
    #       Make a new PriceCol if Price is already over Budget
    #       if SellPrice = MRP(DiscountPercentOff)
    #       then Budget/MRP = OPTDiscountPercentOff
    #       and KnapSackPrice = MRP*OPTDiscountPercentOff
    #       but then all KnapSackPrices will be the budget price
    #       so just make them all the budget price
    MRP_col = "MRPNum"
    OPTDiscount_col = "inBudgetPrice"
    # create a list of conditions 
    #conditions = [
    #    csvFile[MRP_col] <= budget,
    #    csvFile[MRP_col] > budget
    #]
    # create a list of the valyes we want to assign for each condition
    # if already in budget, keep the price, else, make it the max budget
   # values = [csvFile[MRP_col], budget]
    # perfom cents to dollar conversion on column of data
    #csvFile[OPTDiscount_col] = np.select(conditions, values, default=np.nan)
    csvFile.loc[csvFile[MRP_col] <= budget, OPTDiscount_col] = csvFile[MRP_col]
    csvFile.loc[csvFile[MRP_col] > budget, OPTDiscount_col] = budget
    return csvFile

def createCustomerValueCSV(csvFile, category_list, value_list):
    ''' 
        A function that creates a new column in the DataFrame of product value
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    productValue = "CustomerValue"
    category_col = "Category"
    # create a list of conditions 
    for i in range(len(category_list)):
        #condition = [
        #    csvFile[category_col] == category_list[i]
        #]
        # create a list of the valyes we want to assign for each condition
        #value = [value_list[i]]
        # Update values in the 'productValue' column based on the condition
        csvFile.loc[csvFile[category_col] == category_list[i], productValue] = value_list[i]
        #csvFile[productValue] = np.where(condition, value, csvFile[productValue])

    return csvFile


def customerValueCSV(csvFile, budget):
    ''' 
        A collects the data to creates a new column in the DataFrame of product value, then calls the function that dose it
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # obtain all categoy of products in the budget
    category_col = "Category"
    unique_categories = list(csvFile[category_col].unique())
    print("There are "+str(len(unique_categories))+" categories of products in your budget.")
    # present the categories to the user
    print("The "+str(len(unique_categories))+" categories are:")
    for i in range(len(unique_categories)):
        print("\t"+unique_categories[i])
    # obtain the customer percived value per category
    print("Please input a unique ranking [1, "+str(len(unique_categories))+"] meaning [I don't like, I like] for each category:")
    unique_category_values = []
    for i in range(len(unique_categories)):
        value = input(unique_categories[i]+" :")
        # store the value
        unique_category_values.append(int(value))
    # create new column of data with value info
    csvFile = createCustomerValueCSV(csvFile, unique_categories, unique_category_values)
    return csvFile

def main():
    # do like a while loop, while not done shopping or something
    # get the csv file
    file_path = "FashionDataset.csv"
    # create a pandas DataFrame using the csv file
    my_csv = getCSVFile(file_path)
    # convert relevant columns from cents to dollars
    my_csv = convertCSVCenttoDollar(my_csv)
    # start shopping
    shopping = True
    while shopping:
        # get the budget of the user and sort for relavent products
        customer_csv, customer_budget = productsInBudgetCSV(my_csv)
        # perfrom price optimization on discount percentage and add info to a new column
        customer_csv = optimizedDiscountCSV(customer_csv, customer_budget)
        # get the percieved value for each product from the customer
        customer_csv = customerValueCSV(customer_csv, customer_budget)
        customer_csv.to_csv('FashionDatasetChanged.csv', header=True, index=True)
        # end shopping
        shopping = False
    # exit program
    print("Good bye")

    # set the value to each product. 1. Ask the customer to rank their desired product category. Price range of prodcuts for that category
    # this will get the value for us.  Set the values
    # then get budget of the customer
    # Perfrom DP integral KnapSack. 
    # (next version, get knapscack running first)1st prodcut %80 of budget, then other smaller items?
    # just see what knapSack gives back?

main()