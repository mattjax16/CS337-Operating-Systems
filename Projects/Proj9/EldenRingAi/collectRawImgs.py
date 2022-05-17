'''Main testing file for elden ring AI'''

# Imports
import PIL

from matplotlib import pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors
from tkinter import *
from PIL import Image
from PIL import ImageGrab
import numpy as np
import cv2
import pyautogui
import os




# master = Tk()
# canny_thresh_1 = Scale(master, from_=0, to=255, tickinterval=1, orient=HORIZONTAL)
# canny_thresh_1.set(60)
# canny_thresh_1.pack()
# canny_thresh_2 = Scale(master, from_=0, to=255, tickinterval=1, orient=HORIZONTAL)
# canny_thresh_2.set(70)
# canny_thresh_2.pack()





# Global variables
# The screen corner coordinates
screen_corner_cords = np.array([(0, 150), (0, 1120), (1424, 150), (1424, 1120)])


labels = [{'name':'player', 'id':1}, {'name':'bow', 'id':2},
          {'name':'bird', 'id':3}, {'name':'grace', 'id':4},
          {'name':'rest', 'id':5}, {'name':'atRest', 'id':6}]

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

def get_mouse_pos():
    # Get the postion of the mouse and display it
    while True:
        mouse_pos = pyautogui.position()
        print(mouse_pos)



def get_game_frame():
    '''
    Get the game frame from the screen

    Returns:
        numpy array of the game frame
    '''

    # make the screen region
    screen_region = tuple(make_region(screen_corner_cords))

    # Get the game frame from the screen
    game_frame = ImageGrab.grab(bbox=screen_region)

    return np.array(game_frame)


def make_region(corner_cords):
    '''
    Make a region from the corner coordinates

    Args:
        corner_cords: numpy of the corner coordinates

    Returns:
        numpy array of the region
    '''
    # Get the top left corner
    top_left = corner_cords[0]

    # Get the bottom right corner
    bottom_right = corner_cords[3]

    # Make the region
    region = np.array((top_left[0], top_left[1], bottom_right[0] - top_left[0],
                       bottom_right[1] - top_left[1]))

    return region


def process_frame(frame):
    '''
    Process the frame to make it easier to work with

    Args:
        frame: numpy array of the frame

    Returns:
        numpy array of the processed frame
    '''



    original_frame = frame.copy()

    # Convert the frame to grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)
    # Blur the frame
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    frame = auto_canny(frame,
                       sigma=0.33)

    return original_frame, frame



def decode_labeled_frames(labeled_frames_path,
                          debug=True):
    '''
    Decode the labeled frames

    Args:
        labeled_frames_path: path to the labeled frames
        debug: if true, show how long it takes to run the function
    '''


    if debug:
        start_time = time.time()



    files_in_dir = os.listdir(labeled_frames_path)

    # Separate the file paths into their base names
    frame_names = set()
    for file in files_in_dir:

        # get the base name of the file
        file = file.split('.')[:2]
        file = str.join('.', file)

        if file not in frame_names:
            frame_names.add(file)




    if debug:
        print(f"Time to run decode_labeled_frames: {time.time() - start_time}")




def click_to_yolo(num_times=20):
    '''
    A function to click yolo then save then previous for the number of times given
    :return:
    :rtype:
    '''
    type_pos = (48,442)
    save_pos = (48,385)
    prev_pos = (48,323)


    # Loop through the number of times
    for i in range(num_times):

        # Click the type button
        pyautogui.click(type_pos)

        # Click the save button
        pyautogui.click(save_pos)

        # Click the previous button
        pyautogui.click(prev_pos)

    return

def run():
    while True:
        # Set a timer
        start_time = time.time()

        # Get the game frame
        frame = get_game_frame()

        # Process the frame
        frame = process_frame(frame)

        #End timer
        end_time = time.time()
        print(f"Time to get and frame {end_time - start_time} seconds")

        # Show the frame
        cv2.imshow('frame', frame)
        cv2.waitKey(0)





    return

def plt_split_frame(frame):
    '''
    Plot the frame by rgb vals in 3d

    Args:
        frame: numpy array of the frame
    '''
    frame = np.array(frame)

    #Make frame rgb from rgba
    frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

    r,g,b = cv2.split(frame)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')

    # Flaten the frame
    frame_colors = frame.reshape(frame.shape[0] * frame.shape[1], 3)

    # Normalize the frame
    norm = colors.Normalize(vmin=-1.,vmax=1.)
    norm.autoscale(frame_colors)
    frame_colors = norm(frame_colors).tolist()

    #Setting up plot
    ax.scatter(r.flatten(), g.flatten(), b.flatten(), facecolors=frame_colors, marker=".")
    ax.set_xlabel("Red")
    ax.set_ylabel("Green")
    ax.set_zlabel("Blue")


    # Show the plot
    plt.show()


def collect_data(time_to_run = 60):
    '''
    Collect data for a certain amount of time

    Args:
        time_to_run: amount of time to collect data
    '''

    # Set a timer
    start_time = time.time()

    while time.time() - start_time  < time_to_run:

        # Get the game frame
        frame = get_game_frame()

        # Process the frame
        frame, processed_frame = process_frame(frame)

        # Make the image names
        original_frame_name = f"original_frame_{time.time()}.png"
        processed_frame_name = f"processed_frame_{time.time()}.png"

        # Make the directory paths
        dir_data_path = os.path.dirname("Data/")

        dir_original_frame_path = os.path.join(dir_data_path, "Original")
        dir_processed_frame_path = os.path.join(dir_data_path, "Processed")

        #Make the final paths
        original_frame_path = os.path.join(dir_original_frame_path, original_frame_name)
        processed_frame_path = os.path.join(dir_processed_frame_path, processed_frame_name)

        # Save the frames
        cv2.imwrite(original_frame_path, frame)
        cv2.imwrite(processed_frame_path, processed_frame)

        print(f"Saved frame")



def capture_live_game_no_save():
    '''
    Capture a live game without saving the frames
    '''

    # Set a timer
    start_time = time.time()

    while(True):

        # Get the game frame
        frame = get_game_frame()



        # Show the frame
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()
            break

    return




def main():
    # collect_data(time_to_run = 60)
    capture_live_game_no_save()


    return


if __name__ == '__main__':
    main()