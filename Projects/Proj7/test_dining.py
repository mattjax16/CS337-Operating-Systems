import threading
import random
import time
import contextlib
import io
import matplotlib.pyplot as plt
import multiprocessing
import warnings
import re
import sys
import numpy as np
import matplotlib.animation as animation
import networkx as nx
from dataclasses import dataclass, field


@dataclass
class Semaphore():
    '''
    A Semaphore class that allows for the use of a counter and a condition
    variable. It has a counter that is used to determine if the semaphore is
    available or not.  It also has a condition variable that is used to make
    incrementing and decrementing the counter thread safe (an atomic operation).

    Attributes:

        counter: An integer that represents the number of threads
                that are currently waiting on the condition variable.

        condition: A condition variable that is used to make incrementing and decrementing the
                counter thread safe (an atomic operation).
    '''
    counter: int = field(default=1)
    condition: threading.Condition = field(default=threading.Condition(),
                                           init=False)

    def acquire(self):
        '''
        This method acquires the lock for the condition variable before
        decrementing the counter by one, then it checks if the counter is
        below zero and sets the thread to sleep if true.  Otherwise, it
        releases the lock.

        '''

        # acquire the lock for the condition variable with the context manager
        with self.condition:
            # decrement the counter
            self.counter -= 1

            # check if the counter is below zero
            # if so, set the thread to sleep
            # otherwise, release the lock
            if self.counter < 0:
                self.condition.wait()

        return

    def release(self):
        '''
        This method acquires the condition lock and increments the counter by
        one, notifies a single sleeping thread, and releases the lock.
        '''

        # acquire the lock for the condition variable with the context manager
        with self.condition:
            # increment the counter
            self.counter += 1

            # notify a single sleeping thread
            self.condition.notify()

        return

    # Make the Semaphore class a context manager
    __enter__ = acquire
    __exit__ = release


class Fork(Semaphore):
    '''
    A Fork class that inherits from the Semaphore class.  This class is used
    to represent a fork in the dining philosophers problem.  It has a counter
    that is used to determine if the fork is available or not.  It also has a
    condition variable that is used to make incrementing and decrementing the
    counter thread safe (an atomic operation).

    Attributes:
        counter: An integer that represents the number of threads that are
            currently waiting on the condition variable.
        condition: A condition variable that is used to signal threads that
            the counter is 0.
        fork_id: An integer that represents the id of the fork.
    '''

    def __init__(self, fork_id):
        '''
        This method initializes the fork with the fork_id.
        '''

        # Initialize the super with a counter of 1
        # to show that only 1 thread can use the fork at a time
        super().__init__(1)

        # initialize the fork with the fork_id
        self.fork_id = fork_id
        return


