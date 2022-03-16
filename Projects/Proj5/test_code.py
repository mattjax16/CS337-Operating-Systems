
import pandas as pd
import numpy as np
import nltk
import re
import time
import os
from nltk.tokenize import word_tokenize
from collections import Counter

#main function for testing
def main():

    # Get the current file directory path of the file.
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Make the filepath the reddit comments (data) path
    data_path = os.path.join(dir_path, os.path.normcase("data/"))

    # Get all the data files
    data_files = os.listdir(data_path)
    fil = data_path + data_files[2]

    n = 40
    t1_start_time = time.perf_counter()
    for i in range(n):
        t_start_time = time.perf_counter()
        with open(fil, 'r') as file:
            data = file.read()
            data = re.sub(r"[^A-Za-z0-9\s]+", "", data).split(" ")

            data = Counter(data)

        t_end_time = time.perf_counter()
        t_total_time = t_end_time - t_start_time
        print(f"\nAction {i} is done! " + f"\n\tIt took {t_total_time} sec(s) to run in total!\n")

    t1_end_time = time.perf_counter()
    t1_total_time = t1_end_time - t1_start_time
    print(f"\nAction is done! " + f"\n\tIt took {t1_total_time/n} sec(s) to run on avg!\n")


    return


if __name__ == '__main__':
    main()