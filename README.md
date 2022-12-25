# CSHL Protocols Mosquito Egg Counting
 
This repository accompanies the CSH Protocols chapter Evaluating egg-laying preference of individual Aedes aegypti mosquitoes. It is divided into two sections: one for image acquisition via raspberry pi, and the other for automated egg counting using Python and OpenCV. Two egg-counting methods are presented, and the workflow for using these scripts will be described in this Wiki. 

## Equipment list:

### Image Acquisition: 
- Raspberry pi (model >= 2, or any version with a CSI port for a camera interface. Note: the raspberry pi 400 does not have a CSI camera port and will not work for this application)
- Raspberry pi camera (we recommend the Raspberry Pi HQ camera as it is compatible with interchangeable C/CS-mount lenses for easy focus adjustment)
- microSD card (> 8GB) for the raspberry pi OS
- memory stick or external hard drive for file storage/transfer
- USB keyboard
- USB mouse
- Monitor
- HDMI-HDMI or HDMI-micro HDMI (depending on raspberry pi model)
- CSI ribbon cable
- LED tracing panel (> 4x6 in, any size will work as long as it is larger than the egg papers being used in the experiment)

### Egg counting: 
- Computer with [Anaconda (version >= 3.0)](https://www.anaconda.com/) installed - this remote environment software will be used to set up a Python environment for easy installation of OpenCV
- Installation of OpenCV (verison >= 4.1) - this can be easily [installed within your Anaconda environment](https://anaconda.org/conda-forge/opencv)

## Image Acquisition

First, set up the raspberry pi with a camera fixed in a secure position. In brief, the imaging setup should be extremely consistent throughout each experiment, and we stress the importance of both consistent camera position and consistent lighting - best achieved by using a backlight. Ensure that the imaging setup is as described in the CSHP chapter, and then proceed to using the script in this repository for collecting images. If setting up the raspberry pi for the first time, follow [this guide](https://www.raspberrypi.com/documentation/computers/getting-started.html) to install the operating system and initialize the pi. Additionally, the [camera interface will need to be initialized](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera). Once the raspberry pi has been initialized, test the camera by opening the terminal and running the following line to display a live preview of the camera: `libcamera-hello -t 0`. After the camera is successfully showing an image in the preview, close the preview using the `ctrl + c` shortcut. Once the camera is working and the imaging setup is prepared, transfer the 'ovi_paper_imaging.py' python script from this repository and run them in the pi's terminal. 

The imaging script `ovi-paper-imaging.py` is a python script that can be directly run on a Raspberry Pi. Before running the script, edit the first portion of the script with the experiment's treatment names, number of replicates, and a name for a folder to write the images into. After the inputs have been provided, the experimenter will have a preview available to set up and place the egg paper in the region of interest. Once the experimenter is satisfied with the position of the egg paper, they can press the ENTER key to take that image. The script will prompt the experimenter through the rest of the treatments and replicates that they defined prior to running the script.

The initial portion of the code also has parameters for camera settings and for cropping a region of interest (ROI). Before capturing the first standardized images, we recommend finding a configuration that works well with your imaging setup and keeping these settings consistent while imaging all papers within the experiment. 

## Egg counting 

We have included two automated egg-counting methods in this repository: contour-based (more simple) and pixel-based (more complex). Prior to using either method, experimenters will need to select a suitable threshold for binarizing images to highlight eggs and only eggs. First, open the `set-threshold.py` script in your Anaconda environment containing the OpenCV installation. This file will read in a sample image and write out a binary image with the threshold in the file name so that experimenters can determine a threshold that discriminates eggs from the background without producing artifacts or fragmented eggs. The threshold should be adjusted until eggs are discretely shown as white contours with nothing in the background converted to white pixels. 

Once a suitable threshold has been determined, researchers will select one of two automated counting methods. Both methods can be tested and their performance can be evaluated against "control" counts, or the supposed 'best' method can be selected by the extent of clumping present in the raw images. 