class Philosopher(threading.Thread):
    '''
    This is a class that represents a philosopher.  It inherits from the
    threading.Thread class. It has a philosopher_id, a left_fork, and a right_fork.

    This is the base philosopher class that is used to create the
    philosophers and in this one the running function creates a deadlock as
    no solution is used.

    '''

    # a class attribute to signal that the philosophers are running
    is_running = True

    def __init__(self, philosopher_id: int, left_fork: Fork, right_fork: Fork,
                 fork_pause_time: float = 0.5, times_to_eat: int = 2):
        '''
        This method initializes a Philosopher object.

        Parameters:
            philosopher_id: An integer that represents the philosopher's id.
            left_fork: The left fork of the philosopher.
            right_fork: The right fork of the philosopher.
            fork_pause_time: The time that the philosopher will pause between
                            `eating` a meal.
            times_to_eat: The number of times the philosopher will eat.

        '''
        super().__init__(name=f"Philosopher {philosopher_id}")
        self.philosopher_id = philosopher_id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.fork_pause_time = fork_pause_time
        self.times_to_eat = times_to_eat
        self.times_eaten = 0

        # A bool to be used to toggle the philosopher running per instance
        self.philosopher_running = True

    def think(self):
        '''
        This method simulates thinking by sleeping for a random amount of
        time, between 0.02 and 0.6 seconds.
        '''
        print(f"\t\t{self.name} is thinking...")
        time.sleep(random.uniform(0.2, 0.6))
        return

    def eat(self):
        '''
        This method simulates eating by sleeping for a random amount of
        time, between 0.02 and 0.6 seconds.
        '''
        print(f"\t\t{self.name} is eating...")
        time.sleep(random.uniform(0.2, 0.6))
        return

    def take_left_fork(self):
        '''
        This method takes the left fork of the philosopher.
        '''
        print(
            f"\t\t{self.name} is taking left fork  {self.left_fork.fork_id} ...")
        self.left_fork.acquire()
        print(f"\t\t{self.name} is using left fork {self.left_fork.fork_id} ...")

        # Pause for fork_pause_time seconds
        time.sleep(self.fork_pause_time)

        return

    def take_right_fork(self):
        '''
        This method takes the right fork of the philosopher.
        '''
        print(
            f"\t\t{self.name} is taking right fork {self.right_fork.fork_id} ...")
        self.right_fork.acquire()
        print(
            f"\t\t{self.name} is using right fork {self.right_fork.fork_id} ...")

        # Pause for fork_pause_time seconds
        time.sleep(self.fork_pause_time)

        return

    def put_left_fork(self):
        '''
        This method puts the left fork of the philosopher.
        '''
        print(
            f"\t\t{self.name} is putting left fork {self.left_fork.fork_id} down ...")
        self.left_fork.release()
        print(
            f"\t\t{self.name} is done with left fork {self.left_fork.fork_id} ...")

        return

    def put_right_fork(self):
        '''
        This method puts the right fork of the philosopher.
        '''
        print(
            f"\t\t{self.name} is putting right fork {self.right_fork.fork_id} down ...")
        self.right_fork.release()
        print(
            f"\t\t{self.name} is done with right fork {self.right_fork.fork_id} ...")

        return

    def run(self):
        '''
        This method runs the philosopher.
        '''
        while self.is_running and self.philosopher_running and self.times_eaten < self.times_to_eat:
            self.think()
            self.take_left_fork()
            self.take_right_fork()
            self.eat()
            self.put_right_fork()
            self.put_left_fork()

            self.times_eaten += 1

            print(f"\t{self.name} is done eating and thinking...")

        return


class PhilosopherAsym(Philosopher):
    '''
    This is a class that represents a PhilosopherAsym.  It inherits from the
    Philosopher. It has a philosopher_id, a left_fork, and a right_fork.

    This is the PhilosopherAsym class that is used to create an Asymmetric
    solution to the dining philosophers problem. In this solution odd
    philosophers pick up left then right, even philosophers pick up right
    then left.



    '''

    def __init__(self, philosopher_id: int, left_fork: Fork, right_fork: Fork,
                 fork_pause_time: float = 0.5):
        '''
        This method initializes a PhilosopherAsym object.

        Parameters:
            philosopher_id: An integer that represents the philosopher's id.
            left_fork: The left fork of the philosopher.
            right_fork: The right fork of the philosopher.
            fork_pause_time: The time that the philosopher will pause between
        '''
        super().__init__(philosopher_id, left_fork, right_fork, fork_pause_time)
        return

    # Override the run method
    def run(self):
        '''
        This method runs the philosophers in an asymmetric manner, where
        odd philosophers pick up left then right, and even philosophers pick
        up right then left.
        '''

        while self.is_running and self.philosopher_running and self.times_eaten < self.times_to_eat:

            self.think()

            if self.philosopher_id % 2 == 0:
                self.take_left_fork()
                self.take_right_fork()
                self.eat()
                self.put_right_fork()
                self.put_left_fork()
            else:
                self.take_right_fork()
                self.take_left_fork()
                self.eat()
                self.put_left_fork()
                self.put_right_fork()

            print(f"\t{self.name} is done eating and thinking...")

            self.times_eaten += 1

        return


