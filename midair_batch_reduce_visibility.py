#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Note: please run this code under your datset path


"""
@author: Cheng_Zhang

"""
# from asyncio.windows_events import NULL
import os
import sys
from pathlib import Path
import shutil
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import importlib
import cv2 
from PIL import Image

def main():
    # enter function to ask for specific trajectory to bagify and return selection
    [environment, condition, camera, trajectoryList] = userInput()      
    # print("trajectoryList=",trajectoryList)
    # use the selection to find the appropriate sensor records file
    # sensorRecordsPath = os.path.abspath(os.getcwd() + "/MidAir/" + environment + '/' + condition)
    sensorRecordsPath = os.path.abspath(os.getcwd() + "/" + environment + '/' + condition)
    print("###---->>sensorRecordsPath:",sensorRecordsPath)
    sensorRecordsFile = sensorRecordsPath + "/sensor_records.hdf5"
    print("###---->>sensorRecordsFile:",sensorRecordsFile)
    
    # if the sensor records file doesn't exist, or is not yet unzipped, exit
    if not os.path.exists(sensorRecordsFile):
        if os.path.exists(sensorRecordsPath + "/sensor_records.zip"):
            print("I did not find the file: " + sensorRecordsFile + "\n\n I did find the corresponding .zip file, however. Please uncompress this file and try again.")
        else:
            print("I did not find the file: " + sensorRecordsFile)
        sys.exit(0)
    
    print("\nPlease choose how to reduce the visibility:\n1. Add Noise\n2. Add Dirt")
    reduction = int(input(""))
    
    if reduction == 1:
        detriment = "noisy"
    elif reduction == 2:
        detriment = "dirty"
        # choose dirty level
        answer = int(input("""Please choose the dirty level:\n
        1. disspersed progressive(from 5% to 60% visibility reduced)
        2. center progressive(from 5% to 60% visibility reduced)  \n\n"""))

        if(answer==1):
            filterList = [os.path.abspath("dirt_filter_dispersed") + "/" + img for img in os.listdir(os.path.abspath("dirt_filter_dispersed"))]
        elif(answer==2):
            filterList = [os.path.abspath("dirt_filter_center") + "/" + img for img in os.listdir(os.path.abspath("dirt_filter_center"))]
        else:
            sys.exit("You entered an invalid value")
        filterList.sort()
    else:
        sys.exit(0)
        
    
    # create a new path name for the noisy data to be stored in
    worseCondition = os.path.dirname(sensorRecordsPath) + "/{}_{}".format(detriment, condition)
    # print("******worseCondition=",worseCondition)
    
    # create the path if it doesn't already exist
    if not os.path.isdir(worseCondition):
        os.mkdir(worseCondition)

    # copy the sensor data into the new file
    shutil.copyfile(sensorRecordsFile, worseCondition + "/sensor_records.hdf5")
    
    for trajectory in trajectoryList:
        # the folder in which the original images are stored
        images = sensorRecordsPath + "/" + camera + "/trajectory_{}".format(trajectory)

        # create a new path name for the noisy images to be stored in
        worseImageFolder = worseCondition + "/" + camera + "/trajectory_{}".format(trajectory)
        
        print("\nAdding {} images to {}".format(detriment, worseImageFolder))
        # copy the full image folder over to the new location
        if not os.path.isdir(worseImageFolder):
            shutil.copytree(images, worseImageFolder)

        imageList = [os.path.abspath(worseImageFolder) + "/" + img for img in os.listdir(os.path.abspath(worseImageFolder)) if "zip" not in img]

        # add a function to allow the code generate different dirty levels with filters in the dirt_filter_dispersed document
        # make sure filter names in the dirt_filter_dispersed document are well organised for sorting

        # lists need to be sorted, original lists are random
        imageList.sort()
        batch = round(len(imageList) / len(filterList))
        filterNumber = 0
        processedImage= 0
        dirt_over = Image.open(filterList[filterNumber])
        # print("imageList=",imageList)
        print("Processing image with filter:", filterList[filterNumber])
        for img in imageList:
            if processedImage > batch:
                processedImage = 0
                filterNumber += 1
                dirt_over = Image.open(filterList[filterNumber])
                print("Processing image with filter:", filterList[filterNumber])
            
            worseImg = dirty(img, dirt_over)
            cv2.imwrite(img, cv2.cvtColor(worseImg, cv2.COLOR_RGB2BGR))
            processedImage += 1
        
        print("Generating .bag file for new data")
        bagify = importlib.import_module("midair_generateBagFile_Stereo")     
        bagify.main(environment, "/{}_{}".format(detriment, condition), trajectory, camera)
        ## TODO: prompt to create bag file at the end    

