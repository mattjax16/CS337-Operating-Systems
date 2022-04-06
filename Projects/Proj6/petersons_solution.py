'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
petersons_solution.py
Matthew Bass
04/05/2022

This is the Peterson's solution to the project.(uses flags and turn)

In the petersons_solution.py file you will implement Peterson’s
synchronization solution from lecture slides (lecture 13) using a Python
class that implements the following:

        ● An __init__ method that initializes a flags list and a turn variable.

        ● A lock method that takes a thread_id as an argument. The method
        should behave according to the pseudocode in lecture slides.

        ● An unlock method that takes a thread_id, and uses it to change the
        value of flags according to the pseudocode in lecture slides.

'''


import time
import numpy as np
from sync_solution import SyncSolution


class SolutionPeterson(SyncSolution):
    '''
    This is the Peterson's solution to the project.(uses flags and turn)
    '''

    def __init__(self, thread_count: int = 2) -> None:
        '''
        This method initializes the name turn and flags array

        Args: thread_count (int): The number of threads that will be using the
        Bakery Solution.

        Returns:
            None
        '''
        self.name = 'peterson'
        self.turn = 0
        self.flags = np.zeros(thread_count, dtype=bool)
        self.thread_count = thread_count



    def lock(self, thread_id : int, debug : bool = True) -> None:
        '''
        This method implements the Petersons synchronization attempt from lecture slides
        (lecture 13).

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

        if self.thread_count == 2:
            # Get thread id and other thread id
            thread_idx = thread_id - 1
            other_thread = thread_idx ^ 1

            # Set flag
            self.flags[thread_idx] = True

            # Set turn
            self.turn = other_thread

            # Wait for other thread to release lock
            while self.flags[other_thread] and self.turn == other_thread:
                pass

        elif self.thread_count > 2:

            # Get thread id and other thread id
            thread_idx = thread_id - 1
            other_thread_r = (thread_idx + 1) % self.thread_count
            other_thread_l = (thread_idx + 1) % self.thread_count


            # Set flag
            self.flags[thread_idx] = True

            # Set turn
            self.turn = other_thread_r

            # Wait for other thread to release lock
            while self.flags[other_thread_r] and self.flags[other_thread_l] and \
                    self.turn == other_thread_r:
                pass


        if debug:
            print(f'Thread {thread_id} has locked')


    def lockSleep(self, thread_id : int, debug : bool = True) -> None:
        '''
        This method is the same as lock but used to force a contex switch by having
        time.sleep() in the lock method.


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

        if self.thread_count == 2:
            # Get thread id and other thread id
            thread_idx = thread_id - 1
            other_thread = thread_idx ^ 1

            # Set flag
            self.flags[thread_idx] = True

            # Forcing a context switch
            time.sleep(0.0001)

            # Set turn
            self.turn = other_thread

            # Forcing a context switch
            time.sleep(0.0001)

            # Wait for other thread to release lock
            while self.flags[other_thread] and self.turn == other_thread:
                pass

        elif self.thread_count > 2:

            # Get thread id and other thread id
            thread_idx = thread_id - 1
            other_thread_r = (thread_idx + 1) % self.thread_count
            other_thread_l = (thread_idx + 1) % self.thread_count

            # Set flag
            self.flags[thread_idx] = True

            # Forcing a context switch
            time.sleep(0.0001)

            # Set turn
            self.turn = other_thread_r

            # Forcing a context switch
            time.sleep(0.0001)

            # Wait for other thread to release lock
            while self.flags[other_thread_r] and self.flags[
                other_thread_l] and self.turn == other_thread_r:
                pass

        if debug:
            print(f'Thread {thread_id} has locked')


    def unlock(self, thread_id : int, debug : bool = True) -> None:
            '''
            This method implements the Peterson's synchronization attempt from lecture slides
            (lecture 13).

            The method takes a thread_id as an argument. The method should behave
            according to the pseudocode in lecture slides. All it does is change the
            value of turn according to thread_id being unlocked.

            Args:
                thread_id (int): The thread_id of the thread that is trying to
                release the lock of.
                debug (bool): If True, print the value of turn after the unlock.
            '''
            thread_id -= 1
            self.flags[thread_id] = False


            if debug:
                print(f"Thread {thread_id+1} released the lock.")




def main():
    return


if __name__ == '__main__':
    main()