# CS337 Spring 2022 - Operating Systems Prof. Al Madi
# scheduler.py
# Matthew Bass
# 02/09/2022

# This is a file to the different process scheduling functions for the OS

def FCFS_scheduler(processes, ready, CPU, time, debug=True):
    ''' non-preemptive FCFS scheduler '''

    # pick process with lowest arrival time and remove it from ready
    process = min(processes, lambda x:x.arrival_time)

    # set start time to time
    start_time = time

    # while process is not finished
    while(process.burst_time != 0):
        # decrement process burst time by one
        process.burst_time += -1

        # add 1 to time
        time += 1

    # add processes that arrived now to ready queue
    ready.push(process)

    # set end time to time
    end_time = time

    # add processID, start, end to CPU (this will be useful later)
    CPU.append(dict(process=process.id,
                    Start=start_time,
                    Finish=end_time,
                    Priority=process.priority))

    # return time
    return time