# global flags for selection prompts
installFlag = ""
notInstallFlag = "(NOT INSTALLED)"

# prompt the user through the process of selecting the trajectory to bagify
def userInput():
    # get the path to the dataset folder
    # dataPath = os.getcwd() + "/MidAir"
    dataPath = os.getcwd()
    
    # the user will be told if particular options aren't available on their machine
    kiteTestFlag = installFlag if os.path.isdir(dataPath + "/Kite_test") else notInstallFlag
    kiteTrainFlag = installFlag if os.path.isdir(dataPath + "/Kite_training") else notInstallFlag
    pleTestFlag = installFlag if os.path.isdir(dataPath + "/PLE_test") else notInstallFlag
    pleTrainFlag = installFlag if os.path.isdir(dataPath + "/PLE_training") else notInstallFlag
    voTestFlag = installFlag if os.path.isdir(dataPath + "/VO_test") else notInstallFlag
    
    # ask for the environment to test in, noting which are not available
    answer = int(input("""Please enter the environment you are testing in:\n
    1. Kite_test {}
    2. Kite_training {}               
    3. PLE_test {}
    4. PLE_training {}
    5. VO_test {}\n\n""".format(kiteTestFlag, kiteTrainFlag,pleTestFlag,pleTrainFlag,voTestFlag)))
    
    # apply selection
    if (answer==1):
        if kiteTestFlag == notInstallFlag:
            print("Environment not installed")
            sys.exit(0)
        else:
            environment="Kite_test"
    elif(answer==2):
        if kiteTrainFlag == notInstallFlag:
            print("Environment not installed")
            sys.exit(0)
        else:
            environment="Kite_training"
    elif(answer==3):
        if pleTestFlag == notInstallFlag:
            print("Environment not installed")
            sys.exit(0)
        else:
            environment="PLE_test"
    elif(answer==4):
        if pleTrainFlag == notInstallFlag:
            print("Environment not installed")
            sys.exit(0)
        else:
            environment="PLE_training"
    elif(answer==5):
        if voTestFlag == notInstallFlag:
            print("Environment not installed")
            sys.exit(0)
        else:
            environment="VO_test"
    else:
        sys.exit("You entered an out-of-range value")
    
    # each environment is numbered and ordered slightly differently, so account for this
    if "Kite" in environment:
        # the test environment has less trajectories than the training one
        trajRange = 4 if("test" in environment) else 29
        
        # again, notify user if particular conditions aren't installed
        cloudyFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "cloudy") else notInstallFlag
        foggyFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "foggy") else notInstallFlag
        sunnyFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "sunny") else notInstallFlag
        sunsetFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "sunset") else notInstallFlag
        
        # ask the user which condition they'd like to test under
        answer = int(input("""Please enter the condition you are testing in:\n
    1. cloudy {}
    2. foggy {}           
    3. sunny {}
    4. sunset {}\n\n""".format(cloudyFlag,foggyFlag,sunnyFlag,sunsetFlag)))
        if (answer==1):
            if cloudyFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="cloudy"
        elif(answer==2):
            if foggyFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="foggy"
        elif(answer==3):
            if sunnyFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="sunny"
        elif(answer==4):
            if sunsetFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="sunset"
        else:
            sys.exit(0)
         
        # look for available trajectories at this path
        trajSearchPath = dataPath + "/" + environment + "/" + condition
        # get the camera and trajectory number from the user
        trajList, camera = trajPrinter(trajSearchPath, trajRange)
            
    elif "PLE" in environment:
        # number of trajectories for the test and train sets
        trajRange = 5 if("test" in environment) else 23
        
        # notify of unavailable conditions
        fallFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "fall") else notInstallFlag
        springFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "spring") else notInstallFlag
        winterFlag = installFlag if os.path.isdir(dataPath + "/" + environment + "/" + "winter") else notInstallFlag
        
        # ask for the condition to test under
        answer = int(input("""Please enter the condition you are testing in:\n
    1. fall {}
    2. spring {}              
    3. winter {}\n\n""".format(fallFlag,springFlag,winterFlag)))
        if (answer==1):
            if fallFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="fall"
        elif(answer==2):
            if springFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="spring"
        elif(answer==3):
            if winterFlag == notInstallFlag:
                print("Condition not installed")
                sys.exit(0)
            else:
                condition="winter"
        else:
            sys.exit(0)    
        
        # get the camera to use and the trajectory to test
        trajSearchPath = dataPath + "/" + environment + "/" + condition
        trajList, camera = trajPrinter(trajSearchPath, trajRange)
                
    elif(environment=="VO_test"):
        trajRange = 2
        
        answer = int(input("""Please enter the condition you are testing in:\n
    1. foggy               
    2. sunny
    3. sunset\n\n"""))
        if(answer==1):
            condition="foggy"
        elif(answer==2):
            condition="sunny"
        elif(answer==3):
            condition="sunset"
        else:
            sys.exit("You entered an invalid value")
            
        trajSearchPath = dataPath + "/" + environment + "/" + condition
        trajList, camera = trajPrinter(trajSearchPath, trajRange)
        
    return [environment, condition, camera, trajList]
    