class PhilosopherEatCS(Philosopher):

    def __init__(self, philosopher_id: int, left_fork: Fork, right_fork: Fork,
                 left_eating: threading.Condition,
                 right_eating: threading.Condition,
                 fork_pause_time: float = 0.5):
        '''
        This method initializes a PhilosopherAsym object.

        Parameters:
            philosopher_id: An integer that represents the philosopher's id.
            left_fork: The left fork of the philosopher.
            right_fork: The right fork of the philosopher.
            left_eating: The semaphore that represents if left neighbor is eating.
            right_eating: The semaphore that represents if right neighbor is eating.
            fork_pause_time: The time that the philosopher will pause between
        '''
        super().__init__(philosopher_id, left_fork, right_fork, fork_pause_time)
        self.left_eating = left_eating
        self.right_eating = right_eating
        return

    # Override the run method
    def run(self):
        '''
        This method runs the philosophers in a way where the philosopher waits
        for both forks to be avalible before eating. (entering the critical section)

        '''
        while self.is_running and \
                self.philosopher_running and\
                self.times_eaten < self.times_to_eat:
            self.think()

            with self.left_eating:
                with self.right_eating:
                    self.take_left_fork()
                    self.take_right_fork()
                    self.eat()
                    self.put_right_fork()
                    self.put_left_fork()

            self.times_eaten += 1

            print(f"\t{self.name} is done eating and thinking...")

        return


def diningPhilosophers(philosopher_amt: int = 5, simulation_time: int = 20,
                       fork_pause_time: float = 0.5,
                       sim_type: str = 'deadlock'):
    '''
    This method simulates the dining philosophers problem.

    Args:
         philosopher_amt: The number of philosophers to simulate.

        simulation_time: The number of seconds to simulate. sim_type: The type
                of simulation to run.  Can be 'deadlock', 'asymetric' or 'complex'.

        fork_pause_time: The time that the philosopher will pause between
    '''

    # Get correct philosopher object
    if sim_type == 'deadlock':
        philosopher_obj = Philosopher
    elif sim_type == 'asymetric':
        philosopher_obj = PhilosopherAsym
    elif sim_type == 'complex':
        philosopher_obj = PhilosopherEatCS

    # create the forks
    left_forks = [Fork(i) for i in range(philosopher_amt)]
    right_forks = [left_forks[(i + 1) % philosopher_amt] for i in
                   range(philosopher_amt)]

    # Create a list of philosophers
    if sim_type != 'complex':

        philosophers = [
            philosopher_obj(i, left_forks[i], right_forks[i], fork_pause_time)
            for i in range(philosopher_amt)]

    # If sim
    else:
        # Make eating locks
        left_eating = [threading.Condition() for _ in range(philosopher_amt)]
        right_eating = [left_eating[(i + 1) % philosopher_amt] for i in
                        range(philosopher_amt)]

        # Create philosophers
        philosophers = [philosopher_obj(i,
                                        left_forks[i],
                                        right_forks[i],
                                        left_eating[i],
                                        right_eating[i],
                                        fork_pause_time) for i in
                        range(philosopher_amt)]

    print("\nStarting the Dining Philosophers Simulation...")

    # Start the philosophers
    for philosopher in philosophers:
        philosopher.start()

    # Wait for the simulation_time
    time.sleep(simulation_time)
    philosopher_obj.is_running = False
    print("\nEnding the Dining Philosophers Simulation...")

    # time.sleep(philosopher_amt*2.5)

    if sim_type != 'deadlock':
        for philosopher in philosophers:
            philosopher.join()

    print("The Dining Philosophers Simulation has ended.")

    # See if all philosophers have eaten the correct number of times
    all_eaten = True
    for philosopher in philosophers:
        if philosopher.times_eaten != philosopher.times_to_eat:
            print(
                f"\n{philosopher.name} has eaten {philosopher.times_eaten} times instead of {philosopher.times_to_eat} times.")
            all_eaten = False

    if all_eaten:
        print("\nAll philosophers have eaten the correct number of times.")

    return


