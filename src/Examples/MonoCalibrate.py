import os
import calibration.Mono as cc
from sys import argv
_, fileName = argv

basedir = os.getcwd()
calibration = cc.CameraCalibration(basedir, fileName)

calibration.detect_chessboard((8, 13), 50)
calibration.calibrate()

calibration.save()