# print trajectory numbers with notice of whether or not they are installed
def trajPrinter(trajSearchPath, trajRange):
    
    colorLeftFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_left") else notInstallFlag   
    colorRightFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_right") else notInstallFlag 
    colorDownFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_down") else notInstallFlag 
    
    answer = int(input("""Please enter the camera you are testing with:\n
    1. color_left {}
    2. color_right {}             
    3. color_down {} \n\n""".format(colorLeftFlag,colorRightFlag,colorDownFlag)))
    
    if (answer==1):
        if colorLeftFlag == notInstallFlag:
            print("Camera not installed")
            sys.exit(0)
        else:
            camera="color_left"
    elif(answer==2):
        if colorRightFlag == notInstallFlag:
            print("Camera not installed")
            sys.exit(0)
        else:
            camera="color_right"
    elif(answer==3):
        if colorDownFlag == notInstallFlag:
            print("Camera not installed")
            sys.exit(0)
        else:
            camera="color_down"
    else:
        sys.exit("You entered an invalid value") 
    
    trajSearchPath = trajSearchPath + "/" + camera
    
    trajFileList = list(Path(trajSearchPath).rglob("[trajectory]*"))
    trajFileList = [str(a) for a in trajFileList if ("trajectory" in str(a) and ".bag" not in str(a))]
    trajList = [str(a[-4:]) for a in trajFileList]
    
    return(trajList, camera)

#https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
def noisy(img):
    image = mpimg.imread(img)
    row,col,ch = image.shape
    s_vs_p = 0.5
    amount = 0.008
    out = np.copy(image)
    # Salt mode
    num_salt = np.ceil(amount * image.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt))
            for i in image.shape]
    out[tuple(coords)] = 1
    
    # Pepper mode
    num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper))
            for i in image.shape]
    out[tuple(coords)] = 0
    return out

def dirty(img, over):
    # Open input images, background and overlay
    back = Image.open(img)
    
    # Paste overlay onto background using overlay alpha as mask
    back.paste(over, mask=over)
    soiled_img = np.array(back.copy())
    
    return soiled_img

if __name__ == "__main__":
    main()