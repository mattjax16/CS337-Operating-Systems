'''
This is a file to run the ELden Ring Object Detection model

It used multiprocessing to split capturing, processing, and running the model into different
processes to speed things up.

'''

import torch
import time
from PIL import ImageGrab
import numpy as np
import cv2
import torch.multiprocessing as mp




class testDetector(mp.Process):

    def __init__(self, input_queue, output_queue):
        mp.Process.__init__(self, name="Test")
        self.input_queue = input_queue
        self.output_queue = output_queue


    def run(self):
        while True:
            # Get the next frame from the input queue
            frame = self.input_queue.get()

            # put the frame into the output queue
            self.output_queue.put(frame)



class ObjectDetector(mp.Process):
    """
    Class implements Yolo5 model to make inference on frames Opencv2.

    It is a multiprocess.Process to be used for multiprocessing code
    """

    def __init__(self, model_path, input_queue: mp.Queue,
                 output_queue: mp.Queue, threshold: float = 0.2):
        """
        Initializes the class with input and model path.
        """
        mp.Process.__init__(self, name="ObjectDetectorProcess")
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.threshold = threshold
        self.model_path = model_path
        self.detection_model = self.load_model()
        self.classes = self.detection_model.names
        self.is_running = True


    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        model = torch.hub.load('ultralytics/yolov5',
                               'custom',
                               path=self.model_path)
        return model



    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """


        results = self.detection_model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        added_labels = []
        for i in range(n):
            if labels[i] in added_labels:
                continue
            else:
                added_labels.append(labels[i])

                row = cord[i]
                if row[4] >= self.threshold:
                    x1, y1, x2, y2 = int(row[0] * x_shape), int(
                        row[1] * y_shape), int(row[2] * x_shape), int(
                        row[3] * y_shape)
                    bgr = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                    cv2.putText(frame,
                                self.class_to_label(labels[i]),
                                (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                bgr,
                                2)

        return frame

    def run(self):
        """
        This function is called when class (processes) is executed

        It take frames from the input_queue
        and detects the objects and buts the frames with
        the boxes in the output queue
        :return: void
        """

        while self.is_running:

            start_time =time.time()

            frame = self.input_queue.get()

            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)

            end_time = time.time()
            fps = 1 / np.round(end_time - start_time, 2)
            # print(f"Frames Per Second : {fps}")

            cv2.putText(frame,
                        f'FPS: {int(fps)}',
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 255, 0),
                        2)

            self.output_queue.put(frame)


class FrameGetter(mp.Process):
    """
    Class that is used to get continuous screen grabs from the
    screen_coordinates provided
    """

    def __init__(self, output_queue: mp.Queue,
                 screen_coordinates : np.array = np.array([(0, 150), (0, 1120), (1424, 150), (1424, 1120)]),):

        self.screen_coordinates = screen_coordinates
        mp.Process.__init__(self, name="FrameGetterProcess")

        self.output_queue = output_queue
        self.is_running = True

    def make_region(self, screen_coordinates):
        '''
        Make a region from the corner coordinates

        Args:
            screen_coordinates: numpy of the corner coordinates

        Returns:
            numpy array of the region
        '''
        # Get the top left corner
        top_left = screen_coordinates[0]

        # Get the bottom right corner
        bottom_right = screen_coordinates[3]

        # Make the region
        region = (top_left[0], top_left[1],
                           bottom_right[0] - top_left[0],
                           bottom_right[1] - top_left[1])

        return region

    
    def get_frame(self, region):
        '''
        Get the  frame from the screen

        Returns:
            numpy array of the game frame
        '''


        # Get the game frame from the screen
        game_frame = ImageGrab.grab(bbox=region)

        # Return numpy array of it
        return np.array(game_frame)


    def run(self):
        """
        This function is called when class (processes) is executed

        It take frames from the input_queue
        and detects the objects and buts the frames with
        the boxes in the output queue
        :return: void
        """

        screen_region = self.make_region(self.screen_coordinates)

        while self.is_running:

            frame = self.get_frame(screen_region)

            self.output_queue.put(frame)


class FrameViewer(mp.Process):
    """
    Class that is used to display frames from the input queue in open cv
    """

    def __init__(self,
                 input_queue: mp.Queue ):
        """
        Initializes the class with input and model path.
        """
        mp.Process.__init__(self, name="FrameViewerProcess")
        self.is_running = True
        self.input_queue = input_queue



    def run(self):
        """
        This function is called when class (processes) is executed

        It take frames from the input_queue
        and detects the objects and buts the frames with
        the boxes in the output queue
        :return: void
        """



        while self.is_running:

            if len(self.input_queue.get()) > 0:

                frame = self.input_queue.get()

                cv2.imshow('YOLOv5 Detection', frame)

                if cv2.waitKey(1) == "q":
                    cv2.destroyAllWindows()
                    break






def runDetectionModel(model_path: str = "/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj9/EldenRingAi/yolov5/1024_m_elden_ring/exp/weights/best.pt",
                      threshold : float = 0.2,
                      screen_coordinates : np.array = np.array([(0, 150), (0, 1120), (1424, 150), (1424, 1120)]),
                      time_to_run : float = 100) -> None:
    '''
    This is a function to run the object detection model

    Args:
        model_path (str): path to the model
        threshold (float): threshold for the detection
        screen_coordinates (np.array): numpy array of the screen coordinates

    Returns:

    '''




    # Initialize the queues to connect the processes
    frame_to_detect_queue = mp.Queue()
    detect_to_view_queue = mp.Queue()

    # Initialize the processes
    object_detector = ObjectDetector(input_queue=frame_to_detect_queue,
                                   output_queue=detect_to_view_queue,
                                   model_path = model_path,
                                   threshold=threshold)

    # test_detector = testDetector(input_queue=frame_to_detect_queue,
    #                                output_queue=detect_to_view_queue)

    frame_getter = FrameGetter(output_queue = frame_to_detect_queue,
                               screen_coordinates=screen_coordinates)
    frame_viewer = FrameViewer(input_queue=detect_to_view_queue)

    procs = [frame_getter, object_detector,frame_viewer]

    # Start the processes
    print("Starting FrameGetter")
    frame_getter.start()


    print("Starting detector")

    object_detector.start()


    print("Starting viewer")
    frame_viewer.start()

    time.sleep(time_to_run)





    # Sleep for the time to run
    time.sleep(time_to_run)

    # Stop the processes
    for proc in procs:
        proc.is_running = False
        proc.join()




    print("Model finished")

    return



def main():
    runDetectionModel()
    return


if __name__ == "__main__":
    main()


