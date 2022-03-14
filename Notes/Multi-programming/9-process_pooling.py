
import multiprocessing
import time
import os

def square(n):
    print(n, os.getpid())
    return n*n

def main():

    my_list = [1,2,3,4,5]
    result = []

    for num in my_list:
        result.append(square(num))

    print(result)


if __name__ == '__main__':
    main()