def createWaitForGraph(resource_graph: nx.DiGraph):
    '''
    This method creates a wait-for graph of the resources in the resource_graph.
    '''

    # Create the graph
    wait_for_graph = resource_graph.copy()

    # Remove all fork nodes and concat edges between waiting philosophers
    fork_nodes = [node for node in wait_for_graph.nodes() if
                  node.startswith('F')]

    # get all edges
    # edges = list(wait_for_graph.edges())

    for node in fork_nodes:

        node_edges_in = list(wait_for_graph.in_edges(node))
        node_edges_out = list(wait_for_graph.out_edges(node))

        # If there are edges in and out
        if node_edges_in and node_edges_out:

            # Connect the philosophers
            for edge_in in node_edges_in:
                for edge_out in node_edges_out:
                    wait_for_graph.add_edge(edge_in[0], edge_out[1])

        # Remove the fork node
        wait_for_graph.remove_node(node)

    return wait_for_graph


def createGraphs(sim_output: list, resource_graph: nx.DiGraph) -> tuple:
    '''
    Function to create a list of directed resource graphs for each step in
    the simulation from the base resource graph

    Args:
        sim_output: The list of simulation outputs
        resource_graph: The base resource graph to create the directed resource graphs from

    Returns:
        A list of directed resource graphs
    '''

    # Create a list of graphs
    directed_resource_graphs = []
    wait_for_graphs = []

    # Create a new graph
    new_graph = resource_graph.copy()

    for line in sim_output:

        # If has is in the line continue
        if ' has ' in line:
            continue

        split_line = line.split(' is')

        if len(split_line) > 1 and "thinking" not in split_line[
            1] and "eating" not in split_line[1] and "putting" not in \
                split_line[1]:

            # Get the philosopher id
            philosopher_id = f"P {int(split_line[0].split(' ')[-1])}"

            # Get the action of the philosopher
            action = split_line[1].split(' ')[1]

            # Get the id of the fork

            fork_id = f"F {int(split_line[1].split(' ')[-2])}"

            # Remove old edge between philosopher and fork
            try:
                new_graph.remove_edge(philosopher_id, fork_id)
            except nx.exception.NetworkXError:
                pass
            try:
                new_graph.remove_edge(fork_id, philosopher_id)
            except nx.exception.NetworkXError:
                pass

            # add to new graph based on philosopher id , action and fork id
            # TODO: add atributes to the graph edge
            if action == 'taking':
                new_graph.add_edge(philosopher_id, fork_id)
            elif action == 'using':

                # Get all other edges connected to the fork
                # that are going into it
                edges = list(new_graph.edges(fork_id))

                # flip the edges that are "using"
                for edge in edges:
                    new_graph.remove_edge(edge[0], edge[1])
                    new_graph.add_edge(edge[1], edge[0])

                new_graph.add_edge(fork_id, philosopher_id)
            # elif action == 'done':
            #     graph.remove_edge(philosopher_id, fork_id)

            # Create wait-for graph
            wait_for_graph = createWaitForGraph(new_graph)

            wait_for_graphs.append(wait_for_graph)
            directed_resource_graphs.append(new_graph)

            new_graph = new_graph.copy()

    return (directed_resource_graphs, wait_for_graphs)


