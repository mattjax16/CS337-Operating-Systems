'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
race_condition_pete_bwt.py
Matthew Bass
04/05/2022

This is to make a race condition that will be used to test for use of any
number off threads for peterson's solution. (FOR TESTING NUMBER OF THREADS WILL BE 3)

'''
import threading
import time
import sync_solutions

from sync_solution import SyncSolution

# Setting global var x to 0
x = 0

INCREMENT = 50000
NUM_THREADS = 3
T1_AMT = INCREMENT
T2_AMT = INCREMENT * 5
T3_AMT = INCREMENT * 3

INC_AMTS = [T1_AMT, T2_AMT, T3_AMT]

SYNCSOLUTION = sync_solutions.SolutionPeterson(thread_count=NUM_THREADS)


def increment():
    '''
    This function will be used to increment the global variable x
    Returns:
    '''
    # Get the global counter x
    global x

    # Increment the global counter x
    x += 1


def thread_task(lock: SyncSolution, thread_id: int, inc_amt: int,
                debug: bool = True):
    '''
    This is the thread task that will be used to test the software
    synchronization solutions.

    Args:
        lock (SyncSolution): The lock that will be used to synchronize
        thread_id (int): The number that will be used to synchronize (the thread number)
        inc_amt (int): The amount that will be used to increment the global variable x
        debug (bool): If the debug flag is set to True, then the debug
    '''

    lock.lockSleep(thread_id, False)

    for _ in range(inc_amt):

        if debug:
            print(f'Thread {thread_id} is incrementing x ({x})')

        increment()

    if debug:
        print(f'Thread {thread_id} is unlocking')
    lock.unlock(thread_id, False)

    prog_check = 0
    for _ in range(inc_amt * 10):
        prog_check += 1

    if debug:
        print(f'Thread {thread_id} is done')
    return


################################################################################
# Functions to check the different solutions for correctness
################################################################################

def check_result(result: int) -> bool:
    '''
    This function will check the result of the the x output for the main_tasks

    Args:
        result (int): The result of the x output from the main_task

    Returns:
        bool: True if the result is correct, False otherwise
    '''
    if result == sum(INC_AMTS):
        return True
    else:
        return False


def check_results(results: list) -> bool:
    '''
    This function will check the results of the the x outputs for the main_tasks

    Args:
        results (list): The list of results from the main_tasks

    Returns:
        bool: True if the results are correct, False otherwise
    '''
    for result in results:
        if not check_result(result["x"]):
            return False
    return True


def check_global_x() -> bool:
    '''
    This function will check the global x variable

    Returns:
        bool: True if the global x variable is correct, False otherwise
    '''
    global x

    if x == T1_AMT + T2_AMT:
        return True
    else:
        return False


################################################################################
#  Main test functions
################################################################################


def main_task(debug: bool = False) -> int:
    '''
    This is the main task that will be used to test the
    software synchronization solutions.

    Args:

        debug (bool): If the debug flag is set to True, then the debug

    Returns:
        int: The result of the x output from the main_task

    '''

    global x
    x = 0

    # Create threads based on the info
    # create a lock
    lock = SYNCSOLUTION

    # Create threads
    threads = []
    for thread_num in range(1, NUM_THREADS + 1):
        thread = threading.Thread(target=thread_task,
                                  args=(
                                  lock, thread_num, INC_AMTS[thread_num - 1],
                                  debug))
        threads.append(thread)

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()


def main(debug: bool = False) -> None:
    '''
    This is the main function that will be used to test the
    software synchronization solutions.

    Args:
        debug (bool): If the debug flag is set to True, then the debug
    Returns:

    '''

    # Run the main task 10 times
    main_task_results = []
    for i in range(10):
        # Run the main task
        main_task(debug)

        # Print the results
        print("Iteration {0}: x = {1}".format(i, x))

        # Append the results to the list
        main_task_results.append({'iteration': i, 'x': x})

    # Check the results
    if check_results(main_task_results):
        print('\nAll results are correct!')

    # Else print the results that are incorrect
    else:
        print('\nThe results are incorrect!')
        print('\nThe results are:')
        for result in main_task_results:
            print(f'Iteration {result["iteration"]}: x = {result["x"]}')

    # Check the global x variable
    if check_global_x():
        print('\nThe global x variable is correct!')
    else:
        print('\nThe global x variable is incorrect!')
        print(f'\nThe global x variable should be {INCREMENT * NUM_THREADS}')
        print(f'\nThe global x variable is {x}')

    return


if __name__ == "__main__":
    main()