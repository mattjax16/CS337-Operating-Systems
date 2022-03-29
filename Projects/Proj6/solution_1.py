'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
solution_one.py
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
class SolutionOne(SyncSolution):
    '''
    This is the first solution to the project.

    Initialize the turn variable.

        Args:
            turn (int): The initial value of the turn variable.

    '''
    turn: int = field(default=0)

    def lock(self, thread_id : int) -> None:
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

        if self.turn == thread_id:
            self.turn = (thread_id + 1) % 2
        else:
            while self.turn != thread_id:
                pass

    def unlock(self, thread_id : int) -> None:
        '''
        This method implements the first synchronization attempt from lecture slides
        (lecture 12).

        The method takes a thread_id as an argument. The method should behave
        according to the pseudocode in lecture slides. All it does is change the
        value of turn according to thread_id being unlocked.

        Args: thread_id (int): The thread_id of the thread that is trying to
        release the lock of.
        '''
        self.turn = thread_id




def main():
    return


if __name__ == '__main__':
    main()