#parse csv file with csv library
import csv
#get os direcotry with os library
import os
#read csv file efficiently with pandas
import pandas as pd

#use r prefix to tell python not to interpret escape characters

file_path = "FashionDataset.csv"
#print(file_path)

#  #get the current working directory
# directory  =  os.getcwd()
# file_location = directory + file_path
# print(file_location)

# file = open("TestDataset.txt", 'r')
# print(file)
my_csv = pd.read_csv(file_path)
pd.options.display.max_rows = 10
#pd.set_option('display.max_rows', 10)
print(my_csv.head(10))

with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print('Test first row first coloum: ', row)
                line_count += 1
            else:
                print(row)
                break
# #         break
# #     print('finish')
            
#vector operations for efficiency
