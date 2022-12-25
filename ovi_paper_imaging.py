#this script will be used to capture images using the raspberry pi's picamera modules
#by default the location of this script will be the working directory
#and output folders will be placed in the home folder for the storage location of this script

#######################################################
#read in required packages
import os #directory management and folder creation
from picamera import PiCamera #using the raspberry pi's camera

#edit the following variables according to each experiment
#define image collection session name (must be unique to prevent overwriting data)
sessionID = "test_session5" 
fileFormat = ".png" #.png, .jpg, etc.

#fill this list with the treatments in the order they will be imaged 
treatmentList = ["control", "0.1_NaCl", "0.1_KCl", "0.1_Na2SO4"]
numberReplicates = 2 #number of replicates per treatment

###
#camera settings - edit as needed but keep consistent once optimized
#crop settings
roiX = 0.0 #coordinate for center of ROI (x value)
roiY = 0.0 #coordinate for center of ROI (y value)
roiWidth = 0.68 #roi width (0-1.0, as proportion of the sensor)
roiHeight = 0.77 #roi height (0-1.0, as proportion of the sensor)

previewTransparency = 205 #transparency from 0(completely transparent) to 255 (completely opaque)
resolutionX = 1750 #image width, pixels
resolutionY = 1500 #image height, pixels
shutterSpeed = 2500 #shutter speed, in us (200-6000000)
iso = 200 #range: 100,200,400,800
whiteBalance = 'fluorescent'

####################################################
#Everything below this line will run automatically without additional user input
####################################################
#print user-inputted settings
print("treatments: ")
for treatment in treatmentList:
	print(treatment)

numberTreatments = len(treatmentList)
print("number of treatments: ", numberTreatments)

camera = PiCamera()
#make new folder for captured images 
os.mkdir(sessionID)
print(f'{"output folder"}{sessionID}{"successfully created"}')

input("camera initialized; press enter to start preview")

for replicate in range(1, (numberReplicates + 1)):
	print(f'{"imaging replicate "}{replicate}{" of "}{numberReplicates}')
	replicateID = str(f'{"r"}{replicate}')
	for treatment in treatmentList:
		print(f'{"capturing image for treatment: "}{treatment}')
		camera.resolution = (resolutionX, resolutionY)
		camera.exposure_mode = "auto"
		camera.shutter_speed = shutterSpeed
		camera.awb_mode = whiteBalance
		camera.color_effects = (128,128) #captures grayscale image, comment out if color is desired
		camera.zoom = (roiX, roiY, roiWidth, roiHeight)
		camera.start_preview(alpha = previewTransparency)
		fileName = f'{os.getcwd()}{"/"}{sessionID}{"/"}{sessionID}{"_"}{"eggpaper_"}{treatment}{"_"}{replicateID}{fileFormat}'
		print(fileName)
		input("Preview - press enter key to capture image")
		camera.capture(fileName)
		input("imaged captured, press enter to continue to next image")

print("imaging session complete!")

