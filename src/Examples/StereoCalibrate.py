import calibration.Mono as cc
import calibration.Stereo as sc
import os
from sys import argv
_, leftFolder, rightFolder = argv

baseDir = os.getcwd()
left = cc.CameraCalibration(baseDir, leftFolder)
right = cc.CameraCalibration(baseDir, rightFolder)

stereoCalib = sc.StereoCalibration(left, right)
stereoCalib.calibrate()
print("calibration Complete")
stereoCalib.save(baseDir + "\\calibration")
print("done")
exit()