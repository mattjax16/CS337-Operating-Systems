'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 2 - Preemptive CPU Scheduling Analysis
scheduler.py
Matthew Bass
02/21/2022

This is a file to the different process scheduling functions for the OS
'''

#Importing need libraries
from process import Process



'''
################################################################
Project 2 Algorithms
###############################################################
'''

def RR_scheduler(
        processes,
        ready,
        wait,
        CPU,
        Scheduled_Processes,
        time,
        quantum = 2,
        debug=True):
    ''' preemptive Round-Robin (RR) scheduler

        The Round-Robin (RR) algorithm is a scheduling algorithm
        where a processes is run for the specified quantum time or until it
        is finished then it is paused and another process in the ready queue
        is started. It accomplishes this by popping then appending the
        process back to the ready list if the process still has work to be done
        This make the algorithim preemptive at the end of the time slice.
        Some caveats are that long processes may have to wait n*q
        time units for another time slice where n is the number of other
        processes and q is the quantum or length of time slice

        Parameters:
            processes: is a list of all the processes in the simulation,
                whether they arrived or not, they are in this list.

            ready: this is a list of processes with current arrival time.
                Meaning, if the arrival time of a process is less than
                the current time, it should be in the ready list.
                Therefore, this list holds only processes that have
                arrived at the ready list. It also requires that the
                processes does not have I/0 time that needs to be waiting

            wait: this is a list of all the processes that are waiting for I/O input

            CPU: this is a list that simulates the CPU by holding beginning runtime
                and end of runtime for each process. This is the same as the Gantt bar
                that we have been using in lecture slides at the bottom of each example.

            Scheduled_Processes: this is a list of all the process that have been scheduled

            time: this is an integer that represents the current time, where simulation starts
                at time zero and time is incremented by one after each time slice.

            quantum: (int) the maximum amount of timesteps a process will
                    run for before it its put back to the waiting state (or finishes)
                    and the next process is started.

            debug: this is a boolean with the default value of True. It controls a print
                statement that shows process ID, start time, and end time at each context
                switch. It is useful for debugging.
        '''

    # Wait for the processes to be in ready queue or wait queue
    wait_for_process(processes, ready, time, wait)

    ## pick process that is ready with CPU work
    # ready.sort(key=lambda x: (x.duty_type, -x.times_worked_on))

    # popping the start of the process
    process = ready.pop(0)

    # indicate the process has been worked on
    process.process_worked_on()

    # set start time to time
    start_time = time

    # Work on the chosen process for at most the quantum time
    # or until the process is done
    for q_time in range(quantum):

        # add 1 to time
        time += 1

       # run the process
        process.run_process()

        #run the waiting list
        run_wait(ready,wait)


        if process.times_worked_on == 1:
            process.response_time = process.arrival_time - time







        # if the process is done add it to Scheduled_Processes and terminate
        # the loop
        if sum(process.duty) == 0:

            # set end time to time
            end_time = time

            # set the completion time of the process
            process.completion_time = time

            Scheduled_Processes.append(process)

            # add processID, start, end to CPU
            CPU.append(dict(id=process.id,
                            start=start_time,
                            finish=end_time,
                            priority=process.priority))



            # add processes that arrived now to ready queue
            add_ready(processes, ready, time)

            if debug:
                print(
                    f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")
            return time




        #if the process is in the IO state now
        if process.duty_type == "I/O":

            # change the processes status
            process.change_status()


            # If process isn't done and needs I/O append it to ready list
            wait.append(process)

            # set end time to time
            end_time = time

            # add processID, start, end to CPU
            CPU.append(dict(id=process.id,
                            start=start_time,
                            finish=end_time,
                            priority=process.priority))

            if debug:
                print(
                    f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

            return time


    # If process isn't done append it to ready list
    ready.append(process)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))


    # add processes that arrived now to ready queue
    add_ready(processes, ready, time)

    if debug:
        print(f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time








'''
################################################################
Project 1 Algorithms
###############################################################
'''

def FCFS_scheduler(
        processes,
        ready,
        CPU,
        Scheduled_Processes,
        time,
        debug=True):
    ''' non-preemptive FCFS scheduler

    The First Come First Serve algorithm schedules jobs to be executed
    based on the time that the arrive to the ready queue (jobs that arrive
    earlier are processed earlier). The FCFS algorithm can be thought of as
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

    # wait for the processes to be in ready queue
    wait_for_process(processes, ready, time)


    # pick process with lowest arrival time and remove it from ready (sorting
    # list)
    ready.sort(key=lambda x: x.arrival_time, reverse=True)
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
        add_ready(processes, ready, time)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def SJF_scheduler(processes, ready, CPU, Scheduled_Processes, time,
                  debug=True):
    ''' non-preemptive SJF scheduler

    The Shortest Job First algorithm schedules jobs to be executed
    based on the burst time (working time) of the processes in the ready
    queue. The SJF algorithm is one of the best approaches to minimize wait
    times and easy to implement when the CPU knows how long the process will
    take (in fact it needs to know this). This algorithm can be unfair to
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

    # wait for the processes to be in ready queue
    wait_for_process(processes, ready, time)

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

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def Priority_scheduler(
        processes,
        ready,
        CPU,
        Scheduled_Processes,
        time,
        debug=True):
    ''' non-preemptive Priority scheduler

    Priority is Correlation (higher number being higher priority)

    Schedules the precesses in the ready queue based on their priority which
    was externally assigned.
    The Priority algorithm can still face problems like being unfair with it
    being unfair to processes with low priority
    (when it is a correlation priority like for this algorithm). This
    algorithm can also face starvation. One advantage of Priority scheduling
    is that it can have very low over head (a lot of times just needing to be
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

    # wait for the processes to be in ready queue
    wait_for_process(processes, ready, time)

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

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def Priority_Turnaround_scheduler(processes, ready, CPU, Scheduled_Processes,
                                  time, debug=True):
    ''' non-preemptive Priority Turnaround scheduler

    Priority is Correlation (higher number being higher priority)

    The Priority Turnaround algorithm schedules jobs to be executed
    based on the priority level of each job which is bases on burst time
    (working time) of the processes in the ready queue along with the
    processes arrival time which is the turn, It subtracts the arrival time
    from the time of the CPU, so it is slowly aging the priority as well. The
    Priority Turnaround algorithm can
    still face problems like being unfair with it being unfair to processes
    with low priority (when it is a correlation priority like for this
    algorithm). This algorithm can also face starvation but shouldn't be as
    bad because it is aging by increasing priority the longer the processes
    waits in the ready queue. One advantage of Priority scheduling is that it
    can have very low over head (a lot of times just needing to be a max heap)


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


    # wait for the processes to be in ready queue
    wait_for_process(processes, ready, time)

    # Calculate turnaround time for all Processes in the ready Queue
    # output with the lowest turnaround is chosen first
    # get the max byrsttime of all processes
    all_procs = ready.copy() + processes.copy() + Scheduled_Processes.copy()
    all_procs.sort(key=lambda x: x.burst_time)

    # set the aging ammount
    max_burst_time = int(all_procs[-1].priority)

    for proc in ready:
        proc.priority = (time - proc.arrival_time) + \
            max_burst_time - proc.burst_time

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

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def Priority_Aging_scheduler(processes, ready, CPU, Scheduled_Processes,
                             time, debug=True):
    ''' non-preemptive Priority Turnaround scheduler

    Priority is Correlation (higher number being higher priority)

    The Priority algorithm schedules processes to be executed
    based on the priority level of each process which has been set externally
    The Priority algorithm can still face problems
    like being unfair with it being unfair to processes with low priority
    (when it is a correlation priority like for this algorithm). This
    algorithm can also face starvation but shouldnt be as bad because it is aging by increasing
    priority the longer the processes waits in the ready queue. One
    advantage of Priority scheduling is that it can have very low over head (
    alot of times just needing to be a max heap)

    IMPORTANT aging rate can be changed in code


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

    wait_for_process(processes, ready, time)

    # get the max priority of all processes
    all_procs = ready.copy() + processes.copy() + Scheduled_Processes.copy()
    all_procs.sort(key=lambda x: x.priority)

    # set the aging ammount
    age_amt = int(all_procs[-1].priority / 10)

    for proc in ready:
        proc.priority += age_amt

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

    # add processID, start, end to CPU 
    CPU.append(dict(id=process.id,
                    start=start_time,
                    finish=end_time,
                    priority=process.priority))

    Scheduled_Processes.append(process)

    if debug:
        print(
            f"Process ID: {process.id} , Start Time: {start_time} , End Time: {end_time}")

    return time


def wait_for_process(processes, ready, time, wait = [], debug = False):
    '''
    Waits for a processes to be in the ready queue. If the ready queue has
    nothing add the processes to the ready list
    increment time until there is one

    :param processes:
    :param ready:
    :param time:
    :return:
    '''

    wait_flag = (len(ready) == 0)
    while wait_flag:
        if debug:
            print("In wait_for_process")
        add_ready(processes, ready, time)
        if len(ready) == 0:
            run_wait(ready,wait)
            time += 1

        # if there is now something in the ready list
        if ready:
            wait_flag = False

    if debug:
        print("Done with wait_for_process")
    return

def add_ready(processes, ready, time):
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
    processes.sort(key=lambda x: x.arrival_time)

    # If there are Proceeses left,
    # while the front of the processes list has arrived
    arrival_flag = True
    while arrival_flag:
        if (processes and (processes[0].arrival_time <= time)):
            ready.append(processes.pop(0))
        else:
            arrival_flag = False
    return


def run_wait( ready, wait):
    '''
    A process to have all the processes in the wait time run and if any of
    them are done waiting add to ready queue

    ready: this is a list of processes with current arrival time.
                Meaning, if the arrival time of a process is less than
                the current time, it should be in the ready list.
                Therefore, this list holds only processes that have
                arrived at the ready list. It also requires that the
                processes does not have I/0 time that needs to be waiting

    waiting: this is a list of all the processes that are waiting for I/O input

    :return:
    '''

    for index, proc in enumerate(wait):
        proc.run_process()
        if proc.duty_type == "CPU":
            ready.append(wait.pop(index))
            ready[-1].change_status()