def diningPhilosophersGraphAfter(philosopher_amt: int = 5,
                                 simulation_time: int = 20,
                                 fork_pause_time: float = 0.5,
                                 sim_type: str = 'deadlock'):
    '''
    This method simulates the dining philosophers problem and graphs it with
    a wait-for or directed resource graph using networknx. The graphs are produced
    after the simulation has finished.

    Args:
         philosopher_amt: The number of philosophers to simulate.

        simulation_time: The number of seconds to simulate. sim_type: The type
                of simulation to run.  Can be 'deadlock', 'asymetric' or 'complex'.

        fork_pause_time: The time that the philosopher will pause between
    '''

    # Get correct philosopher object
    if sim_type == 'deadlock':
        philosopher_obj = Philosopher
    elif sim_type == 'asymetric':
        philosopher_obj = PhilosopherAsym
    elif sim_type == 'complex':
        philosopher_obj = PhilosopherEatCS

    # create the forks
    left_forks = [Fork(i) for i in range(philosopher_amt)]
    right_forks = [left_forks[(i + 1) % philosopher_amt] for i in
                   range(philosopher_amt)]

    # Create a list of philosophers
    if sim_type != 'complex':

        philosophers = [
            philosopher_obj(i, left_forks[i], right_forks[i], fork_pause_time)
            for i in range(philosopher_amt)]

    # If sim
    else:
        # Make eating locks
        left_eating = [threading.Condition() for _ in range(philosopher_amt)]
        right_eating = [left_eating[(i + 1) % philosopher_amt] for i in
                        range(philosopher_amt)]

        # Create philosophers
        philosophers = [philosopher_obj(i,
                                        left_forks[i],
                                        right_forks[i],
                                        left_eating[i],
                                        right_eating[i],
                                        fork_pause_time) for i in
                        range(philosopher_amt)]

    # Create directed resource graph base
    directed_resource_graph = nx.DiGraph()
    for i in range(philosopher_amt):
        directed_resource_graph.add_node(f"P {philosophers[i].philosopher_id}")
        directed_resource_graph.add_node(f"F {i}")

    # Create graph Maker
    # directed_resource_graph_maker = GraphMaker(directed_resource_graph)
    # directed_resource_graph_maker.start()

    print("\nStarting the Dining Philosophers Simulation...")

    # use contextlib to redirect stdout to a StringIO object
    sim_output = io.StringIO()
    with contextlib.redirect_stdout(sim_output):

        # Start the philosophers
        for philosopher in philosophers:
            philosopher.start()

        # Wait for the simulation_time
        time.sleep(simulation_time)
        philosopher_obj.is_running = False
        print("\nEnding the Dining Philosophers Simulation...")

    # # Set directed resource graph maker to not running
    # directed_resource_graph_maker.is_running = False
    #
    # # Wait for the directed resource graph maker to finish
    # directed_resource_graph_maker.join()

    print("\nThe Dining Philosophers Simulation has ended.")

    # Split the output into lines
    lines = sim_output.getvalue().split('\n')

    # Print the lines
    for line_num, line in enumerate(lines):
        print(f"{line_num} {line}")

    # Filter output

    # filtered_lines = []
    # for line in lines:
    #     split_line = line.split(' is')
    #
    #     if len(split_line) > 1 and "thinking" not in split_line[1] and "eating" not in split_line[1] and "putting" not in split_line[1]:
    #         filtered_lines.append(line)

    # Create a list of graphs

    di_graphs = createGraphs(lines, directed_resource_graph)
    return di_graphs
    #
    # # define color map. philosopher = red, fork = green
    # color_map_resources = ["red"  if "P" in node else "green" for node in directed_resource_graph]
    #
    # directed_resource_graphs = di_graphs[0]
    # wait_for_graphs = di_graphs[1]
    #
    # # Plot the graphs
    # for graph_resource, wait_for_graph in zip(directed_resource_graphs,
    #                                           wait_for_graphs):
    #
    #     # Plot directed resource graph
    #     nx.draw_circular(graph_resource, with_labels=True, node_color = color_map_resources)
    #     plt.show()
    #
    #     # Clear the plot
    #     plt.clf()
    #
    #     # Plot wait for graph.
    #     nx.draw_circular(wait_for_graph,
    #                      with_labels=True,
    #                      node_color="red")
    #     plt.show()
    #     # time.sleep(0.001)
    #
    # # find all cycles in wait for graphs
    # graph_cycles = []
    # for wait_for_graph in wait_for_graphs:
    #     cycles = list(nx.simple_cycles(wait_for_graph))
    #     graph_cycles.append(cycles)

    return


