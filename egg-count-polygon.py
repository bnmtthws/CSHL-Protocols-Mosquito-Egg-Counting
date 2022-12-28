# -*- coding: utf-8 -*-
"""
Mosquito egg counting code using OpenCV polygon counts

Updated on Mon Sep 12 13:48:44 2022

@author: Nick Tochor
"""

# This script will use basic contour detection to automatically count eggs within photos of egg papers
# Binary thresholds were set based on a particular imaging setup and may need to be adjusted for different imaging setups
# This simple method of counting eggs is fairly robust to variation in imaging setups, but currently has issues with regions of highly clumped (e.g. overlapping) eggs
# If egg papers have a high degree of clumping and this method works poorly, try using the `egg-count-pixel.py' script, which is more robust for counting clustered eggs

## Directory Structure
# This code uses relative paths, with a home directory containing three folders: 'rawdata', 'outdata', and 'scripts'

# This code was written in Python 3.9.12 using OpenCV version 4.6.0

#read in packages
import os #directories; path management
import glob2 as glob #batch reading images
import pandas as pd #workikng with matrices and writing to .csv
import cv2 #image analysis

###############################################################################
#change global variables that are project/user-dependent
imgFolder = r"../rawdata/test-batch-1/" #set folder with images for egg counting

threshold = 50 #threshold for binarizing black and white images (see readme.md and `set-threshold.py` for more information)

outFolder = "../outdata/" #folder to write output .csv to
outputFile = "test-batch-1" #file name for .csv of count data - best to use project/experiment name
###############################################################################
#Everything below this line is generalized to run without any customization required 

#use 'glob()' to extract the file names
#the leading '*" is a string wildcard; it must be present before the file format
#other formats could be '*.jpeg', '*.jpg', '*.tif', '*.tiff', etc. 
imagesList = glob.glob(imgFolder+'*.png')
numberImages = len(imagesList)

#make new dictionaries for variables of interest - we'll include an optional third column for pixel counts so that the extent of clumping can be approximated
#e.g. if one paper has a much higher pixels/egg ratio, it may be highly clumped, and another method might be better
fileNames = {}
numberEggs = {}
pixelsPerEgg = {}

#run the analysis for all images in 'imgFolder'
for i in range(numberImages):
    #read in image using openCV's 'imread' function
    file = imagesList[i]
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    #cv2.imwrite("../outdata/test-batch-1/readtest.png", img) #uncomment if troubleshooting image reading
    
    #create binarized image using threshold
    ret,imageBinary=cv2.threshold(image,threshold, 255, cv2.THRESH_BINARY_INV) #threshold set manually based on test images
    #cv2.imwrite("../outdata/test-batch-1/binarytest.png", imgBinary) #uncomment if troubleshooting thresholding
    
    #define contours for distinct shapes present in the binarized image
    contours, hier=cv2.findContours(imageBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    #summarize count and other info to be written to .csv
    fileNames[i] = os.path.basename(file)[:-4]
    numberEggs[i] = len(contours)
    
    #calculate mean pixels/egg
    if numberEggs[i] == 0:
        pixelsPerEgg[i] = 0
    else:
        pixelsPerEgg[i] = cv2.countNonZero(imageBinary) / numberEggs[i]
    
#append lists of data to 'eggCountMatrix' dataframe
eggCountMatrix = pd.DataFrame({'image_name': fileNames, 'num_eggs': numberEggs, 'pix_per_egg': pixelsPerEgg})
    
#define count method for file output name
countMethod = "contour-based-counts"
outputFileType = ".csv"

#write out count data as .csv
eggCountMatrix.to_csv(outFolder + outputFile + "-" + countMethod + outputFileType, index = False)
