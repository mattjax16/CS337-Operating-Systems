'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
race_condition.py
Matthew Bass
03/29/2022

This is to make a race condition that will be used
to test mutual exclusion for solution 1
'''
import threading
import sync_solutions

from sync_solution import SyncSolution


# Setting global var x to 0
x = 0

INCREMENT = 500000
NUM_THREADS = 2

T1_AMT = INCREMENT
T2_AMT = INCREMENT


def increment():
    '''
    This function will be used to increment the global variable x
    Returns:
    '''
    # Get the global counter x
    global x

    # Increment the global counter x
    x += 1


def thread1_task(lock: threading.Lock, thread_id: int, debug: bool = True):
    '''
    This is the first thread that will be used to test the software
    synchronization solutions.

    Args:
        lock (threading.Lock): The lock that will be used to synchronize
        thread_id (int): The number that will be used to synchronize (the thread number)
        debug (bool): If the debug flag is set to True, then the debug
    '''
    global turn

    lock.acquire()

    for _ in range(INCREMENT):

        if debug:
            print(f'Thread {thread_id} is incrementing x ({x})')

        increment()

    if debug:
        print(f'Thread {thread_id} is unlocking')
    lock.release()

    if debug:
        print(f'Thread {thread_id} is done')
    return


def thread2_task(lock: threading.Lock, thread_id: int, debug: bool = True):
    '''
    This is the second thread that will be used to test the
    software synchronization solutions. This will be the thread that
    has the extreme amount of time to run. This will be used to test progression
    of the software synchronization solutions.

    Args:
        lock (threading.Lock): The lock that will be used to synchronize
        thread_id (int): The number that will be used to synchronize (the thread number)
        debug (bool): If the debug flag is set to True, then the debug
    '''
    global turn

    lock.acquire()

    for _ in range(INCREMENT):
        if debug:
            print(f'Thread {thread_id} is incrementing x ({x})')
        increment()

    if debug:
        print(f'Thread {thread_id} is unlocking')
    lock.release()


##########################################################################
# Functions to check the different solutions for correctness
##########################################################################

def check_result(result: int) -> bool:
    '''
    This function will check the result of the the x output for the main_tasks

    Args:
        result (int): The result of the x output from the main_task

    Returns:
        bool: True if the result is correct, False otherwise
    '''
    if result == INCREMENT * NUM_THREADS:
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


##########################################################################
#  Main test functions
##########################################################################


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
    # create a lock using the threading module
    lock = threading.Lock()

    # Create threads
    t1 = threading.Thread(target=thread1_task, args=(lock, 1, debug))
    t2 = threading.Thread(target=thread2_task, args=(lock, 2, debug))

    # start the threads
    t1.start()
    t2.start()

    # wait for threads to finish
    t1.join()
    t2.join()


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