def detectDeadlock(wait_for_graphs: list) -> bool:
    '''
    Detects deadlock in the wait for graphs
    Args:
        wait_for_graphs (list): list of wait for graphs

    Returns:
        bool: True if deadlock detected, False otherwise

    '''
    # find all cycles in wait for graphs
    graph_cycles = []
    for wait_for_graph in wait_for_graphs:
        cycles = list(nx.simple_cycles(wait_for_graph))
        graph_cycles.append(cycles)

    # If any cycles exist, then there is a deadlock
    if any(cycles for cycles in graph_cycles):
        return True

    return False


class GraphMakerProcess(multiprocessing.Process):
    '''
    Process to create directed resource graph
    '''

    def __init__(self, directed_resource_graph, moves_queue, deadlock_queue):
        multiprocessing.Process.__init__(self, name="GraphMakerProcess")
        self.directed_resource_graph = directed_resource_graph
        self.is_running = True
        self.moves_queue = moves_queue
        self.deadlock_queue = deadlock_queue

    def run(self):

        current_moves = []
        while self.is_running:

            # get moves from the moves queue
            moves_list = self.moves_queue.get()

            if len(moves_list) > 1 and moves_list != current_moves:
                current_moves = moves_list
                di_graphs = createGraphs(
                    current_moves, self.directed_resource_graph)

                wait_for_graphs = di_graphs[1]

                # Check for deadlock
                if detectDeadlock(wait_for_graphs):
                    self.deadlock_queue.put(True)

            pass


class GraphMakerThread(threading.Thread):
    '''
    This class is used to create a directed graph of resources and wait-for graph
    '''

    # Create running class attribute
    is_running = True

    def __init__(self, resource_graph: nx.DiGraph,
                 moves_queue: multiprocessing.Queue):
        '''
        This method initializes a DirectedResourceGraphMaker object.

        Parameters:
            resource_graph: The graph to add the resources to.
            queue: The queue to add sys.out to.
        '''
        super().__init__(name=f"GraphMakerThread")
        self.resource_graph = resource_graph
        self.moves_queue = moves_queue
        return

    def run(self):
        '''
        This method runs the DirectedResourceGraphMaker object.
        '''

        captured_output = io.StringIO()  # Create StringIO object
        while self.is_running:
            with contextlib.redirect_stdout(captured_output):

                time.sleep(0.001)

            lines = captured_output.getvalue().split('\n')

            # Add the lines to the queue
            self.moves_queue.put(lines)

        return


class DeadlockHandler(threading.Thread):

    # Create running class attribute
    is_running = True

    def __init__(self, deadlock_queue: multiprocessing.Queue,
                 forks: list,
                 philosophers: list,
                 deadlock_sleep_time: int):

        super().__init__(name=f"DeadlockHandler")
        self.deadlock_queue = deadlock_queue
        self.forks = forks
        self.philosophers = philosophers
        self.deadlock_sleep_time = deadlock_sleep_time
        return

    def run(self):

        while self.is_running:

            # get data from deadlock queue
            if not self.deadlock_queue.empty():
                deadlock_signal = self.deadlock_queue.get()
                if deadlock_signal:

                    # Raise warning about deadlock
                    warnings.warn("Deadlock detected")

                    # Chose a random philosopher to turn off
                    random_philosopher = random.choice(self.philosophers)
                    random_philosopher.is_running = False

                    time.sleep(self.deadlock_sleep_time)

                    random_philosopher.is_running = True

        return


