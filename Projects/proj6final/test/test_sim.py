
import threading
import time
import numpy as np
from dataclasses import field, dataclass
from abc import ABC, abstractmethod


# Abstract class for all the solutions
class SyncSolution(ABC):

    def __init__(self) -> None:
        # Name of the solution (lock)
        self.name = None

        # Number of threads
        self.thread_count = None

        return

    @abstractmethod
    def lock(self) -> None:
        '''
        This method will be used to lock the solution.
        '''

        pass

    @abstractmethod
    def unlock(self) -> None:
        '''
        This method will be used to unlock the solution.
        '''
        pass


def increment():
    '''
    This function will be used to increment the global variable x
    Returns:
    '''
    # Get the global counter x
    global x

    # Increment the global counter x
    x += 1


def check_result(result: int, inc_amts: list) -> bool:
    '''
    This function will check the result of the the x output for the main_tasks

    Args:
        result (int): The result of the x output from the main_task
        inc_amts (list): The list of increments that were done per thread

    Returns:
        bool: True if the result is correct, False otherwise
    '''
    if result == sum(inc_amts):
        return True
    else:
        return False


def thread_task_me(lock: SyncSolution, thread_id: int, inc_amt: int, debug:
                   bool = False) -> None:
    '''
    This function will be used to test for mutual exclusion.

    Args:
        lock (SyncSolution): The solution to test
        thread_id (int): The id of the thread
        inc_amt (int): The amount of times to increment the global counter x
        debug (bool): If True, will print the results of the test

    Returns:
        None
    '''
    # Lock the solution
    lock.lock(thread_id, debug)

    # Increment the global counter x
    for i in range(inc_amt):
        increment()

    if debug:
        print(f"Thread {thread_id} is unlocking")

    # Unlock the solution
    lock.unlock(thread_id, debug)

    if debug:
        print(f'Thread {thread_id} is done')

    return


def thread_task_prog(lock: SyncSolution, thread_id: int, inc_amt: int, debug:
                     bool = False) -> None:
    '''
    This function will be used to test for progress.

    Args:
        lock (SyncSolution): The solution to test
        thread_id (int): The id of the thread
        inc_amt (int): The amount of times to increment the global counter x
        debug (bool): If True, will print the results of the test

    Returns:
        None
    '''

    # Increment the global counter x
    for i in range(inc_amt):
        # Lock the solution
        lock.lock(thread_id, debug)

        increment()

        if debug:
            print(f"Thread {thread_id} is unlocking")

        # Unlock the solution
        lock.unlock(thread_id, debug)

    prog_check = 0
    for _ in range(inc_amt * 10):
        prog_check += 1

    if debug:
        print(f'Thread {thread_id} is done')

    return


def thread_task_bwt(lock: SyncSolution, thread_id: int, inc_amt: int, debug:
                    bool = False) -> None:
    '''
    This function will be used to test for progress.

    Args:
        lock (SyncSolution): The solution to test
        thread_id (int): The id of the thread
        inc_amt (int): The amount of times to increment the global counter x
        debug (bool): If True, will print the results of the test

    Returns:
        None
    '''

    # Increment the global counter x
    for i in range(inc_amt):
        # Lock the solution
        lock.lockSleep(thread_id, debug)

        increment()

        if debug:
            print(f"Thread {thread_id} is unlocking")

        # Unlock the solution
        lock.unlock(thread_id, debug)

    prog_check = 0
    for _ in range(inc_amt * 10):
        prog_check += 1

    if debug:
        print(f'Thread {thread_id} is done')

    return


def thread_task(lock: SyncSolution = None, thread_id: int = 0, inc_amt: int =
                100000, test:
                str = "me",
                debug: bool = False):
    '''
    This is the thread task that will be used to test the software
    synchronization solutions.

    Args:
        lock (SyncSolution): The lock that will be used to synchronize
        thread_id (int): The number that will be used to synchronize (the thread number)
        inc_amt (int): The amount that will be used to increment the global variable x
        test (str): The test that we will be doing to determine what code to run
        debug (bool): If the debug flag is set to True, then the debug
    '''

    # If the SyncSolution is not specified, then we will use the default
    if lock is None:
        # If there is no lock, then just increment the global x variable
        for _ in range(inc_amt):
            increment()

        if debug:
            print(f'Thread {thread_id} is done')
        return

    # If the test is me, then we will run the main_task
    if test == "me":
        thread_task_me(lock, thread_id, inc_amt, debug)

    # If not mutual exclusion but is progress check do more thread switching
    # (and locked and unlocking) for each increment so they have to rely on
    # each other .
    elif test == "prog":
        thread_task_prog(lock, thread_id, inc_amt, debug)

    # If testing for bounded wait time use the lockSleep method which is the
    # same as the lock method but induces contex switches by calling
    # time.sleep(0.0001)
    elif test == "bwt":
        thread_task_bwt(lock, thread_id, inc_amt, debug)

    return


