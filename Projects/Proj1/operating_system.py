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


def kernal(selected_scheduler,debug=False,
           CPU_to_csv = True,Processes_to_csv = True):
    """
     Simulates the CPU scheduling aspects of an operating system kernel.

    :param selected_scheduler: (Function) one of the scheduling functions from scheduler.py
    :param debug: (Boolean) If true output messages will be printed from the selected_scheduler function
    :param CPU_to_csv: (Boolean) if true results of CPU will be written to a csv
    :param Processes_to_csv: (Boolean) if true results of Scheduled_Processes will be written to a csv
    :return:
    """

    CPU = [] # A list to hold the data for some of the
            # scheduled process for the CPU

    Scheduled_Processes = [] # A list to hold the scheduled process for the CPU

    ready = []  # A list to hold the process scheduled ready to be scheduled

    time = 0  # creating the intial time for the kernal

    processes = [Process(0,5,0,30),Process(1,4,2,35),
                 Process(2,1,5,36),Process(3,6,6,20)] # a list to hold all the processes to be schuedled for the CPU


    # adding the proccesses to the ready list
    # increment time until there is one
    while(len(ready) == 0):
        scheduler.add_ready(processes,ready,time)
        if len(ready) == 0:
            time +=1



    #runnig schuedler for all processes in ready
    while(processes or ready):
         time = selected_scheduler(processes, ready, CPU,Scheduled_Processes, time, debug=debug)




    # Once all the processes in the CPU that have finished
    # and calculate their wait time and turn around time
    calc_wait_and_tunaround(CPU,Scheduled_Processes)


    return


def calc_wait_and_tunaround(CPU,Scheduled_Processes):
    '''
    Calculates the wait tiem and turn around for all the schuedled processes

    :param CPU: this is a list that simulates the CPU by holding beginning runtime
            and end of runtime for each process. This is the same as the Gantt bar
            that we have been using in lecture slides at the bottom of each example.
    :param Scheduled_Processes: this is a list of all the process that have been scheduled
    :return:
    '''

    #Sort the CPU and Schedled_process based on their id
    CPU.sort(key = lambda x: x['process'],reverse = True)
    Scheduled_Processes.sort(key=lambda x: x.id, reverse=True)

    for cpu_info , proc in zip(CPU,Scheduled_Processes):
        proc.wait_time = cpu_info['Start'] - proc.arrival_time
        proc.turnaround_time =  cpu_info['Finish'] - proc.arrival_time

    return




# Main Testing function
def main():

    kernal(scheduler.FCFS_scheduler,True)


if __name__ == "__main__":
    main()



