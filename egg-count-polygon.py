# -*- coding: utf-8 -*-
"""
Mosquito egg counting code using OpenCV polygon counts

Updated on Mon Aug 29 13:48:44 2022

@author: Nick Tochor
"""

# This script will use basic contour detection to automatically count eggs within photos of egg papers
# Binary thresholds were set based on a particular imaging setup and may need to be adjusted for different imaging setups
# This simple method of counting eggs is fairly robust to variation in imaging setups, but currently has issues with regions of highly clumped (e.g. overlapping) eggs
# More complex methods using pixel-based egg counting, trained on each image in the dataset will be written and updated

## Directory Structure
# This code uses relative paths, with a home directory containing three folders: 'rawdata', 'outdata', and 'scripts'

# This code was written in Python 3.9.12 using OpenCV version 4.6.0

#read in packages
import os # directories; path management
import glob2 as glob # batch reading images
import pandas as pd # workikng with matrices and writing to .csv
import cv2 # image analysis

#set working directory to 'scripts' folder
os.chdir("C:/Users/ubc/Desktop/Current-Lab-Members/NickTochor/eggcount/eggcount-methods/scripts")

#set folder with images for egg counting
imgFolder = r"../rawdata/test-batch-1/"

#the leading '*" is a string wildcard; it must be present before the file format
#other formats could be '*.jpeg', '*.jpg', '*.tif', '*.tiff', etc. 
imagesList = glob.glob(imgFolder+'*.png')
numImages = len(imagesList)

#make nk dictionaries for variables of interest - we'll include an optional third column for pixel counts so that the extent of clumping can be approximated
#e.g. if one paper has a much higher pixels/egg ratio, it may be highly clumped, and another method might be better
fileNames = {}
numEggs = {}
pixPerEgg = {}

#run the analysis for all images in 'imgFolder'
for i in range(numImages):
    #read in image using openCV's 'imread' function
    file = imagesList[i]
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    #cv2.imwrite("../outdata/test-batch-1/readtest.png", img)
    
    #create binarized image using threshold
    #we used a threshold of 50 (0-255) - see 'thresh-set.py' script for determining thresholds
    ret,imgBinary=cv2.threshold(img,50,255,cv2.THRESH_BINARY_INV) #threshold set manually based on test images
    #cv2.imwrite("../outdata/test-batch-1/binarytest.png", imgBinary)
    
    #define contours for distinct shapes present in the binarized image
    contours, hier=cv2.findContours(imgBinary, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    #summarize count and other info to be written to .csv
    fileNames[i] = os.path.basename(file)[:-4]
    numEggs[i] = len(contours)
    #calculate mean pixels/egg
    if numEggs[i] == 0:
        pixPerEgg[i] = 0
    else:
        pixPerEgg[i] = cv2.countNonZero(imgBinary) / numEggs[i]
    
#append lists of data to 'eggCountMatrix' dataframe
eggCountMatrix = pd.DataFrame({'image_name': fileNames, 'num_eggs': numEggs, 'pix_per_egg': pixPerEgg})
    
#write out .csv
eggCountMatrix.to_csv("../outdata/test-batch-1-counts.csv", index = False)
