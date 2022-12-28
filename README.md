# CSHL Protocols Mosquito Egg Counting
 
This repository accompanies the CSH Protocols chapter Evaluating egg-laying preference of individual Aedes aegypti mosquitoes. It is divided into two sections: one for image acquisition via Raspberry Pi, and the other for automated egg counting using Python and OpenCV. Two egg-counting methods are presented and the workflow for using these scripts will be described in this Wiki. 

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

### Setting a threshold

It is critical to select a threshold that appropriately binarizes egg paper images into binary matrices clearly defined eggs with no artifacts. Unsuitable thresholds can severely impact counting accuracy, so we've created a separate script for this part of the workflow. The `set-threshold.py` script is used for trying a range of thresholds until a suitable one is found for a given imaging setup. To find a threshold:
- download the `set-threshold.py` script from this repository and open it in a Python environment with OpenCV installed
- read in a test image from your imaging setup
- set a threshold in the middle of the pixel range (0-255, 128 is a good starting point)
- run the script to produce a binarized image in your working directory
- check the image for any artifacts (e.g. background or egg papers converted to white pixels, fragmented egg geometries)

Once a threshold is found that clearly defines eggs as single polygons, make note of that threshold and use it for the following automated counting methods. 

### Countour-based automated egg counting 

The simplest automated counting method uses the threshold from the above section to binarize a raw image and then simply counts the numbers of distinct polygons (eggs). While very simple, it works very effectively for images of egg papers from single animal oviposition experiments. Follow the steps below to count eggs using this method, and evaluate the performance of the automated egg counts before moving on to data analysis. 

- download the `egg-count-polygon.py` script from this repository and open it in a Python environment with OpenCV installed
- set the directory to the folder containing your experiments' raw egg paper images
- define the directory for writing the .csv of summarized egg counts for each egg paper image
- change the `threshold` to the threshold deterimined using the `set-threshold.py` script from this repository
- run the script to automatically count eggs

### Evaluating the performance of automated egg counts 

When initially using an automated egg count method, it is highly important that researchers validate its accuracy before moving on to data analysis. Both of the egg counting methods we use are very simple, and will produce "counts" from images of any objects as long as the threshold is set in a way that creates clusters of white pixels. With this in mind, it is important to ensure that your imaging setup, camera settings, and threshold selection are all working well and producing reasonable data before any of these models are trusted. 

We recommend manually counting eggs using a software such as FIJI in order to build a reference dataset to check automated counts against. If you plan to do this, count the eggs for a reasonably large number of egg papers (at least 25, but more is better) and record these count data along with the file names for each image. With this dataset made, you can quickly compare the counts produced by either counting method in this repository in order to compare the performance of the two methods. Since both methods output a .csv with image file names and the number of eggs counted for each image, it is easiest to merge these to the dataset of manual counts and quickly calculate the count error for each method. We recommend calculating the relative error between each method and the manual counts, and averaging the error over the number of images in the manual dataset. Some judgement is required for determining the acceptable margin of error, but we have found both counting methods to perform with relatively high degrees of accuracy for a variety of imaging setups. 

### Pixel-based automated egg counting 




