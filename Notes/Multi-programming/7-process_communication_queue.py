
import multiprocessing
import time

def square_list(mylist, q):
    for num in mylist:
        q.put(num * num)


def print_list(q):
    while not q.empty():
        print(q.get())

def main():

    numbers = [1, 2, 3, 4]
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=square_list, args=(numbers, q))
    p2 = multiprocessing.Process(target=print_list, args=(q,))
    
    p1.start()
    p2.start()
    p2.join()
    p1.join()


if __name__ == '__main__':
    main()