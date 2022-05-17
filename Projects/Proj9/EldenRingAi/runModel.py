import torch
from time import time
from PIL import ImageGrab
import numpy as np
import cv2
import multiprocessing



class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using Opencv2.
    """

    def __init__(self,
                 model_path,
                 screen_coordinates = np.array([(0, 150), (0, 1120), (1424, 150), (1424, 1120)]),
                 threshold = 0.2):
        """
        Initializes the class with input and model path.
        """

        self.corner_cords = screen_coordinates
        self.model_path = model_path
        self.threshold = threshold
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def auto_canny(self, frame, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(frame)

        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(frame, lower, upper)

        # return the edged image
        return edged

    def get_game_frame(self):
        '''
        Get the game frame from the screen

        Returns:
            numpy array of the game frame
        '''

        # make the screen region
        screen_region = tuple(self.make_region())

        # Get the game frame from the screen
        game_frame = ImageGrab.grab(bbox=screen_region)

        return np.array(game_frame)

    def make_region(self):
        '''
        Make a region from the corner coordinates

        Args:
            corner_cords: numpy of the corner coordinates

        Returns:
            numpy array of the region
        '''
        # Get the top left corner
        top_left = self.corner_cords[0]

        # Get the bottom right corner
        bottom_right = self.corner_cords[3]

        # Make the region
        region = np.array((top_left[0], top_left[1],
                           bottom_right[0] - top_left[0],
                           bottom_right[1] - top_left[1]))

        return region

    def process_frame(self, frame):
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

        frame = self.auto_canny(frame, sigma=0.33)

        return original_frame, frame

    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=self.model_path)

        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
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
                    x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), \
                                     int(row[2]*x_shape), int(row[3]*y_shape)
                    bgr = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                    cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def run(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """

        while True:

            start_time = time()

            frame = self.get_game_frame()


            results = self.score_frame(frame)
            frame = self.plot_boxes(results, frame)

            end_time = time()
            fps = 1 / np.round(end_time - start_time, 2)
            # print(f"Frames Per Second : {fps}")

            cv2.putText(frame,
                        f'FPS: {int(fps)}',
                        (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 255, 0),
                        2)

            cv2.imshow('YOLOv5 Detection', frame)

            if cv2.waitKey(1) == "q":
                cv2.destroyAllWindows()
                break


    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        self.run()


def main():
    # Create a new object and execute.
    detector = ObjectDetection(model_path="/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj9/EldenRingAi/yolov5/1024_m_elden_ring/exp/weights/best.pt")
    detector()
    return
        
if __name__ == "__main__":
    main()
