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
# use date and time as random seed for generator
import time 
from time import perf_counter
# create a plot using matplot library
import matplotlib.pyplot as plt

class PlotResults:
    """
    Class to plot the results.  Taken from Assignment 4 CMPUT 366
    """
    def plot_results(self, data1, data2, label1, label2, filename):
        """
        This method receives two lists of data point (data1 and data2) and plots
        a scatter plot with the information. The lists store statistics about individual search 
        problems such as the number of nodes a search algorithm needs to expand to solve the problem.

        The function assumes that data1 and data2 have the same size. 

        label1 and label2 are the labels of the axes of the scatter plot. 
        
        filename is the name of the file in which the plot will be saved.
        """
        _, ax = plt.subplots()
        ax.scatter(data1, data2, s=100, c="g", alpha=0.5, cmap=plt.cm.coolwarm, zorder=10)
    
        lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]
    
        ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        plt.xlabel(label1)
        plt.ylabel(label2)
        plt.grid()
        plt.savefig(filename)

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
    sub_csv = csv_file[convert_column]
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
    csvFile[productValue] = csvFile[productValue].apply(floatToInt)
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
    # consumer has a budget from 1 - 75
    budget = rd.uniform(1, 75)
    # specify the Sell Price column to compare discounts
    MRP_col = "MRPNum"
    Discount_col = "SellPrice"
    # collect all products that are normally in the budget, or that after applying the max possible discount they are within the budget
    in_budget_products = csvFile[(csvFile[MRP_col] <= budget) | (csvFile[Discount_col] < budget)]
    return in_budget_products, budget

def optimizedDiscountCSV(csvFile, budget):
    ''' 
        A function that creates a new column in the DataFrame OPTDiscountPercentOff
        Outstanding task: implement this function so it's not hard coded.
        inputs: name of .csv file in current directory
        output: altered DataFame
    '''
    # The math:
    #       if Price is already over Budget
    #       SellPrice = MRP(DiscountPercentOff)
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
    # obtain the customer percived value per category
    unique_category_values = []
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
    #edit items in place, pass by reference
    items = []
    #printOutKnapSack(knap_2d, rows-1, cols-1, items)          
    return knap_2d[rows - 1][cols - 1], items

def printOutKnapSack(A, i, D, items):
    ''' 
        Obtain the list of optimal items after perfroming DP knapsack
        Outstanding task: recursion depth error, did not use in project submisison
    '''
    if (i>0) or (D>0):
        if A[i][D] == A[i-1][D]:
            printOutKnapSack(A, i-1, D, items)
            items.append(0)
        else:
            printOutKnapSack(A, i-1, D-1, items)
            items.append(1)
    return 

def SA(values, prices, heur, temp, beta, alpha, epsilon, capacity, rnd):
    '''
        Perform the SA algorithm on the products that meet the customer requirements.
        Maximize value given the shopping bag capacity and price of products
        Outstanding task: implement this function so it's not hard coded.
        inputs: C set of candidates
        output: 

    '''
    i = 0
    # create the first candidate, all 0's
    c = [0]*len(values)
    best = c
    while True:
        c_next = adjacent(c, rnd)
        h = heur()
        # obtain h value for c
        h_c = h.h_SA(c, values, prices, capacity)
        # obtain h value for c_next
        h_c_next = h.h_SA(c_next, values, prices, capacity)

        diff = h_c_next - h_c
        accept_p = min(1, np.exp(diff*(beta/temp)))
        p = rnd.random()
        if p <= accept_p:   
            c = c_next

        if  h_c_next > h.h_SA(best, values, prices, capacity) and (h_c_next <= capacity):
            best = c_next
            #c = c_next

        i += 1
        temp = temp/(1+(alpha*i))
        if temp < epsilon:
            # this current combination is the best combbination
            max_value = None
            if h.h_SA(best, values, prices, capacity) != 0:
                max_value = 0
                for i in range(len(best)):
                    if best[i] == 1:
                        max_value += values[i]
            return max_value, best

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
    pack_combination = list(pack_combination)
    if sum(pack_combination) == 0:
        # no items in the bag, can not pick (i) or (ii)
        neighbor_generation_choice = rnd.choice([3])
    elif sum(pack_combination) == len(pack_combination):
         # all items in the bag, can not pick (iii)
        neighbor_generation_choice = rnd.choice([1, 2])
    else:
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
    # collect the run times in a list
    running_time_DPK = []
    running_time_SA= []
    # collect the values found in a list
    values_DPK = []
    values_time_SA = []

    # run the test 100 times
    for _ in range(100):
        # get the budget of the user and sort for relavent products
        customer_csv, customer_budget = productsInBudgetCSV(my_csv)
        # perfrom price optimization on discount percentage and add info to a new column
        customer_csv = optimizedDiscountCSV(customer_csv, customer_budget)
        # get the percieved value for each product from the customer
        customer_csv = customerValueCSV(customer_csv)
        # convert inBudgetPrice column into whole integers to prepare for KnapSack
        customer_csv = convertCSVFloattoInt(customer_csv)
        # save changes to new csv File for viewing 
        customer_csv.to_csv('FashionDatasetChanged.csv', header=True, index=False)

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
        # sart counter
        start = perf_counter()
        max_value, knapSackResultDPK = knapSack(values, prices, rows, cols)
        # stop counter
        stop = perf_counter()
        # find RT
        runtimeDPK= stop - start
        # save data
        running_time_DPK.append(runtimeDPK)
        # save results
        values_DPK.append(max_value)

        # perpare for Simulated Annealing:
        #       create a heuristic function
        # heuristic() this line is intentionally commented
        #       generat a random number generator
        rnd = np.random.RandomState(int(time.time()))  
        #       T-0
        init_temperature = 1000.0
        #       beta
        beta = 5
        #       alpha
        alpha = 2
        #       eplison
        epsilon = 0.005
        #       perfrom Simulated Annealing.
        # start counter
        start = perf_counter()
        max_value, knapSackResultSA = SA(values, prices, heuristic, init_temperature, beta, alpha, epsilon, int(customer_budget), rnd)
        # stop counter
        stop = perf_counter()
        # calculate RT
        runtimeSA= stop - start
        # save data
        running_time_SA.append(runtimeSA)
        # save results
        values_time_SA.append(max_value)

    plotter = PlotResults()
    plotter.plot_results(running_time_DPK, running_time_SA, "Running Time Dynamic Programming Bottom-Up KnapSack", "Running Time Simulated Annealing KnapSack", "running_time")
    plotter.plot_results(values_DPK, values_time_SA, "KnapSack Value with Dynamic Programming Bottom-Up Approach", "KnapSack Value with Simulated Annealing Approach", "knapsack_value")

    # exit program
    print("Good bye")

main()