'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
bakery_solution.py
Matthew Bass
04/05/2022

This is the Bakery Solution.

In the bakery_solution.py file you will implement Bakery’s synchronization
solution from lecture slides (lecture 14) using a Python class that
implements the following:

        ● An __init__ method that takes a thread_count and initializes a
        choosing list and a tickets list.


        ● A lock method that takes a thread_id as an argument. The method
        should behave according to the pseudocode in lecture slides.

        ● An unlock method that takes a thread_id and behaves according to
        the pseudocode in lecture slides.

'''

import time
import numpy as np
from sync_solution import SyncSolution


class SolutionBakery(SyncSolution):
    '''
    This is the Bakery Solution. It uses two np.arrays a choosing array and a
    tickets array.
    '''

    def __init__(self, thread_count : int) -> None:
        '''
        This method initializes a choosing array and a tickets array.

        Args: thread_count (int): The number of threads that will be using the
        Bakery Solution.

        Returns:
            None
        '''

        # Initialize thread count
        self.thread_count = thread_count

        # Initialize choosing array
        self.choosing = np.zeros(thread_count, dtype=bool)

        # Initialize tickets array
        self.tickets = np.zeros(thread_count, dtype=int)


    def lock(self, thread_id : int, debug : bool = True) -> None:
        '''
        This method implement Bakery’s synchronization solution from lecture
        slides (lecture 14)

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

        thread_idx = thread_id-1

        ### The Doorway


        # Choosing variable to be TRUE indicating its intent to enter critical section.
        self.choosing[thread_idx] = True

        # Set tickets array to the highest ticket number corresponding to other processes.
        self.tickets[thread_idx] = np.max(self.tickets) + 1

        # Set the choosing variable is set to FALSE indicating that it now has a new ticket number.
        self.choosing[thread_idx] = False

        # The entry part of the lock
        for p in range(self.thread_count):

            # Wait until thread p receives its number:
            while self.choosing[p]:
                pass

            # Then first the ticket number is compared. If they are the same
            # then the thread id is compared next
            while (self.tickets[p] != 0) and \
                    ((self.tickets[p],p) <
                     (self.tickets[thread_idx],thread_idx)):
                pass


        if debug:
            print(f'Thread {thread_id} has locked')


    def lockSleep(self, thread_id : int, debug : bool = True) -> None:
        '''
        This method implement Bakery’s synchronization solution from lecture
        slides (lecture 14)

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

        thread_idx = thread_id - 1

        ### The Doorway

        # Set the choosing array to True at the thread_id index
        self.choosing[thread_idx] = True

        # Force a context switch
        time.sleep(0.0001)

        # Set tickers array
        self.tickets[thread_idx] = np.max(self.tickets) + 1

        # Force a context switch
        time.sleep(0.0001)

        # Set the choosing array to False at the thread_id index
        self.choosing[thread_idx] = False

        # Force a context switch
        time.sleep(0.0001)

        # Second part of the lock
        for p in range(self.thread_count):
            while self.choosing[p]:
                pass
            while (self.tickets[p] != 0) and ((self.tickets[p], p) < (
            self.tickets[thread_idx], thread_idx)):
                pass

        if debug:
            print(f'Thread {thread_id} has locked')


    def unlock(self, thread_id : int, debug : bool = True) -> None:
            '''
            This method implement Bakery’s synchronization solution from lecture
            slides (lecture 14)


            The method takes a thread_id as an argument. The method should behave
            according to the pseudocode in lecture slides. All it does is change the
            value of turn according to thread_id being unlocked.

            Args:
                thread_id (int): The thread_id of the thread that is trying to
                release the lock of.
                debug (bool): If True, print the value of turn after the unlock.
            '''
            thread_idx = thread_id - 1

            self.tickets[thread_idx] = 0


            if debug:
                print(f"Thread {thread_id} released the lock.")




def main():
    return


if __name__ == '__main__':
    main()