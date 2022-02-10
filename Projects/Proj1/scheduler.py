# CS337 Spring 2022 - Operating Systems Prof. Al Madi
# scheduler.py
# Matthew Bass
# 02/09/2022

# This is a file to the different process scheduling functions for the OS

def FCFS_scheduler(processes, ready, CPU, time, debug=True):
    ''' non-preemptive FCFS scheduler

    Parameters:
        processes: is a list of all the processes in the simulation,
            whether they arrived or not, they are in this list.

        ready: this is a list of processes with current arrival time.
            Meaning, if the arrival time of a process is less than
            the current time, it should be in the ready list.
            Therefore, this list holds only processes that have
            arrived at the ready list.

        CPU: this is a list that simulates the CPU by holding beginning runtime
            and end of runtime for each process. This is the same as the Gantt bar
            that we have been using in lecture slides at the bottom of each example.

        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.

        debug: this is a boolean with the default value of True. It controls a print
            statement that shows process ID, start time, and end time at each context
            switch. It is useful for debugging.
    '''

    # pick process with lowest arrival time and remove it from ready (sorting list)
    ready.sort(key = lambda x: x.arrival_time)
    process = ready.pop()
    # set start time to time
    start_time = time

    # while process is not finished
    while(process.burst_time > 0):
        # decrement process burst time by one
        process.burst_time += -1

        # add 1 to time
        time += 1

        # add processes that arrived now to ready queue
        add_ready(processes,ready,time)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU (this will be useful later)
    CPU.append(dict(process=process.id,
                    Start=start_time,
                    Finish=end_time,
                    Priority=process.priority))

    if debug:
        print(f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")


    # # Run until ready
    # while(ready):
    #     FCFS_scheduler(processes, ready, CPU, time, debug=debug)

    return time


def add_ready(processes,ready,time):
    '''
    Parameters:
        processes: is a list of all the processes in the simulation,
            whether they arrived or not, they are in this list.

        ready: this is a list of processes with current arrival time.
            Meaning, if the arrival time of a process is less than
            the current time, it should be in the ready list.
            Therefore, this list holds only processes that have
            arrived at the ready list.


        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.
    :param process:
    :return:
    '''
    while processes:
        ready.append(processes.pop())
