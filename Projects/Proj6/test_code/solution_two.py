'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
solution_two.py
Matthew Bass
04/05/2022

This is the second solution to the project.

In the solution_two.py file you will implement the second synchronization
attempt from lecture slides (lecture 13) using a Python class that implements
the following:
 `
    ● An __init__ method that initializes a flags list.

    ● A lock method that takes a thread_id as an argument. The method should
    behave according to the pseudocode in lecture slides.

    ● An unlock method that takes a thread_id, and uses it to change the
    value of flags according to the pseudocode in lecture slides.

'''

from dataclasses import dataclass, field
import time
from sync_solution import SyncSolution


@dataclass
class Solution2(SyncSolution):
    '''
    This is the second solution to the project.
    '''

    flags: int = field(default_factory=lambda: [False] * 2)
    name: str = field(default="2")
    thread_count: int = field(default=2)

    def lock(self, thread_id: int, debug: bool = True) -> None:
        '''
        This method implements the second synchronization attempt from lecture slides
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

        thread_idx = thread_id - 1
        other_thread = thread_idx ^ 1

        self.flags[thread_idx] = True
        while self.flags[other_thread]:
            pass

        # IF DEBUG PRINT THAT THE THREAD HAS LOCKED
        if debug:
            print(f'Thread {thread_id} has locked')

    def lockSleep(self, thread_id: int, debug: bool = True) -> None:
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

        thread_idx = thread_id - 1
        other_thread = thread_idx ^ 1

        self.flags[thread_idx] = True

        # FORCE A CONTEXT SWITCH
        time.sleep(0.0001)

        while self.flags[other_thread]:
            pass
        if debug:
            print(f'Thread {thread_id} has locked')

    def unlock(self, thread_id: int, debug: bool = True) -> None:
        '''
        This method implements the second synchronization attempt from lecture slides
        (lecture 13).

        The method takes a thread_id as an argument. The method should behave
        according to the pseudocode in lecture slides. All it does is change the
        value of turn according to thread_id being unlocked.

        Args:
            thread_id (int): The thread_id of the thread that is trying to
            release the lock of.
            debug (bool): If True, print the value of turn after the unlock.
        '''
        thread_idx = thread_id - 1
        self.flags[thread_idx] = False

        if debug:
            print(f"Thread {thread_id} released the lock.")


def main():
    return


if __name__ == '__main__':
    main()
