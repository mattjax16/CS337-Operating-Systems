import threading
import random
import time
import contextlib
import io
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import multiprocessing
import warnings
import re
import sys
import numpy as np
import networkx as nx
from dataclasses import dataclass, field

# plt.rcParams["figure.autolayout"] = True




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
        print(f"\t\t{self.name} is taking left fork  {self.left_fork.fork_id} ...")
        self.left_fork.acquire()
        print(f"\t\t{self.name} is using left fork {self.left_fork.fork_id} ...")

        # Pause for fork_pause_time seconds
        time.sleep(self.fork_pause_time)

        return

    def take_right_fork(self):
        '''
        This method takes the right fork of the philosopher.
        '''
        print(f"\t\t{self.name} is taking right fork {self.right_fork.fork_id} ...")
        self.right_fork.acquire()
        print(f"\t\t{self.name} is using right fork {self.right_fork.fork_id} ...")

        # Pause for fork_pause_time seconds
        time.sleep(self.fork_pause_time)

        return

    def put_left_fork(self):
        '''
        This method puts the left fork of the philosopher.
        '''
        print(f"\t\t{self.name} is putting left fork {self.left_fork.fork_id} down ...")
        self.left_fork.release()
        print(f"\t\t{self.name} is done with left fork {self.left_fork.fork_id} ...")

        return

    def put_right_fork(self):
        '''
        This method puts the right fork of the philosopher.
        '''
        print(f"\t\t{self.name} is putting right fork {self.right_fork.fork_id} down ...")
        self.right_fork.release()
        print(f"\t\t{self.name} is done with right fork {self.right_fork.fork_id} ...")

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

    # Create a list of graphs and used lines
    directed_resource_graphs = []
    wait_for_graphs = []
    graph_lines = []

    # Create a new graph
    new_graph = resource_graph.copy()

    for line in sim_output:

        # If has is in the line continue
        if ' has' in line:
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

            # Create wait-for graph
            wait_for_graph = createWaitForGraph(new_graph)

            wait_for_graphs.append(wait_for_graph)
            directed_resource_graphs.append(new_graph)

            # add line to graph_lines list
            graph_lines.append(line)

            new_graph = new_graph.copy()

    return (directed_resource_graphs, wait_for_graphs, graph_lines)

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



    print("\nThe Dining Philosophers Simulation has ended.")

    # Split the output into lines
    lines = sim_output.getvalue().split('\n')

    # Print the lines
    for line_num, line in enumerate(lines):
        print(f"{line_num} {line}")

    di_graphs = createGraphs(lines, directed_resource_graph)


    return  di_graphs



# Make graph function
def plotGraphs(frame, ax, directed_resource_graphs, wait_for_graphs, graph_lines,
               color_map):

        # Clear all axes
        for a in ax:
            a.clear()

        ax[0].set_title("Directed Resource Graph")
        ax[1].set_title("Wait-for Graph")

        # Plot the directed resource graph
        nx.draw_circular(directed_resource_graphs[frame],
                ax=ax[0],
                node_color=color_map,
                with_labels=True)

        # Plot the wait-for graph
        nx.draw_circular(wait_for_graphs[frame],
                ax=ax[1],
                node_color="red",
                with_labels=True)

        # Clean the line
        clean_line = re.sub(r'[\n\t\s]*', ' ', graph_lines[frame])
        # add the action that cause each graph to change
        ax[0].text(0.65, -1.2, f"Action {frame}.     {clean_line}", fontsize=8)

        # call tight layout
        plt.tight_layout()

        new_ax = ax.copy()


        return new_ax

def makeGraphsGif(di_graphs: list, gif_name: str = "animation") -> None:


    # # initialize fig and axis
    # fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    fig = plt.figure(figsize=(10, 5))
    #
    # get the subplots to update when generating the animation
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax = [ax1, ax2]



     # define color map. philosopher = red, fork = green
    color_map_resources = ["red" if "P" in node else "green" for node in
                           di_graphs[0][0].nodes]


    # get the graphs
    directed_resource_graphs = di_graphs[0]
    wait_for_graphs = di_graphs[1]

    # get the graph lines
    graph_lines = di_graphs[2]


    ani = animation.FuncAnimation(fig, plotGraphs, frames=np.arange(len(di_graphs[0])),
                                             interval=1000, repeat=True,
                                  fargs=(ax, directed_resource_graphs, wait_for_graphs, graph_lines, color_map_resources))

    writergif = animation.PillowWriter(fps=1.5)
    ani.save(f"Graph_Gifs/{gif_name}.gif", writer=writergif)

    return

def main():
    sol2_graphs = diningPhilosophersGraphAfter(philosopher_amt=5,
                                                   simulation_time=25,
                                                   fork_pause_time=0.6,
                                                   sim_type='complex')

    makeGraphsGif(sol2_graphs,"sol2_animation")
    # showAnimation(deadlock_graphs)
    return


if __name__ == '__main__':
    main()