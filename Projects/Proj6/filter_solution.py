'''
CS337 Spring 2022 - Operating Systems Prof. Al Madi
Project 6 - Software Synchronization Solutions
filter_solution.py
Matthew Bass
04/06/2022

This is the filter solution which is the n+threads Peterson solution basically.

Here the flags are instead called levels, are a numpy array of integers (
representing each thread process) that is thread_count in size and it acts as
the queue representation for the threads, it is used to indicate the position
of each thread (which queue it is in) . A thread must wait until it is at the
end of the waiting queue to run its critical section.T turns instead be will
be made into a thread_count - 1 sized array and called last_to_enter because
it is used mainly to keep track of the last thread to enter the queue at each
level, this is to make sure there are not 2 threads running at the same time
(end of the queue). This helps with mutal exclusion because `pos` exits the
inner loop when there is either no process with a higher level than `level[
thread_idx]`, so the next waiting room is free; or, when `thread_idx !=
last_to_enter[pos]`, so another process joined its waiting room. At level
zero, then, even if all thread_count processes were to enter waiting room
zero at the same time, no more than thread_count − 1 will proceed to the next
room, the final one finding itself the last to enter the room. This then goes
on recursively for all the threads. If it is easier to think of the levels
and last to enter can be thought almost as a 2d matrix that is thread_count -
1 by thread_count.

'''
import time
import numpy as np
from sync_solution import SyncSolution


class SolutionFilter(SyncSolution):
    '''
    This is the Filter's solution to the project.(uses flags and turn)
    '''

    def __init__(self, thread_count: int = 2) -> None:
        '''
        This method initializes the name turn and flags array

        Args: thread_count (int): The number of threads that will be using the
        Filter Solution.

        Returns:
            None
        '''
        self.name = 'filter'
        self.levels = np.zeros(thread_count, dtype=int)
        self.last_to_enter = np.zeros(thread_count - 1, dtype=bool)
        self.thread_count = thread_count

    def noConflict(
            self,
            thread_idx: int,
            thread_pos: int,
            debug: bool = True) -> bool:
        '''
        This is a helper function for lock to make sure no threads are in the same position in the queue

        Args:
            thread_idx (int): The id of the thread that is trying to enter the critical section.(tid - 1)
            pos (int): The position of the thread in the queue
            debug (bool): If True, print the value of turn after the unlock.

        Returns:
            conflict (bool): True if there is a conflict, False if not.
        '''

        conflict = False
        for idx, pos in enumerate(self.levels):
            if idx != thread_idx and pos >= thread_pos:
                conflict = True
                break
        return conflict

    def lock(self, thread_id: int, debug: bool = True) -> None:
        '''
        This method implements the lock method for the Filter Solution. It
        runs a thread once it reaches the end of the levels queue.

        Args: thread_id (int): The thread_id of the thread that is trying to
        acquire the lock.

        Returns:
            None
        '''

        # IF DEBUG PRINT THAT THE THREAD IS SPINNING
        if debug:
            print(f'\nThread {thread_id} is spinning')

        thread_idx = thread_id - 1

        # Loop through all the queues minus th last
        for pos in range(0, self.last_to_enter.size - 1):

            # Set the thread to the pos position of the wait queue
            self.levels[thread_idx] = pos

            # Show that the
            self.last_to_enter[pos] = thread_idx

            # Wait till either there is no process at the top of queue or
            # until there is no other processes entered in that position of
            # the queue.
            while self.last_to_enter[pos] == thread_idx and \
                    self.noConflict(thread_idx, pos):
                pass

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

        # Loop through all the positions of the last_to_enter
        for pos in range(0, self.last_to_enter.size):

            # Set the thread to the pos position of the wait queue
            self.levels[thread_idx] = pos

            # Force a context switch
            time.sleep(0.0001)

            # Show that the
            self.last_to_enter[pos] = thread_idx

            # Force a context switch
            time.sleep(0.0001)

            # Wait till either there is no process at the top of queue or
            # until there is no other processes entered in that position of
            # the queue.
            while self.last_to_enter[pos] == thread_idx or self.noConflict(
                    thread_idx,
                    pos):
                pass

        if debug:
            print(f'Thread {thread_id} has locked')

    def unlock(self, thread_id: int, debug: bool = True) -> None:
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
        thread_idx = thread_id - 1
        self.levels[thread_idx] = -1
        if debug:
            print(f"Thread {thread_id} released the lock.")


def main():
    return


if __name__ == '__main__':
    main()
