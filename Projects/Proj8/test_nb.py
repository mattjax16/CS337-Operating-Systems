# %% md

# Test Notebook

# %%


import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def makeReferenceStringWithoutLocality(length: int = 100) -> np.ndarray:
    '''
    This is a function to make a reference string with random numbers 0 -
    length of size length.


    Args:
        length (int): The length of the reference string.


    Returns:
        reference_string (np.ndarray): The reference string.
    '''

    # Check that the length is positive
    if length <= 0:
        raise ValueError("The length must be positive.")

    # Make the reference string
    reference_string = np.random.choice(np.arange(length),
                                        size=length,
                                        replace=True)

    return reference_string


def makeReferenceStringWithLocality(length: int = 100) -> np.ndarray:
    '''
    This is a function to make a reference string with of size length and
    numbers index plus a random int -3 - 3


    Args:
        length (int): The length of the reference string.


    Returns:
        reference_string (np.ndarray): The reference string.
    '''

    # Check that the length is positive
    if length <= 0:
        raise ValueError("The length must be positive.")

    # Make the reference string
    reference_string = np.arange(length) + np.random.choice(np.arange(-3, 4),
                                                            length,
                                                            True)

    # Check that no references are negative or greater than the length
    # If they are set them to a proper value
    for i in range(len(reference_string)):
        if reference_string[i] < 0:
            reference_string[i] = 0
        elif reference_string[i] >= length:
            reference_string[i] = length - 1

    return reference_string


class PageReplacementAlg():
    '''
    This is a class to represent a page replacement algorithm.
    '''

    def __init__(self) -> None:

        self.name = "Page Replacement Algorithm"

    def run(self,
            reference_string: np.ndarray,
            frames: int = 5) -> np.ndarray:
        '''

        This is the base function for any page replacement algorithm. The
        solutions are run with their own unique algorithm function

        Args:
            reference_string (np.ndarray): The reference string.
            frames (int): The number of frames.

        Returns:

        '''

        # Check that frames is positive
        if frames <= 0:
            raise ValueError("The frames must be positive.")

        # Make the page table key
        page_table_key = ["Time Stamp", "Reference Sting"] + [
            "Frame " + str(i) for i in range(frames)] + ["Page Fault",
                                                         "Removed Page"]

        page_table_key = np.array(
            page_table_key, dtype=str).reshape(
            (len(page_table_key), 1))

        # Make the time stamps
        time_stamps = np.arange(len(reference_string))

        # Make the frame table
        frames_table = np.zeros((frames, len(time_stamps)), dtype=int) - 1

        # Make the page fault and removed page
        page_fault = np.zeros(len(time_stamps), dtype=int)
        removed_page = np.zeros(len(time_stamps), dtype=int) - 1

        # loop through the reference string and run the FCFS algorithm
        for index, page in enumerate(reference_string):

            # if the index is not 0 copy the precious frames to the current
            # frame time stamp
            if index != 0:
                frames_table[:, index] = frames_table[:, index - 1]

            # Check if the page is in the frame table at the current time stamp
            if np.any(frames_table[:, index] == page):

                # If there is show that a page wasnt removed
                removed_page[index] = -1

            # If the page is not in the frames at the current time stamp
            else:

                # Set the page fault to 1 to show one has occurred
                page_fault[index] = 1

                # Check if there is a free space in the frame table
                if np.any(frames_table[:, index] == -1):

                    # If there is, set the requested page to the first free
                    # space
                    free_space = np.where(frames_table[:, index] == -1)[0][0]
                    frames_table[free_space, index] = page

                    # Show that a page wasnt removed
                    removed_page[index] = -1

                # If there is not, run the algorithm to find the page to remove
                else:
                    remove_page_idx = self.algorithm(frames_table,
                                                     reference_string,
                                                     index)

                    page_to_be_removed = frames_table[remove_page_idx, index]

                    # Set the removed page to the page to be removed
                    if not isinstance(page_to_be_removed, np.ndarray):
                        removed_page[index] = page_to_be_removed
                    elif page_to_be_removed.size > 1:
                        removed_page[index] = page_to_be_removed[0]
                    else:
                        removed_page[index] = page_to_be_removed

                    # set the new page
                    frames_table[remove_page_idx, index] = page

        # Combine all the data into a table
        page_table = np.vstack((time_stamps, reference_string, frames_table,
                                page_fault, removed_page))

        page_table = np.hstack((page_table_key, page_table))

        return page_table

    # Generic algorithm to find the page to remove

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:

        return 0


