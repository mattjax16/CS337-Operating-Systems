'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
operating_system.py
Matthew Bass
02/10/2022

The operating_system.py file where processes are created, scheduler runs,
and statistics are calculated.
'''

#Importing the nessicary packages and objects
import pandas as pd
import scheduler
from process import Process
# import numpy #using numpy to make more efficient


def kernal(selected_scheduler,debug=False):
    """
     Simulates the CPU scheduling aspects of an operating system kernel.

    :param selected_scheduler: (Function) one of the scheduling functions from scheduler.py
    :param debug: (Boolean) If true output messages will be printed from the selected_scheduler function
    :return:
    """

    CPU = [] # A list to hold the scheduled process for the CPU

    ready = []  # A list to hold the process scheduled ready to be scheduled

    time = 0  # creating the intial time for the kernal

    processes = [Process(0,5,0,30),Process(1,4,2,35),
                 Process(2,1,5,36),Process(3,6,6,20)] # a list to hold all the processes to be schuedled for the CPU


    # adding the proccesses to the ready list
    while processes:
        ready.append(processes.pop())


    #runnig schuedler for all processes in ready
    while(ready):
         time = selected_scheduler(processes, ready, CPU, time, debug=debug)


    return



# Main Testing function
def main():

    kernal(scheduler.FCFS_scheduler,True)


if __name__ == "__main__":
    main()



