
# Elden Ring AI
#### AI to farm the bird for runes

### Required

Yolov5 - the model used for object detection
````
$ git clone https://github.com/ultralytics/yolov5.git
$ cd yolov5
$ pip install -r requirements.txt  # install

````

[LabelIMG](https://github.com/tzutalin/labelImg) - the GUI for labeling the images


### Optional

A [roboflow](https://app.roboflow.com) account - a website used to hold labeled images 
and export them to different kinds of formats for multiple object 
recognition algorithms.


A [wandb](https://wandb.ai) account - a website used to monitor the 
progress of the yolov5 model.






## Overview:

In this project I will be using the yolov5 model ( you only look once) to 
detect objects in the elden ring images to use them to eventually make an AI 
to farm the bird for runes. Here I will show how mulitprocessing can be used 
to speed up the detection process.




## Setup:

To start I created a python file called `collectRawImgs` to capture the game 
images from elden 
ring and to save them into a folder to be labeled with `labelimg` package.


I would then use parsec to play the game on my PC at home and run the 
`collect_data()` function in the python file. to capture the game frames.


## Labeling:

I then label the data which was a very arduous process even using a GUI. 

Below is a video of the process.(click img to play)


[![IMAGE ALT TEXT](http://img.youtube.com/vi/c_QWo7zBOMY/0.jpg)](http://www.youtube.com/watch?v=c_QWo7zBOMY "Video Title")


## Training:

After labeling the data I uploaded the folder to roboflow and exported it 
for the yolov5 model (oytorch format). I then followed the instructions in 
the [yolov5 documentation](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data) to train the model.


Here is the code used to train the model:


```
cd yolov5
python train.py --data batch_1.yaml --project original_m_elden_ring --epochs 
30 --weights yolov5m.pt   
```

This trained a yolov5m model on the elden ring images.

Here are the results:

[charts](https://wandb.ai/mattjax16/1024_m_elden_ring/reports/Elden-Ring-M-model--VmlldzoyMDI2NzM0)





## Running the model (Serial)

Now I will run the object detection model using `runModel.py` which is a 
single threaded version of running the model.


Here is video of the model running (click img to play):


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/od48ZoMoK_M/0.jpg)](https://www.youtube.com/watch?v=od48ZoMoK_M)


## Multi-processing:

Clearly this is not the best way to run the model due to the low speed of it 
(can be seen by low fps).

To fix this I will split running the model into 4 separate processes which 
will be run in parallel in `runModelParallel.py` . This allows the model to 
still 
capture game 
frames 
while the yolov5 model detects the objects, and while the video is being 
shown. `multiprocessing.Queues` are used to transfer the data between the 
processes.

The overall structure of the code is as follows:

![code structure](/Users/matthewbass/Documents/School_Colby/Colby/spring22/CS337-Operating-Systems/Projects/Proj9/EldenRingAi/readmeimgs/multi_proc_des.png)


Here is video of the model running in parallel (click img to play):


[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/NfFF6vOgINQ/0.jpg)](https://www.youtube.com/watch?v=NfFF6vOgINQ)


Success! It is clear that multiprocessing can be used to speed up the object 
detection process. (a 4x speedup!!!)