class FIFO(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "FCFS"

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:
        '''

        This is the FCFS algorithm. It will find the first page in the
        current frames that entered the frame table and remove it.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed

        '''

        # go backwards through reference string and find the first page that was inserted
        # into the frame table

        pages_added_queue = []

        for i in range(index - 1, -1, -1):

            # If the pages added queue is the size of frames break out of the
            # loop
            if len(pages_added_queue) >= frames_table.shape[0] and \
                    reference_string[i] not in pages_added_queue:
                break

            if reference_string[i] not in pages_added_queue and \
                    np.any(frames_table[:, index] == reference_string[i]):

                pages_added_queue.append(reference_string[i])

            # if it is in the queue remove it and append it to the end of the
            # queue
            elif reference_string[i] in pages_added_queue and \
                    np.any(frames_table[:, index] == reference_string[i]):

                pages_added_queue.remove(reference_string[i])
                pages_added_queue.append(reference_string[i])

        # pop the first page in the queue
        page_to_be_removed = pages_added_queue.pop(-1)

        # find the index of the page to be removed
        remove_page_idx = list(
            np.where(frames_table[:, index] == page_to_be_removed)[0])

        rp1 = remove_page_idx[0]

        return rp1


class LRU(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "LRU"

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:
        '''

        This is the LRU algorithm. It will find the least recently used page in the
        current frames and remove it.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed

        '''

        # Get the current pages
        current_pages = frames_table[:, index]

        time_last_used = np.array([-1] * frames_table.shape[0])

        # for each page in the current pages find the last time step that it
        # was used
        for idx, page in enumerate(current_pages):

            # loop backward through the reference string until the page is
            # found
            for i in range(index - 1, -1, -1):
                if reference_string[i] == page:
                    time_last_used[idx] = page
                    break

        # Get the least recently used page
        remove_idx = np.argmin(time_last_used)

        return remove_idx


class OPTIMAL(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "OPT"

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:
        '''
        This is the Optimal page replacement algorithm.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed
        '''

        # Get the current pages
        current_pages = frames_table[:, index]

        time_next_used = np.array([frames_table.shape[0] * 100] *
                                  frames_table.shape[0])

        # for each page in the current pages find the last time step that it
        # was used
        for idx, page in enumerate(current_pages):

            # loop through the reference string until the next time the page
            # is used is found

            for i in range(index + 1, reference_string.size):
                if reference_string[i] == page:
                    time_next_used[idx] = i
                    break

        # Get the least recently used page
        remove_idx = np.argmax(time_next_used)

        return remove_idx


class LFU(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "LFU"

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:
        '''

        This is the LFU algorithm. It will find the least frequently used page in the
        current frames and remove it.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed

        '''

        # Get the current pages
        current_pages = frames_table[:, index]

        times_used = np.array([0] * frames_table.shape[0])

        # for each page in the current pages and get the
        # count of the number of times the page was used
        for idx, page in enumerate(current_pages):

            times_used[idx] = np.count_nonzero(
                reference_string[:index] == page)

        # Get the least recently used page
        remove_idx = np.argmin(times_used)

        return remove_idx


class MFU(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "MFU"

    def algorithm(self, frames_table: np.ndarray, reference_string: np.ndarray,
                  index: int) -> int:
        '''

        This is the MFU algorithm. It will find the most frequently used page in the
        current frames and remove it.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed

        '''

        # Get the current pages
        current_pages = frames_table[:, index]

        times_used = np.array([0] * frames_table.shape[0])

        # for each page in the current pages and get the
        # count of the number of times the page was used
        for idx, page in enumerate(current_pages):
            times_used[idx] = np.count_nonzero(
                reference_string[:index] == page)

        # Get the most recently used page
        remove_idx = np.argmax(times_used)

        return remove_idx


class LFUDA(PageReplacementAlg):

    def __init__(self) -> None:
        super().__init__()
        self.name = "LFUDA"

    def algorithm(self, frames_table: np.ndarray,
                  reference_string: np.ndarray,
                  index: int) -> int:
        '''

        This is the LFUDA algorithm. It will find the least frequently used page in the
        current frames with aging included and remove it.

        Args:
            frames_table (np.ndarray): The frame table.
            reference_string (np.ndarray): The reference string.
            index (int): The current index of the reference string.

        Returns:
            int: The index of the page to be removed

        '''

        # Get the current pages
        current_pages = frames_table[:, index]

        times_used = np.array([0] * frames_table.shape[0])
        frame_ages = np.array([0] * frames_table.shape[0])

        # for each page in the current pages and get the
        # count of the number of times the page was used
        # and get the frame ages
        for idx, page in enumerate(current_pages):

            times_used[idx] = np.count_nonzero(
                reference_string[:index] == page)

            # loop backwards through the frames to get the age
            # (how long page has been in the frame)
            age = 0
            for i in range(index - 1, -1, -1):
                if np.any(frames_table[:, i] == page):
                    age += 1
                else:
                    break
            frame_ages[idx] = age

        aged_lfu = times_used + frame_ages

        # Get the least recently used page with aging
        remove_idx = np.argmin(aged_lfu)

        return remove_idx


def makeTable(table: np.ndarray, only_final_table: bool = True) -> None:
    '''

    This function will make the page table for the given algorithm.
    along with its color map

    Args:
        table (np.ndarray): The page table.
        alg_name (str): The name of the algorithm.

    Returns:
        table_plot: The plot of the page table.

    '''

    # make list to hold all the plots
    table_plots = []

    # Make the table all strings
    table = table.astype(str)

    # replace all -1 with blank spaces
    table[table == '-1'] = ' '

    # Making the colors
    grey_background = np.array(["#D5D8D8"] * table.shape[1])
    white_background = np.array(["#FFFFFF"] * table.shape[1])

    # make base table color map
    table_color_top = np.vstack((white_background, grey_background))
    frame_colors = np.repeat(
        white_background,
        table.shape[0] - 4,
        axis=0).reshape(
        table.shape[0] - 4,
        table.shape[1])
    table_color_bottom = np.vstack((grey_background, white_background))

    table_color_map = np.vstack(
        (table_color_top, frame_colors, table_color_bottom))

    # Make an empty base table for graphing
    base_table = np.copy(table)

    base_table[2:, 1:] = ' '

    table_plots.append((base_table, table_color_map))

    # Make the table for the algorithm
    updated_table = np.copy(base_table)

    # Make the updated table color map
    updated_table_color_map = np.copy(table_color_map)

    # loop through each time step making an updated table
    for i in range(1, table.shape[1]):

        # Make a copy of the base table
        updated_table = np.copy(updated_table)

        # Make the updated table
        updated_table[:, i:] = table[:, i:]

        # Copy the updated table color map
        updated_table_color_map = np.copy(updated_table_color_map)

        # Make the updated table color map
        updated_table_color_map[:, i:] = table_color_map[:, i:]

        # Find where the ref was inserted
        insert_idx = list(np.where(table[:, i] == table[1, i])[0])
        if table[1, i] == '1':
            insert_idx = insert_idx[-2]
        else:
            insert_idx = insert_idx[-1]

        # set if it had a fault
        # make it X and set cell to red
        if table[table.shape[0] - 2, i] == '1':
            updated_table[table.shape[0] - 2, i] = 'X'

            # make the  cell red
            updated_table_color_map[insert_idx, i] = '#ff002f'

            # Handle the replacement cell
            if table[-1, i] == '-1':
                updated_table[-1, i] = ' '
            else:
                updated_table[-1, i] = table[-1, i]

        # set if it had not had a fault
        # make the sell blank and set it to green
        else:
            updated_table[table.shape[0] - 2, i] = ' '

            # make the  cell green
            updated_table_color_map[insert_idx, i] = '#2deb56'

        # Add the updated table to the list of plots
        table_plots.append(
            dict([("table", updated_table), ("cmap", updated_table_color_map)]))

    if only_final_table:
        return table_plots[-1]

    return table_plots


def plotltTable(tables: tuple, alg_name: str):
    '''
    This is a function to plot the tables.

    Args:
        tables (tuple): The table to be plotted.
        alg_name (str): The name of the algorithm.

    Returns:
        None.

    '''
    # for table in tables:
    # get the table and the color map
    table = tables[-1]

    table, color_map = table

    # make figure and axes
    fig, ax = plt.subplots(figsize=(30, 30))

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    table_row_names = table[:, 0]

    table = table[:, 1:]

    row_colors = color_map[:, 0]
    color_map = color_map[:, 1:]

    # plot the table
    ax.table(cellText=table,
             cellColours=color_map,
             rowLabels=table_row_names,
             rowColours=row_colors,
             cellLoc='center')

    # set the title
    ax.set_title(alg_name)

    # fig.tight_layout()

    fig.show()

    return 1


def plotTable(tables: tuple, alg_name: str):
    '''
    This is a function to plot the tables.

    Args:
        tables (tuple): The table to be plotted.
        alg_name (str): The name of the algorithm.

    Returns:
        None.

    '''
    # for table in tables:
    # get the table and the color map

    table, color_map, stats = tables.values()

    # make the cells dict for the plotly table
    cells = {}
    cells['values'] = table[:, 1:]
    cells["fill_color"] = color_map[:, 1:]
    cells["line_color"] = 'darkslategray'
    cells["align"] = ["left", "center"]
    cells["font"] = dict(color="black", size=12)
    cells["height"] = 30

    # make the headers dict
    headers = {}
    headers['values'] = [f"<b>{t}</b>" for t in table[:, 0]]
    headers["fill_color"] = color_map[:, 0]
    headers["line_color"] = 'darkslategray'
    headers["align"] = ["center"]
    headers["font"] = dict(color="black", size=12)

    plot_table = go.Table(cells=cells,
                          header=headers,
                          columnwidth=500)

    # Make the figure
    fig = go.Figure(data=[plot_table],
                    layout=dict(title=f"{alg_name} STATS: {stats}"
                                ))

    # Show the figure using dash

    # df = pd.DataFrame(table[:, 1:].T, columns=table[:,0])
    #
    # dashT = dash_table.DataTable(df.to_dict('records'),
    #     [{"name": i, "id": i} for i in df.columns])

    fig.show()

    # app = dash.Dash()
    #
    # # app.layout = dashT
    # app.layout = html.Div([dcc.Graph(figure=fig)])
    # #
    # app.run_server(debug=True, use_reloader=False)

    return 1



def makeTables(results: dict, col_amt: int = None):
    '''
       This function will make the tables of the results of the page replacement algorithms.
       Args:
           results (dict): The results of the page replacement algorithms.
           col_amt (int): The amount of columns display

       Returns:

       '''

    # Check that the results dictionary is not empty
    if not results:
        raise ValueError("The results dictionary is empty")

    # Make result plots dictionary
    result_plots = {}

    # loop through each algorithm in the results dictionary
    for alg_name, alg_results in results.items():

        result_plots[alg_name] = []

        # Loop through all the tables in the results
        # and plot them
        for table in alg_results:

            # If col_amt is not none
            if col_amt is None:

                result_plots[alg_name].append(makeTable(table))

            else:
                cut_table = table[:, :col_amt + 1]
                result_plots[alg_name].append(makeTable(cut_table, alg_name))

    return result_plots


def plotTables(results: dict, col_amt: int = None):
    '''
    This function will plot the results of the page replacement algorithms.
    Args:
        results (dict): The results of the page replacement algorithms.
        col_amt (int): The amount of columns display

    Returns:

    '''

    # Check that the results dictionary is not empty
    if not results:
        raise ValueError("The results dictionary is empty")

    # Make result plots dictionary
    result_plots = makeTables(results, col_amt)

    print("fdfd")


def calcTableStats(table: np.ndarray):
    '''
    This function will calculate the statistics of the table.

    Args:
        table (np.ndarray): The table to be calculated.

    Returns:
        (tuple): The mean and standard deviation of the table.

    '''

    main_table = table["table"]
    page_faults = main_table[-2, 1:]
    reference_string = main_table[1, 1:]

    num_refrences = reference_string.size
    num_unique_references = np.unique(reference_string).size
    num_faults = np.count_nonzero(page_faults == "X")
    num_hits = num_refrences - num_faults

    fault_rate = num_faults / num_refrences

    hit_rate = num_hits / num_refrences

    stats_dict = {
        "num_references": num_refrences,
        "num_unique_references": num_unique_references,
        "num_faults": num_faults,
        "num_hits": num_hits,
        "fault_rate": fault_rate,
        "hit_rate": hit_rate
    }

    return ("stats", stats_dict)

    print("fdfd")


def calcTablesStats(results_tables: dict):
    '''
    This function will calculate the stats of the tables.

    Args:
        results_tables (dict): The results tables of the page replacement algorithms.

    Returns:
        stats_tables (dict): The stats tables of the page replacement algorithms.

    '''

    # Check that the results dictionary is not empty
    if not results_tables:
        raise ValueError("The results dictionary is empty")

    # Make stats tables dictionary
    stats_tables = {}

    # loop through each algorithm in the results dictionary
    for alg_name, alg_results in results_tables.items():

        stats_tables[alg_name] = []

        # Loop through all the tables in the results
        # and plot them
        for table in alg_results:
            stats = calcTableStats(table)

            table[stats[0]] = stats[1]

    return results_tables


def runPageReplacementSim(times_to_run: int = 5,
                            frames: int = 5,
                            reference_string_length: int = 100,
                            locality: bool = False,
                            algorithms: list = None) -> None:
    '''
    This is a function to simulate the page replacement algorithms.

    Args:
        times_to_run (int): The number of times to run the simulation for
        each algorithm. frames (int): The number of frames.
        reference_string_length (int): The length of the reference string.
        locality (bool): If True, the reference string will have locality.
        algorithms (list): The list of algorithms to run.

    '''

    # Checking arguments
    if list is None:
        raise ValueError("The algorithms must be a list.")

    if times_to_run <= 0:
        raise ValueError("The run time must be positive.")

    if frames <= 0:
        raise ValueError("The frames must be positive.")

    # make the a reference string for each time to run
    if locality:
        reference_strings = [makeReferenceStringWithLocality(
            reference_string_length) for i in range(times_to_run)]
    else:
        reference_strings = [makeReferenceStringWithoutLocality(
            reference_string_length) for i in range(times_to_run)]

    # Go through each algorithm and run it the set number of times to run
    sim_results = {}
    for algorithm in algorithms:

        algorithm = algorithm()

        sim_results[algorithm.name] = []

        for i in range(times_to_run):
            sim_results[algorithm.name].append(
                algorithm.run(reference_strings[i], frames))

    table_results = makeTables(sim_results)

    table_results = calcTablesStats(table_results)

    print("Done With Simulation")

    return table_results


def ComparePageReplacementAlgs(times_to_run: int = 5,
                          frames: int = 5,
                          reference_string_length: int = 100,
                          locality_test: bool = True,
                          plot_results: bool = True,
                          algorithms: list = None) -> None:
    '''
    This is a function to run the simulatePAgeReplacement Function
    and plot the results if set to true
    Args:
        times_to_run (int): The number of times to run the simulation for
        each algorithm.

        frames (int): The number of frames.

        reference_string_length (int): The length of the reference string.

        locality_test (bool): If True, replacement algs will be tested with and without locality.

        plot_results (bool): If True, the tables will be plotted.

        algorithms (list): The list of algorithms to run.
    '''

    if locality_test:
        # Run the simulation without locality
        table_results_no = runPageReplacementSim(
            times_to_run, frames, reference_string_length, False, algorithms)

        # Run the simulation with locality
        table_results_local = runPageReplacementSim(times_to_run,
                                                      frames,
                                                      reference_string_length,
                                                      True,
                                                      algorithms)

        if plot_results:

            results_matrix = []
            # loop through the keys in the table results
            for key in table_results_no.keys():

                # loop through the results for each algorithm
                # and add the stats the the matrix (Making it long form)
                for no_locality, locality in zip(
                        table_results_no[key], table_results_local[key]):

                    # adding no locality stats
                    stat = no_locality["stats"]
                    results_matrix_line = [f"{key}", False,
                                           stat["hit_rate"],
                                           stat["fault_rate"],
                                           stat["num_faults"],
                                           stat["num_hits"],
                                           stat["num_references"],
                                           stat["num_unique_references"]]

                    results_matrix.append(results_matrix_line)

                    # adding locality stats
                    stat = locality["stats"]
                    results_matrix_line = [f"{key}", True,
                                           stat["hit_rate"],
                                           stat["fault_rate"],
                                           stat["num_faults"],
                                           stat["num_hits"],
                                           stat["num_references"],
                                           stat["num_unique_references"]]

                    results_matrix.append(results_matrix_line)

            results_df = pd.DataFrame(
                results_matrix,
                columns=[
                    "Algorithm",
                    "locality",
                    "hit_rate",
                    "fault_rate",
                    "num_faults",
                    "num_hits",
                    "num_references",
                    "num_unique_references"])

            fig = px.box(
                results_df,
                x="Algorithm",
                y="hit_rate",
                color="locality")

            # Update the layout
            fig.update_layout(
                title="Hit Rate Over Different Algorithmsv AND Locality",
                xaxis_title="Algorithm",
                yaxis_title="Hit Rate",
                plot_bgcolor="#fcfcd4",
                yaxis=dict(
                    zeroline=False,
                    gridcolor='grey'))

            fig.show()

            print("Plotting Results")

            pass

    # loop through each algorithm in the results dictionary


def main():
    runPageReplacementSim(times_to_run=50,
                          frames=5,
                          reference_string_length=100,
                          locality_test=True,
                          plot_results=True,
                          algorithms=[FCFS, LRU, OPTIMAL, LFU, MFU, LFUDA])

    # Run the simulation
    # sim_results = simulatePageReplacement(times_to_run = 5,
    #                                          frames = 5,
    #                                          reference_string_length = 100,
    #                                          locality = True,
    #                                          algorithms = [FCFS, LRU, OPTIMAL])
    #
    # first_fcfs = sim_results["FCFS"][1]
    #
    # first_lru = sim_results["LRU"][1]
    #
    # first_opt = sim_results["OPT"][1]
    #
    # plotlyTable(first_opt, "OPT")
    #
    # plotlyTable(first_fcfs,"FCFS")
    #
    # plotlyTable(first_lru,"LRU")


if __name__ == "__main__":
    main()
