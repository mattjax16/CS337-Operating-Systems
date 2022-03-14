import multiprocessing
import os

def square(n):
    print(n, os.getpid())
    return n*n

def main():

    my_list = [1,2,3,4,5]
    result = []

    p = multiprocessing.Pool()
    result = p.map(square, my_list)
    print(result)

if __name__ == '__main__':
    main()
