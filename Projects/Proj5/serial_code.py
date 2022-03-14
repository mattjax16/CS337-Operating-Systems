'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 5 - Multitasking
process.py
Matthew Bass
03/13/2022

This is a file to count the words and do other functions with the the
reddit's comments data

It does the following:
    - Read in the Reddit comments files

    - Count each word

    - Print the 10 most common words in each file

    - Print the frequency of a given word in each year to observe word trends
      (frequency = word_count / number_of_words)

    - Time your “common word” and “word trend” code reliably for comparison
'''
import os
import re
import numpy as np
from typing import Any, List

'''
GLobal variables
'''

VALID_DATA_TYPES = ["list", "np", "gpu"]

'''
Helper FunctionS
'''

def checkDataType(data_type : str):
    '''
    This is a function to check the data types if the datatype is valid
    then nothing happens if it isnt the code exits

    :param data_type: string of data type being passes
    :return:
    '''
    if data_type.lower() not in VALID_DATA_TYPES:
        print(f"Error {data_type} is not a valid data type!!!\n"+
              f"Valid data_types are {VALID_DATA_TYPES}\n"+
              f"exiting from the code!!!")
        exit()


'''
Functions to parse the raw data
'''

def cleanDataList(raw_line_data : list) -> list:
    '''
    Function to clean the raw data from each file

    :param raw_line_data: list of raw data strings
    :return:
    '''

    clean_data = splitLinesList(raw_line_data)

    #making regex to look for word
    word_regex = re.compile("^[a-zA-Z]")
    # Filter out all words strings that are not begging with letters
    clean_data = list(filter(word_regex.match, clean_data ))

    # Make all the filtered words lowercase
    clean_data = list(map(str.lower, clean_data))

    return clean_data

def splitLinesList(raw_line_data : list) -> list:
    '''
    This function splits the raw list of line strings into

    :param raw_line_data: list of raw data strings
    :return:
    '''
    raw_words_list = []
    for line in raw_line_data:
        raw_words_list += re.split("[^a-zA-Z0-9']", line)
    return raw_words_list



'''
Reading in Comments
'''

def readInRawDataNP(file_name : str, data_path:str) -> np.chararray:
    '''
    A function to read in the data of the file and
    returns the raw sting in a list data structure

    :param file_name: the name of the file
    :param data_path: the path to the file
    :return: raw_data: the raw data string of the file in a np char array
    '''

    with open(data_path+file_name, 'r') as file:
        data = file.readlines()
        data = np.chararray(data)
        return data


def readInRawDataList(file_name : str, data_path:str) -> List:
    '''
    A function to read in the data of the file and
    returns the raw sting in a list data structure

    :param file_name: the name of the file
    :param data_path: the path to the file
    :return: raw_data: the raw data string of the file in a List
    '''

    with open(data_path+file_name, 'r') as file:
        data = file.readlines()
        return data

def readInComments(data_type : str = "list") -> dict:
    '''
    A function to read in the comment files.

    This is an I/O bound process

    :param data_type: a str of the data type to use. Valid types list, np, gpu
    :return: a dictionary of all the files raw strings
    '''

    # Check that valid data type has been passed
    data_type = data_type.lower()
    checkDataType(data_type)

    # Get the current file directory path of the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Make the filepath the reddit comments (data) path
    data_path = dir_path + "/data/"

    # Get all the data files
    data_files = os.listdir(data_path)

    raw_data = {}
    # Loop through all the files and read in the raw data
    for data_file in data_files:
         # Read in data based on data type
        if data_type == "list":
            raw_data[data_file] = readInRawDataList(data_file,data_path)
        elif data_type == "np":
            raw_data[data_file] = readInRawDataNP(data_file, data_path)



    # Loop through all the raw data from each clean it (parse the words)
    cleaned_data = {}
    for file_name, data in raw_data.items():

        #TODO add ability to work with different data_types
        cleaned_data[file_name] = cleanDataList(data)


    # Looped through the cleaned data and create the word maps
    for file_name, data in cleaned_data.items():

        pass
    print(1)

    return







# Main function to run the script
def main():
    readInComments()
    return


if __name__ == "__main__":
    main()