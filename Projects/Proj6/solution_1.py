'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
solution_2.py
Matthew Bass
03/29/2022

This is the first solution to the project.

I will will implement the first synchronization attempt from lecture slides
(lecture 12) using a Python class that implements the following:

    ● An __init__ method that initializes a turn variable.

    ● A lock method that takes a thread_id as an argument. The method should
    behave according to the pseudocode in lecture slides.

    ● An unlock method that takes a thread_id, and uses it to change the
    value of turn according to the pseudocode in lecture slides.
'''

from dataclasses import dataclass, field
from sync_solution import SyncSolution

@dataclass
class Solution1(SyncSolution):
    '''
    This is the first solution to the project.

    Initialize the turn variable.

        Args:
            turn (int): The initial value of the turn variable.

    '''
    turn: int = field(default=1)
    name: str = '1'

    def lock(self, thread_id : int, debug : bool = True) -> None:
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

    def unlock(self, thread_id : int, debug : bool = True) -> None:
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
        self.turn = (thread_id) % 2 + 1

        if debug:
            print(f"Thread {thread_id} released the lock.")




def main():
    return


if __name__ == '__main__':
    main()