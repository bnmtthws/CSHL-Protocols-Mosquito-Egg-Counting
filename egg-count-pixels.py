# -*- coding: utf-8 -*-
"""
Mosquito egg counting code using OpenCV pixel-based counts

Updated on Mon Sep 12 13:48:44 2022

@author: Nick Tochor
"""

# This script will use basic contour detection to automatically count eggs within photos of egg papers
# Binary thresholds were set based on a particular imaging setup and may need to be adjusted for different imaging setups
# It is slightly more complex than counting contours, and should adjust for more variation in clumping extent 
# This simple method of counting eggs is fairly robust to variation in imaging setups, but currently has issues with regions of highly clumped (e.g. overlapping) eggs
# More complex methods using locally trained pixel-based egg counting, trained on each image in the dataset will be written and updated

## Directory Structure
# This code uses relative paths, with a home directory containing three folders: 'rawdata', 'outdata', and 'scripts'

# This code was written in Python 3.9.12 using OpenCV version 4.6.0

#read in packages
import os # directories; path management
import glob2 as glob # batch reading images
import pandas as pd # working with matrices and writing to .csv
import cv2 # image analysis

###############################################################################
########### Change global variables that are project/user-dependent ###########
###############################################################################
trainingFolder = r"../rawdata/training-data/" #folder of images with manual counts to be used for training the pixels/egg value
imgFolder = r"../rawdata/test-batch-1/" #folder with images for egg counting
imgFormat = ".png" #image file format, could be '.png', '.jpeg', '.jpg', '.tif', '.tiff'

threshold = 50 #threshold for binarizing black and white images (see 'readme.txt for more information)

outFolder = "../outdata/" #folder to write output .csv to
trainingOutputFileName = "training-data-raw" #file name for training data egg counts
outputFileType = ".csv" #file type for output data
outputFile = "test-batch-1" #file name for .csv of count data - best to use project/experiment name
#Everything below this line is generalized to run without any customization required
###############################################################################
#use 'glob()' to extract the file names
#the leading '*" is a string wildcard; it must be present before the file format
trainingImageList = glob.glob(trainingFolder + "*" + imgFormat)
numberTrainingImages = len(trainingImageList)

#make new dictionaries for variables of interest for the trained dataset
trainingFileNames = {}
trainingNumberContours = {}
trainingTotalEggPixels = {}
trainingPixelsPerEgg = {}

#run the analysis for all images in 'imgFolder'
for i in range(numberTrainingImages):
    #read in image using openCV's 'imread' function
    file = trainingImageList[i]
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    #cv2.imwrite("../outdata/test-batch-1/readtest.png", img) #uncomment if troubleshooting image reading
    
    #create binarized image using threshold
    #we used a threshold of 50 (0-255) - see 'thresh-set.py' script for determining thresholds
    ret,imageBinary=cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV) #threshold set manually based on test images
    #cv2.imwrite("../outdata/test-batch-1/binarytest.png", imgBinary) #uncomment if troubleshooting thresholding
    
    #define contours for distinct shapes present in the binarized image
    contours, hier=cv2.findContours(imageBinary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    #summarize count and other info to be written to .csv
    trainingFileNames[i] = os.path.basename(file)[:-4]
    trainingNumberContours[i] = len(contours)
    #determine total pixels for all eggs in image
    trainingTotalEggPixels[i] = cv2.countNonZero(imageBinary)
    if trainingNumberContours[i] == 0:
        trainingPixelsPerEgg[i] = 0
    else:
        trainingPixelsPerEgg[i] = trainingTotalEggPixels[i] / trainingNumberContours[i]
    
#append lists of data to 'eggCountMatrix' dataframe
trainingCountMatrix = pd.DataFrame({'image_name': trainingFileNames, 'num_contours': trainingNumberContours, 'total_egg_pixels': trainingTotalEggPixels, 'pixels_per_egg': trainingPixelsPerEgg})
    
#write training matrix out as .csv for reference
#this output can be used to check the accuracy of the counts relative to manual counts
trainingCountMatrix.to_csv(outFolder + trainingOutputFileName + outputFileType, index = False)

#now we'll select only the images that had mean pixels/egg values +/- 2 standard deviations from the median to eliminate significant outliers

#remove zero-egg (blank) egg papers
trainingMatrix = trainingCountMatrix.loc[~(trainingCountMatrix['num_contours'] == 0)]

#calculate median eggs per pixel for entire training dataset
medianPixelsPerEgg = trainingMatrix['pixels_per_egg'].median()

#calculate standard deviation of eggs per pixel for the entire training dataset
standardDeviationPixelsPerEgg = trainingMatrix['pixels_per_egg'].std()

#determine upper and lower bounds for inclusion in the training data mean pixel/egg calculation
pixelsPerEggUpperLimit = medianPixelsPerEgg + (2 * standardDeviationPixelsPerEgg) 
pixelsPerEggLowerLimit = medianPixelsPerEgg - (2 * standardDeviationPixelsPerEgg) 

#select images with mean egg/pixel values within +/- two standard deviations of the median
trainingMatrixOutliersRemoved = trainingMatrix.loc[(trainingCountMatrix['pixels_per_egg'] >= pixelsPerEggLowerLimit) & (trainingMatrix['pixels_per_egg'] <= pixelsPerEggUpperLimit)]

#determine mean pixels/egg for our training dataset with the outliers removed
pixelsPerEgg = trainingMatrix['pixels_per_egg'].mean()

###############################################################################

#now we can read in new images to count with our trained pixels per egg value

#use 'glob()' to extract the file names
#the leading '*" is a string wildcard; it must be present before the file format
imagesList = glob.glob(imgFolder + "*" + imgFormat)
numberImages = len(imagesList)

#make new dictionaries for variables of interest - we'll include an optional third column for pixel counts so that the extent of clumping can be approximated
#e.g. if one paper has a much higher pixels/egg ratio, it may be highly clumped, and another method might be better
fileNames = {}
numberEggs = {}

#run the analysis for all images in 'imgFolder'
for i in range(numberImages):
    #read in image using openCV's 'imread' function
    file = imagesList[i]
    image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    
    #create binarized image using threshold
    #we used a threshold of 50 (0-255) - see 'thresh-set.py' script for determining thresholds
    ret,imageBinary=cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV) #threshold set manually based on test images
    
    #define contours for distinct shapes present in the binarized image
    contours, hier=cv2.findContours(imageBinary, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    #summarize count and other info to be written to .csv
    fileNames[i] = os.path.basename(file)[:-4]
    
    #calculate number of eggs using trained value for pixels/egg
    totalEggPixels = cv2.countNonZero(imageBinary)
    numberEggs[i] = round(totalEggPixels / pixelsPerEgg)
    
#append lists of data to 'eggCountMatrix' dataframe
eggCountMatrix = pd.DataFrame({'image_name': fileNames, 'num_eggs': numberEggs})

#define count method for output file name
countMethod = "pixel-based-counts"

#write out egg count matrix as .csv
eggCountMatrix.to_csv(outFolder + outputFile + "-" + countMethod + outputFileType, index = False)
