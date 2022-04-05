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

from dataclasses import dataclass, field
import time
from sync_solution import SyncSolution

@dataclass
class SolutionPeterson(SyncSolution):
    '''
    This is the Peterson's solution to the project.(uses flags and turn)
    '''
    turn: int = field(default=1)
    flags: int = field(default_factory=lambda: [False] * 2)
    name: str = field(default="peterson")


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

        # Get thread id and other thread id
        thread_id -= 1
        other_thread = thread_id ^ 1

        # Set flag
        self.flags[thread_id] = True

        #Set turn
        self.turn = other_thread

        # Wait for other thread to release lock
        while self.flags[other_thread] and self.turn == other_thread:
            pass

        if debug:
            print(f'Thread {thread_id+1} has locked')


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

        # Get thread id and other thread id
        thread_id -= 1
        other_thread = thread_id ^ 1

        # Set flag
        self.flags[thread_id] = True

        # Force a context switch
        time.sleep(0.0001)

        # Set turn
        self.turn = other_thread

        # Force a context switch
        time.sleep(0.0001)

        # Wait for other thread to release lock
        while self.flags[other_thread] and self.turn == other_thread:
            pass

        if debug:
            print(f'Thread {thread_id+1} has locked')



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