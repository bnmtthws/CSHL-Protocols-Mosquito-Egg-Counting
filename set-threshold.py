# -*- coding: utf-8 -*-
"""
Setting a threshold for binarizing images of moquito eggs for automated counting

Created on Sat Dec 17 10:56:02 2022

@author: Nick Tochor
"""

#This script will be used to determine an optimal threshold for binarizing 
#images of eggs in order to prepare them for automated counting. This script
#creates a new folder 'threshold_testing' in your working directory where 
#binarized test images will be written

#Use this script to determine a suitable threshold for binarizing images 
#captured from your standardized setup. Change the 'threshold' value and check
#the binarized outputs until satisfactory binary images are produced

## Directory Structure
# This code uses relative paths, with a home directory containing three folders: 'rawdata', 'outdata', and 'scripts'
# Create a 'threshold-test' folder containing a representative image for determining a suitable threshold using this script

# This code was written in Python 3.9.12 using OpenCV version 4.6.0

#read in packages
import os # directories; path management
import cv2 #image analysis

###############################################################################
########### Change global variables that are project/user-dependent ###########
###############################################################################
imgFolder = r"../rawdata/threshold-test/" #folder with images for egg counting
rawImage = "threshold-test-image"
rawImageFormat = ".png" #image file format, could be '.png', '.jpeg', '.jpg', '.tif', '.tiff'

#the threshold is a value above which pixels will be turned white and below, black
#since the images are inverted first, 'eggs' will be aboce this value and the background will be below
#it ranges from 0-255, so start with an intermediate value (e.g. 128 and check the output) and adjust accordingly
threshold = 45 #threshold for binarizing black and white images - this will be changed until a suitable value is found

outFolder = "../outdata/threshold-test/" #folder to write test binarized images into
thresholdOutputFileName = "threshold-test" #file name for tested images
outputFileType = ".png" #file type for test images
experimentName = "camera-setup" #file name for .csv of count data - best to use project/experiment name

#Everything below this line is generalized to run without any customization required
###############################################################################

#create strings for reading raw image and writing thresholded image based on user inputs
rawImage = f'{imgFolder}{rawImage}{rawImageFormat}'
thresholdImage = str(f'{outFolder}{experimentName}{"_"}{thresholdOutputFileName}{"_"}{threshold}{outputFileType}')

#read in image using openCV's 'imread' function
image = cv2.imread(rawImage, cv2.IMREAD_GRAYSCALE) #the image is converted to black and white

#binarize the image using the previously defined threshold
ret,imageBinary=cv2.threshold(image,threshold, 255, cv2.THRESH_BINARY_INV) #inverts the image and binarizes it based on user-defined threshold

#write binarized image for manual reviewing binarization quality
cv2.imwrite(thresholdImage, imageBinary)
