# CSHL Protocols Mosquito Egg Counting
 
This repository accompanies the CSH Protocols chapter Evaluating egg-laying preference of individual Aedes aegypti mosquitoes. It is divided into two sections: one for image acquisition via raspberry pi, and the other for automated egg counting using Python and OpenCV. Two egg-counting methods are presented, and the workflow for using these scripts will be described in this Wiki. 

##Equipment list:

Image Acquisition: 
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

Egg counting: 
- Computer with [Anaconda (version >= 3.0)](https://www.anaconda.com/) installed - this remote environment software will be used to set up a Python environment for easy installation of OpenCV
- Installation of OpenCV (verison >= 4.1) - this can be easily [installed within your Anaconda environment](https://anaconda.org/conda-forge/opencv)

##Image Acquisition

First, set up the raspberry pi with a camera fixed in a secure position. In brief, the imaging setup should be extremely consistent throughout each experiment, and we stress the importance of both consistent camera position and consistent lighting - best achieved by using a backlight. Ensure that the imaging setup is as described in the CSHP chapter, and then proceed to using the scripts in this repository for collecting images. If setting up the raspberry pi for the first time, follow [this guide](https://www.raspberrypi.com/documentation/computers/getting-started.html) to install the operating system and initialize the pi. Additionally, the [camera interface will need to be initialized](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera). Once the raspberry pi has been initialized, test the camera by opening the terminal and running the following line to display a live preview of the camera: 'raspistill -t 0'. After the camera is successfully showing an image in the preview, close the preview using the 'ctrl + c' shortcut. Once the camera is working and the imaging setup is prepared, transfer the bash scripts from this repository and run them in the pi's terminal. 

The imaging script is a bash script that can be directly run on a Raspberry Pi. When running the script, it will prompt for several user inputs, including treatment names, number of replicates per treatment, and a name for a folder to write the images into. After the inputs have been provided, the experimenter will have a preview available to set up and place the egg paper in the region of interest, and the images will be taken by pressing the ENTER key. 

Note on python version? 

##Egg counting 



- Start up the raspberry pi. And turn on the LED tracing panel.
- If not already done, initialize the raspberry pi’s camera interface, and ensure that the camera is connected (https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
- Open the ‘2-choice-imaging.txt’ file, which contains bash scripts for taking and automatically labeling images of 2-choice oviposition assays. This script can be edited for various experimental setups by changing parameters for the number of choices and replicates. At its simplest, this script can be used to quickly label each pair of papers and to quickly take standardized images
- Set your working directory, then define experimental settings (experiment name, conditions, experimenter etc.)
- Copy and paste the remaining lines of code into the shell console. A camera preview will appear and remain until the ‘enter’ key is pressed. 
- Use the preview to line up the egg paper until the preview is satisfactory
- Press the ‘enter’ key to take the image. The file will be saved in your chosen directory with the information on experimental conditions (concentration, salt type, etc.) and a replicate number. 
- Repeat steps 4 and 5 for other choices tested in your experiment
- Repeat steps 2-6 as-needed for any other salts or concentrations
