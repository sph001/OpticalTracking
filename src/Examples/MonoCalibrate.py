import os
import calibration.Mono as cc
from sys import argv
_, fileName = argv

basedir = os.getcwd()
calibration = cc.CameraCalibration(fileName)

calibration.detect_chessboard((8, 13), 20)
calibration.calibrate()

calibration.save()
