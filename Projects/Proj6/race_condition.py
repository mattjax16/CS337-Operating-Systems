'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
race_condition.py
Matthew Bass
03/29/2022

This is the base code to make a race condition that will be used
to test all the different software synchronization solutions
'''

import threading


x=0


def increment():
    global x
    x += 1


def thread1_task(lock, my_num):
    global turn
    for _ in range(10000):
        increment()


def thread2_task(lock, my_num):
    '''
    This is the second thread that will be used to test the
    software synchronization solutions.

    

    '''
    global turn
    for _ in range(10000):
        increment()


def main_task():

    global x 
    x=0
    
    # create a lock
    # lock = SolutionOne()
    lock   = threading.Lock()

    # create 2 threads
    t1 = threading.Thread(target=thread1_task, args=(lock, 1))
    t2 = threading.Thread(target=thread2_task, args=(lock, 2))

    # start the threads
    t1.start()
    t2.start()

    # wait for threads to finish
    t1.join()
    t2.join()
    
    # print the final value of x for each iteration
    for i in range(10):
        main_task()
        print("Iteration {0}: x = {1}".format(i,x))