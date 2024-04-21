# parse csv file with csv library
import csv
# get os direcotry with os library
import os
# read csv file with pandas library
import pandas as pd
# use numpy select with numpy library
import numpy as np
# round numbers with standard math library
import math as math
# create random permutations with random library
import random as rd
import time

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

def floatToInt(value):
    ''' 
        A function that converts a singluar piece of data from float type to ceiling integer
        inputs: value, the value being converted
        output: value, the convereted value
    '''
    value = int(math.ceil(value))
    return value

def convertCSVFloattoInt(csvFile):
    ''' 
    A function what changes column inBudgetPrice from folat type to Int.
    Outstanding task: implement this function so it's not hard coded.
    inputs: name of .csv file in current directory
    output: altered DataFame
    '''
    # specify the Sell Price column with applied discounts
    OPTDiscount_col = "inBudgetPrice"
    productValue = "CustomerValue"
    # perfom cents to dollar conversion on column of data
    csvFile[OPTDiscount_col] = csvFile[OPTDiscount_col].apply(floatToInt)
    csvFile[productValue] = csvFile[OPTDiscount_col].apply(floatToInt)
    return csvFile

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
    csvFile[MRP_col] = csvFile[MRP_col].apply(centsToDollars)
    # perfom cents to dollar conversion on column of data
    csvFile[Discount_col] = csvFile[Discount_col].apply(centsToDollars)
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

    # the new column being added
    OPTDiscount_col = "inBudgetPrice"
    # the column we are basing our calculations from
    MRP_col = "MRPNum"
    csvFile.loc[csvFile[MRP_col] <= budget, OPTDiscount_col] = csvFile[MRP_col]
    csvFile.loc[csvFile[MRP_col] > budget, OPTDiscount_col] = budget
    #TODO: is this return statement needed?
    return csvFile

