# CSHL Protocols Mosquito Egg Counting
 
Outline for imaging section

- Start up the raspberry pi. And turn on the LED tracing panel.
- If not already done, initialize the raspberry pi’s camera interface, and ensure that the camera is connected (https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
- Open the ‘2-choice-imaging.txt’ file, which contains bash scripts for taking and automatically labeling images of 2-choice oviposition assays. This script can be edited for various experimental setups by changing parameters for the number of choices and replicates. At its simplest, this script can be used to quickly label each pair of papers and to quickly take standardized images
- Set your working directory, then define experimental settings (experiment name, conditions, experimenter etc.)
- Copy and paste the remaining lines of code into the shell console. A camera preview will appear and remain until the ‘enter’ key is pressed. 
- Use the preview to line up the egg paper until the preview is satisfactory
- Press the ‘enter’ key to take the image. The file will be saved in your chosen directory with the information on experimental conditions (concentration, salt type, etc.) and a replicate number. 
- Repeat steps 4 and 5 for other choices tested in your experiment
- Repeat steps 2-6 as-needed for any other salts or concentrations
