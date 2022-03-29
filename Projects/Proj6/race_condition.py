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
import sync_solutions

from sync_solution import SyncSolution

# Making the list of valid solutions
VALID_SOLUTIONS = {'none', '1', '2', 'peterson', 'bakery', 'builtin'}

# Setting global var x to 0
x = 0


def increment():
    '''
    This function will be used to increment the global variable x
    Returns:
    '''
    # Get the global counter x
    global x

    # Increment the global counter x
    x += 1


def thread1_task(lock : , my_num):
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


def main_task(solution : str, sync_solution =None):
    '''
    This is the main task that will be used to test the
    software synchronization solutions.

    Args:
        sync_solutions: The solution that the user wants to test.
            Valid solutions are:
                none, 1, 2, peterson, bakery, builtin
    Returns:

    '''





    global x
    x = 0

    # Create threads based on the solution
    if solution == 'none':
        t1 = threading.Thread(target=thread1_task, args=(None, 1))
        t2 = threading.Thread(target=thread2_task, args=(None, 2))
    else:
        if solution == '1':
            # create a lock
            lock = sync_solutions.SolutionOne()



        # Create threads
        t1 = threading.Thread(target=thread1_task, args=(lock, 1))
        t2 = threading.Thread(target=thread2_task, args=(lock, 2))

    # start the threads
    t1.start()
    t2.start()

    # wait for threads to finish
    t1.join()
    t2.join()

def main():
    '''
    This is the main function that will be used to test the
    software synchronization solutions.

    Returns:

    '''
    # Get a valid solution from the user
    solution = input('Enter a valid solution: ')
    solution = solution.lower()

    # Check if the solution is valid
    if solution not in VALID_SOLUTIONS:
        print(f'\nError {solution} is an Invalid solution!!!' + f'\nValid solutions are: {VALID_SOLUTIONS}!!!' + f'\nSetting solution to none')
        solution = 'none'

    # Run the main task 10 times
    for i in range(10):
        main_task(solution)
        print("Iteration {0}: x = {1}".format(i, x))


if __name__ == "__main__":
    main()
