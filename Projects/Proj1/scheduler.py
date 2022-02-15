# CS337 Spring 2022 - Operating Systems Prof. Al Madi
# scheduler.py
# Matthew Bass
# 02/09/2022

# This is a file to the different process scheduling functions for the OS

def FCFS_scheduler(processes, ready, CPU, Scheduled_Processes ,time, debug=True):
    ''' non-preemptive FCFS scheduler

    The First Come First Serve algorithim schuedules jobs to be executed
    based on the time that the arrive to the ready queue (jobs that arrive
    earlier are proccessed earlier). The FCFS algorithim can be thought of as
    just implementing a first in first out (FIFO) queue.

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

        Scheduled_Processes: this is a list of all the process that have been scheduled

        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.

        debug: this is a boolean with the default value of True. It controls a print
            statement that shows process ID, start time, and end time at each context
            switch. It is useful for debugging.
    '''

    # pick process with lowest arrival time and remove it from ready (sorting list)
    ready.sort(key = lambda x: x.arrival_time,reverse = True)
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

    Scheduled_Processes.append(process)

    if debug:
        print(f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def SJF_scheduler(processes, ready, CPU, Scheduled_Processes, time,
                   debug=True):
    ''' non-preemptive SJF scheduler

    The Shortest Job First algorithm schedules jobs to be executed
    based on the burst time (working time) of the processes in the ready
    queue. The SJF algorithm is one of the best approaches to minimize wait
    times and easy to implement when the CPU knows how long the process will
    take (in fact it needs to know this). This algorithim can be unfair to
    processes with long burt times though.



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

        Scheduled_Processes: this is a list of all the process that have been scheduled

        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.

        debug: this is a boolean with the default value of True. It controls a print
            statement that shows process ID, start time, and end time at each context
            switch. It is useful for debugging.
    '''

    # pick process with shortest burt time and remove it from ready (
    # sorting list)
    ready.sort(key=lambda x: x.burst_time, reverse=True)
    process = ready.pop()
    # set start time to time
    start_time = time

    # while process is not finished
    while (process.burst_time > 0):
        # decrement process burst time by one
        process.burst_time += -1

        # add 1 to time
        time += 1

        # add processes that arrived now to ready queue
        add_ready(processes, ready, time)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU (this will be useful later)
    CPU.append(dict(process=process.id,
                    Start=start_time,
                    Finish=end_time,
                    Priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def Priority_scheduler(processes, ready, CPU, Scheduled_Processes, time, debug =True):
    ''' non-preemptive Priority scheduler

    Priority is Correlation (higher number being higher priority)

    Scueduels the precesses in the ready queue based oon their priority.
    The Priority algorithm can still face problems like being unfair with it
    being unfair to processes with low priority
    (when it is a correlation priority like for this algorithm). This
    algorithm can also face starvation. One advantage of Priority scheduling
    is that it can have very low over head (alot of times just needing to be
    a max heap)

    !!! A solution to fix starvation (not perfect) is aging by increasing
    priority the longer the processes waits in the ready queue

    Warning possible to have starvation and is unfair to low priority processes
    One way to fix this is by using the priority method turnaround_time to
    prevent starvation by aging the processes (adding 1 to their priority for each time step)
    they are waiting in the ready queue

    Its overhead is minimal because it is like a max heap



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

        Scheduled_Processes: this is a list of all the process that have been scheduled

        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.

        priority_method: decides how the priority is calculated, if no value
            is passed it randomizes the priority. VALID INPUTS: turnaround_time or pre_calculated. If non considered
            pre_calculated

        debug: this is a boolean with the default value of True. It controls a print
            statement that shows process ID, start time, and end time at each context
            switch. It is useful for debugging.


    '''






    # pick process with highest priority and remove it from ready
    ready.sort(key=lambda x: x.priority)
    process = ready.pop()
    # set start time to time
    start_time = time

    # while process is not finished
    while (process.burst_time > 0):
        # decrement process burst time by one
        process.burst_time += -1

        # add 1 to time
        time += 1

        # add processes that arrived now to ready queue
        add_ready(processes, ready, time)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU (this will be useful later)
    CPU.append(dict(process=process.id,
                    Start=start_time,
                    Finish=end_time,
                    Priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def Priority_Turnaround_scheduler(processes, ready, CPU, Scheduled_Processes,
                               time, debug =True):
    ''' non-preemptive Priority Turnariund scheduler

    Priority is Correlation (higher number being higher priority)

    The Priority algorithm schedules jobs to be executed
    based on the priority level of each job which is bases on burst time
    (working time) of the processes in the ready queue along with the
    processes arrival time. The Priority algorithm can still face problems
    like being unfair with it being unfair to processes with low priority
    (when it is a correlation priority like for this algorithm). This
    algorithm can also face starvation but shouldnt be as bad because it is aging by increasing
    priority the longer the processes waits in the ready queue. One
    advantage of Priority scheduling is that it can have very low over head (
    alot of times just needing to be a max heap)


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

        Scheduled_Processes: this is a list of all the process that have been scheduled

        time: this is an integer that represents the current time, where simulation starts
            at time zero and time is incremented by one after each time slice.

        priority_method: decides how the priority is calculated, if no value
            is passed it randomizes the priority. VALID INPUTS: turnaround_time or pre_calculated. If non considered
            pre_calculated

        debug: this is a boolean with the default value of True. It controls a print
            statement that shows process ID, start time, and end time at each context
            switch. It is useful for debugging.


    '''

    # Calculate turnaround time for all Processes in the ready Queue
    # output with the lowest turnaround is chosen first
    for proc in ready:
        proc.priority = (time - proc.arrival_time) + proc.burst_time

    # pick process with highest priority and remove it from ready
    ready.sort(key=lambda x: x.priority)
    process = ready.pop()
    # set start time to time
    start_time = time

    # while process is not finished
    while (process.burst_time > 0):
        # decrement process burst time by one
        process.burst_time += -1

        # add 1 to time
        time += 1

        # add processes that arrived now to ready queue
        add_ready(processes, ready, time)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU (this will be useful later)
    CPU.append(dict(process=process.id,
                    Start=start_time,
                    Finish=end_time,
                    Priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def add_ready(processes,ready,time):
    '''
    Adds Processes to ready that have arrived based on the time
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
    # sort the processes list
    processes.sort(key = lambda x: x.arrival_time)

    #If there are Proceeses left,
    # while the front of the processes list has arrived
    arrival_flag = True
    while arrival_flag:
        if (processes and (processes[0].arrival_time <= time)):
            ready.append(processes.pop())
        else:
            arrival_flag = False
    return