def single_sim(solution: SyncSolution = None,
               inc_amt: int = 100000,
               thread_count=2,
               thread_multiplier=None,
               test: str = "me",
               debug: bool = False) -> int:
    '''
    This is the single_simulation that will be used to test the
    software synchronization solutions.

    Args:
        solution (SyncSolution): The lock that will be used to synchronize
        inc_amt (int): The amount that will be used to increment the global variable x
        thread_count (int): The number of threads that will be used
        thread_multiplier (list): The multiplier of the increment amount for each thread
        test (str): The test that we will be doing to determine what code to run
        debug (bool): If the debug flag is set to True, then the debug

    Returns:
        int: The result of the x output from the main_task

    '''

    global x

    # set x to 0
    x = 0

    # Check the thread_multiplier
    if thread_multiplier is None:
        thread_multiplier = [1] * thread_count
    elif len(thread_multiplier) != thread_count:
        raise ValueError(
            f"The thread_multiplier must be the same length as the thread_count")

    inc_amts = [inc_amt * x for x in thread_multiplier]



    # If the lock is not None then iniilize it
    if solution is not None:
        lock = solution(thread_count = thread_count)
    else:
        lock = None

    # Create threads
    threads = []
    for thread_num in range(1, thread_count + 1):
        thread = threading.Thread(target=thread_task, args=(
            lock, thread_num, inc_amts[thread_num - 1], test, debug))

        threads.append(thread)

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()

    return x


def check_results(results: list, inc_amts: list) -> bool:
    '''
    This function will check the results of the the x outputs for the main_tasks

    Args:
        results (list): The list of results from the main_tasks
        inc_amts (list): The list of increment amounts used in the main_tasks

    Returns:
        bool: True if the results are correct, False otherwise
    '''
    for result in results:
        if not check_result(result["x"], inc_amts):
            return False
    return True


def main_simulations(solution: SyncSolution = None,
                     inc_amt: int = 100000,
                     thread_count=2,
                     thread_multiplier=None,
                     test: str = "me",
                     debug: bool = False,
                     times: int = 10) -> None:
    """
    This is the main function that will be used to test the
    software synchronization solutions.r

    Args:
        solution (SyncSolution): The lock that will be used to synchronize
        times (int): The number of times that the simulation will be run
        inc_amt (int): The amount that will be used to increment the global variable x
        thread_count (int): The number of threads that will be used
        thread_multiplier (list): The multiplier of the increment amount for each thread
        test (str): The test that we will be doing to determine what code to run
        debug (bool): If the debug flag is set to True, then the debug



    Returns:
        None:

    """

    global x

    # set x to 0
    x = 0

    # Check the thread_multiplier
    if thread_multiplier is None:
        thread_multiplier = [1] * thread_count
    elif len(thread_multiplier) != thread_count:
        raise ValueError(
            f"The thread_multiplier must be the same length as the thread_count")

    inc_amts = [inc_amt * x for x in thread_multiplier]

    # Run the simulation times
    simulation_results = []
    for i in range(times):
        # Run the main task
        single_sim(
            solution,
            inc_amt,
            thread_count,
            thread_multiplier,
            test,
            debug)

        # Append the results to the list
        simulation_results.append({'iteration': i, 'x': x})

    # Check the results
    if check_results(simulation_results, inc_amts):
        print('\nAll results are correct!')

    # Else print the results that are incorrect
    else:
        print('\nThe results are incorrect!')

    # Print what the correct result should be
    print(f"The correct result should be {sum(inc_amts)}")

    # Print the results
    print('\nThe results are:')
    for result in simulation_results:
        print(f'Iteration {result["iteration"]+1}: x = {result["x"]}')

    return


@dataclass
class Solution1(SyncSolution):
    '''
    This is the first solution to the project.

    Initialize the turn variable.

        Args:
            turn (int): The initial value of the turn variable.

    '''
    turn: int = field(default=1)
    name: str = field(default='1')
    thread_count: int = field(default=2)

    def lock(self, thread_id: int, debug: bool = True) -> None:
        '''
        This method implements the first synchronization attempt from lecture slides
        (lecture 12).

        The method takes a thread_id as an argument. The method should behave
        according to the pseudocode in lecture slides.

        Args: thread_id (int): The thread_id of the thread that is trying to
        acquire the lock.

        Returns:
            None
        '''

        # IF DEBUG PRINT THAT THE THREAD IS SPINNING
        if debug:
            print(f'\nThread {thread_id} is spinning')
        while self.turn != thread_id:
            pass

        if debug:
            print(f'Thread {thread_id} acquired the lock.')
            print(f'Turn is {self.turn}')

    def unlock(self, thread_id: int, debug: bool = True) -> None:
        '''
        This method implements the first synchronization attempt from lecture slides
        (lecture 12).

        The method takes a thread_id as an argument. The method should behave
        according to the pseudocode in lecture slides. All it does is change the
        value of turn according to thread_id being unlocked.

        Args:
            thread_id (int): The thread_id of the thread that is trying to
            release the lock of.
            debug (bool): If True, print the value of turn after the unlock.
        '''

        # Change self.turn to the next thread_id (between 1 or 2)
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn == 2

        if debug:
            print(f"Thread {thread_id} released the lock.")

def main():


    main_simulations(inc_amt=500000, thread_multiplier=[1,5],solution=Solution1)
    return


if __name__ == '__main__':
    main()