def createCustomerValueCSV(csvFile, category_list, value_list):
    ''' 
        A function that creates a new column in the DataFrame of product value
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # the new column being added
    productValue = "CustomerValue"
    # the column we are basing our calculations from
    category_col = "Category"
    for i in range(len(category_list)):
        csvFile.loc[csvFile[category_col] == category_list[i], productValue] = value_list[i]
    #TODO: is this return statement needed?
    return csvFile


def customerValueCSV(csvFile):
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
    print("Please input a unique ranking from 1 to "+str(len(unique_categories))+", where 1 means 'I don't like it', and "+str(len(unique_categories))+" means 'I like it', for each category:")
    unique_category_values = []
    # get user input:
    #for i in range(len(unique_categories)):
    #    value = input(unique_categories[i]+" :")
    #    # store the value
     #   unique_category_values.append(int(value))
    
    # or create a random permutation

    numbers = list(range(1, len(unique_categories) + 1))
    rd.shuffle(numbers)
    unique_category_values = numbers
    # create new column of data with value info
    csvFile = createCustomerValueCSV(csvFile, unique_categories, unique_category_values)
    return csvFile

def knapSack(values, prices, rows, cols):
    ''' 
        Perform the integral knapSack algorithm on the products that meet the customer requirements.
        Maximize value given the shopping bag capacity and price of products
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: 
    '''
    # capacity = int(capacity)
    # # get values
    # productValue = "CustomerValue"
    # values = list(csvFile[productValue])
    # # get prices of each product
    # OPTDiscount_col = "inBudgetPrice"
    # prices = list(csvFile[OPTDiscount_col])
    # # get the number of products
    # n = len(values)
    # rows = n
    # cols = capacity

    #begin making 2d array full of zeros
    knap_2d = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(0)
        knap_2d.append(row)
        
    # begin dp bottom up
    # start one past the begining
    for i in range(1, rows):
        # j represents the current budget capacity, cols inherenty represents the capacity
        for j in range(1, cols):
            knap_2d[i][j] = knap_2d[i-1][j]
            # if the current budget is >= current product price
            # and 
            # value of this combinaiton is less than previous + next item
            if ((j >= prices[i]) and (knap_2d[i][j] < (knap_2d[i-1][j-1] + values[i]))):
                knap_2d[i][j] = knap_2d[i-1][j-1] + values[i]
    # done loop
    return knap_2d[rows - 1][cols - 1]

def SA(values, prices, heur, temp, beta, alpha, epsilon, capacity, rnd):
    '''
        Perform the SA algorithm on the products that meet the customer requirements.
        Maximize value given the shopping bag capacity and price of products
        Outstanding task: implement this function so it's not hard coded.
        inputs: C set of candidates
                S, a subset of C that are solutions
                v, objective function mapping a candidate to a real value
                opt, type of optimization, a min or max. We are a max
        output: 

    '''
    i = 0
    # create the first candidate, all 0's
    pack_combination = [0]*len(values)
    #c = adjacent(pack_combination, rnd)
    c = pack_combination
    best = c
    while True:
        c_next = adjacent(c, rnd)
        # obtain h value for c
        h = heur()
        h_c = h.h_SA(c, values, prices, capacity)
        print("h_c value: ", h_c)
        # obtain h value for c_next
        h_c_next = h.h_SA(c_next, values, prices, capacity)
        print("h_c_next value: ", h_c_next)


        diff = h_c_next - h_c
        accept_p = min(1, np.exp(diff*(beta/temp)))
        p = rnd.random()
        print("accept_p :", accept_p)
        print("random p :", p)
        if p <= accept_p:  
            # accept worse packing anyway
            c = c_next
        # else don't accept
        if  h_c_next > h.h_SA(best, values, prices, capacity):
            best = c_next
            #c = c_next

        i += 1
        temp = temp/(1+(alpha*i))
        if temp < epsilon:
            # this current combination is the best combbination
            max_value = 0
            for i in range(len(best)):
                if best[i] == 1:
                    max_value += values[i]
            return max_value

def adjacent(pack_combination, rnd):
    ''' 
        Calculates an adjacent candidate solution
        The set of k neighbors is generated by 
            (i) replacing an item in the subset with another item, 
            (ii) removing an item, or 
            (iii) adding an item. 
            Whenever generating one of the k neighbors, 
            we choose one of the rules (i), (ii), and (iii) uniformly at random
        inputs: name of .csv file in current directory
        output: 
    '''
    neighbor_generation_choice = rnd.choice([1, 2, 3])

    match neighbor_generation_choice:
        case 1:
            #(i) replacing an item in the subset with another item
            #source CHATGPT 21/04/2024 "I want to turn an already 1 into 0, and an already 0 into 1"
            indices_of_ones = [i for i, x in enumerate(pack_combination) if x == 1]
            indices_of_zeros = [i for i, x in enumerate(pack_combination) if x == 0]

            # Randomly choose an index from the list of 1s and 0s
            index_to_toggle_one = rnd.choice(indices_of_ones)
            index_to_toggle_zero = rnd.choice(indices_of_zeros)

            # Toggle the values at the selected indices
            pack_combination[index_to_toggle_one] = 0
            pack_combination[index_to_toggle_zero] = 1
            #exit
            return pack_combination
        case 2:
            # (ii) removing an item
            # find all items in the sack
            indices_of_ones = [i for i, x in enumerate(pack_combination) if x == 1]
            # Randomly choose an index from the list of 1s
            index_to_toggle_one = rnd.choice(indices_of_ones)
            # remove selected indices
            pack_combination[index_to_toggle_one] = 0
            #exit
            return pack_combination
        case 3:
            # (iii) adding an item
            # find all items not in the sack
            indices_of_zeros = [i for i, x in enumerate(pack_combination) if x == 0]
            # Randomly choose an index from the list of 0s
            index_to_toggle_zero = rnd.choice(indices_of_zeros)
            # add selected indices
            pack_combination[index_to_toggle_zero] = 1
            #exit
            return pack_combination

class heuristic:
    
    def h_SA(self, pack_combination, values, prices, capacity):
        '''
        the function that calcuates the heuristic for SA
        '''
        # total value and size of a specified packing
        v = 0 # total value of packing
        s = 0 # total price of packing
        n = len(pack_combination)
        for i in range(n):
            if pack_combination[i] == 1:
                v += values[i]
                s += prices[i]
        # if too big to fit in knapsack, price > budget
        if s > capacity:  
            v = 0
        return v 

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
        customer_csv = customerValueCSV(customer_csv)
        # convert inBudgetPrice column into whole integers to prepare for KnapSack
        customer_csv = convertCSVFloattoInt(customer_csv)
        # save changes to new csv File for viewing 
        customer_csv.to_csv('FashionDatasetChanged.csv', header=True, index=True)

        # prepare for DP KnapSack:
        #       get values
        productValue = "CustomerValue"
        values = list(customer_csv[productValue])
        #       get prices of each product
        OPTDiscount_col = "inBudgetPrice"
        prices = list(customer_csv[OPTDiscount_col])
        #       get the number of products
        rows = len(values)
        #       get the total capacity as integer for table
        cols = int(customer_budget)
        #       perfrom DP integral KnapSack
        max_value = knapSack(values, prices, rows, cols)
        print("max value of shooping bag given budget by knapSack: ", max_value)

        # perpare for Simulated Annealing:
        #       create a heuristic function
        #       heuristic()
        #       generat a random number generator
        rnd = np.random.RandomState(int(time.time()))  
        #       T0
        init_temperature = 1000.0
        #       beta
        beta = 10
        #       alpha
        alpha = 1.0
        #       eplison
        epsilon = 0.05
        #       perfrom Simulated Annealing.
        max_value = SA(values, prices, heuristic, init_temperature, beta, alpha, epsilon, int(customer_budget), rnd)
        print("max value of shooping bag given budget by SA: ", max_value)

        # end shopping
        shopping = False
    # exit program
    print("Good bye")

    
    # (next version, get knapscack running first)1st prodcut %80 of budget, then other smaller items?
    # just see what knapSack gives back?

main()