
import multiprocessing
import time
import os

def square(n):
    print(n, os.getpid())
    time.sleep(1)
    return n*n

def main():

    my_list = [1,2,3,4,5]
    result = []

    p = multiprocessing.Pool()  #processes=8

    result = p.map(square, my_list)

    print(result)


if __name__ == '__main__':
    main()