def diningPhilosophersCatchDeadlock(philosopher_amt: int = 5,
                                    simulation_time: int = 20,
                                    fork_pause_time: float = 0.5,
                                    sim_type: str = 'deadlock',
                                    deadlock_sleep_time: float = 5):

    # Get correct philosopher object
    if sim_type == 'deadlock':
        philosopher_obj = Philosopher
    elif sim_type == 'asymetric':
        philosopher_obj = PhilosopherAsym
    elif sim_type == 'complex':
        philosopher_obj = PhilosopherEatCS

    # create the forks
    left_forks = [Fork(i) for i in range(philosopher_amt)]
    right_forks = [left_forks[(i + 1) % philosopher_amt] for i in
                   range(philosopher_amt)]

    # Create a list of philosophers
    if sim_type != 'complex':

        philosophers = [
            philosopher_obj(i, left_forks[i], right_forks[i], fork_pause_time)
            for i in range(philosopher_amt)]

    # If sim
    else:
        # Make eating locks
        left_eating = [threading.Condition() for _ in range(philosopher_amt)]
        right_eating = [left_eating[(i + 1) % philosopher_amt] for i in
                        range(philosopher_amt)]

        # Create philosophers
        philosophers = [philosopher_obj(i,
                                        left_forks[i],
                                        right_forks[i],
                                        left_eating[i],
                                        right_eating[i],
                                        fork_pause_time) for i in
                        range(philosopher_amt)]

    # Create directed resource graph base
    directed_resource_graph = nx.DiGraph()
    for i in range(philosopher_amt):
        directed_resource_graph.add_node(f"P {philosophers[i].philosopher_id}")
        directed_resource_graph.add_node(f"F {i}")

    # Initialize the multiprocessing queues
    moves_queue = multiprocessing.Queue()
    deadlock_queue = multiprocessing.Queue()

    # Create graph Maker thread
    graph_maker_thread = GraphMakerThread(directed_resource_graph,
                                          moves_queue=moves_queue)

    # Create the graph maker process
    graph_maker_process = GraphMakerProcess(directed_resource_graph,
                                            moves_queue=moves_queue,
                                            deadlock_queue=deadlock_queue)

    # Create the deadlock handler thread
    deadlock_handler_thread = DeadlockHandler(
        deadlock_queue,
        forks=left_forks,
        philosophers=philosophers,
        deadlock_sleep_time=deadlock_sleep_time)

    print("\nStarting the Dining Philosophers Simulation...")

    # Start the graph maker
    graph_maker_thread.start()

    # Start the graph maker process
    graph_maker_process.start()

    deadlock_handler_thread.start()

    time.sleep(2)

    # Start the philosophers
    for philosopher in philosophers:
        philosopher.start()

    # Wait for the simulation_time
    time.sleep(simulation_time)
    philosopher_obj.is_running = False
    print("\nEnding the Dining Philosophers Simulation...")

    time.sleep(5)

    # Setgraph maker to not running
    graph_maker_thread.is_running = False

    # Wait for the graph maker to finish
    graph_maker_thread.join()

    # Set graph maker to not running
    graph_maker_process.is_running = False

    print("Setting graph maker pros to not running")

    # Wait for the graph maker process to finish
    # graph_maker_process.join()

    # Set deadlock handler to not running
    deadlock_handler_thread.is_running = False
    print("Setting graph maker thread to not running")

    # Wait for the deadlock handler to finish
    # deadlock_handler_thread.join()

    # Close the queue
    moves_queue.close()
    deadlock_queue.close()

    print("\nThe Dining Philosophers Simulation has ended.")

    # See if all philosophers have eaten the correct number of times
    all_eaten = True
    for philosopher in philosophers:
        if philosopher.times_eaten != philosopher.times_to_eat:
            print(
                f"\n{philosopher.name} has eaten {philosopher.times_eaten} times instead of {philosopher.times_to_eat} times.")
            all_eaten = False

    if all_eaten:
        print("\nAll philosophers have eaten the correct number of times.")

    return


def main():
    # diningPhilosophers(5, 20, 1.6, 'asymetric')
    tttt = diningPhilosophersCatchDeadlock(5, 15, 1.6, 'deadlock')
    return


if __name__ == '__main__':
    main()
