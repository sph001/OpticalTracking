import calibration.Mono as cc
import calibration.Stereo as sc
import cv2
import numpy as np
import os
from sys import argv
_, leftFolder, rightFolder = argv

baseDir = os.getcwd()
left = cc.CameraCalibration.load(leftFolder)
right = cc.CameraCalibration.load(rightFolder)
stereoCalib = sc.StereoCalibration(left, right)
print("calibration started")
stereoCalib.calibrate()
print("\tdone")
stereoCalib.save()

