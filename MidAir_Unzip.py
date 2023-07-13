#!/usr/bin/env python3

"""
    @author: Cheng Zhang
    
    BRIEF:  Run this script in the path of Mid-Air dataset to unzip the original zipped files
    
"""

# for file path interpretation and representation    
import os
# for exit control
import sys
# for some file representation stuff
from pathlib import Path

import zipfile


def main():
    userInput()


# global flags for selection prompts
installFlag = ""
notInstallFlag = "(NOT INSTALLED)"


# prompt the user through the process of selecting the trajectory to bagify
def userInput():
    # get the path to the dataset folder
    # dataPath = os.getcwd() + "/dataset/MidAir"
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
        trajectoryList = trajPrinter(trajSearchPath)
        for i in trajectoryList:
            unzip_file(i)
        print("Unzip finished successfully!")
        sys.exit(0)

            
    elif "PLE" in environment:

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
        trajectoryList = trajPrinter(trajSearchPath)
        for i in trajectoryList:
            unzip_file(i)
        print("Unzip finished successfully!")
        sys.exit(0)
                
    else:
        print("Fatal logic error! Check the code")
        sys.exit(0)
  

def trajPrinter(trajSearchPath):
    
    colorLeftFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_left") else notInstallFlag   
    colorRightFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_right") else notInstallFlag 
    colorDownFlag =  installFlag if os.path.isdir(trajSearchPath + "/color_down") else notInstallFlag
    colorBothFlag = installFlag if os.path.isdir(trajSearchPath + "/color_left") and os.path.isdir(trajSearchPath + "/color_right") else notInstallFlag
    
    answer = int(input("""Please enter the camera you are testing with:\n
    1. color_left {}
    2. color_right {}             
    3. color_down {} 
    4. color_left_&_right {}\n\n""".format(colorLeftFlag, colorRightFlag, colorDownFlag, colorBothFlag)))
    
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
    elif(answer==4):
        if colorBothFlag == notInstallFlag:
            print("Stereo camera not installed")
            sys.exit(0)
        else:
            camera="color_left"
    else:
        sys.exit("You entered an invalid value") 
    
    trajSearchPath = trajSearchPath + "/" + camera
    
    trajFileList = list(Path(trajSearchPath).rglob("[trajectory]*"))
    # print("#### trajFileList=",trajFileList)
    trajFileList = [str(a) for a in trajFileList if ("trajectory" in str(a) and ".bag" not in str(a))]
    # print("#### trajFileList=",trajFileList)

    return trajFileList


def unzip_file(file_zip_path):
    # open the zip file
    # zFile = zipfile.ZipFile(file_zip_path+'/frames.zip', "r")

    if not os.path.exists(file_zip_path+'/frames.zip'):
        print('File ',file_zip_path+'/frames.zip',' does NOT exist! Skipped...')

    else:
        zFile = zipfile.ZipFile(file_zip_path+'/frames.zip', "r")
        for fileM in zFile.namelist():
            # unzip frames from .zip file
            Path(zFile.extract(fileM,file_zip_path))
        zFile.close()
        print('Unzipped file', file_zip_path + '/frames.zip')
        # return file_zip_path



if __name__ == "__main__":
    main()