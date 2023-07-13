#!/usr/bin/env python3

"""
    @author: Cheng Zhang
    
    BRIEF:  Run this script in the path of Mid-Air dataset to unzip the original documents
    
"""

# for file path interpretation and representation    
import os
# for exit control
import sys
# for some file representation stuff
from pathlib import Path

import zipfile
def main():
    unzip_file('/home/cor21cz/dataset/MidAir/Kite_training/sunny/color_left/trajectory_0007')

def unzip_file(file_zip_path):
    # open the zip file
    zFile = zipfile.ZipFile(file_zip_path+'/frames.zip', "r")
    for fileM in zFile.namelist():
        # unzip frames from .zip file
        Path(zFile.extract(fileM,file_zip_path))
    zFile.close()
    print('Unzipped file', file_zip_path + '/frames.zip')
    return file_zip_path


if __name__ == "__main__":
    main()