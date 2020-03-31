import calibration.Mono as cc
import calibration.Stereo as sc
import cv2
import numpy as np
import os
from sys import argv
_, leftFolder, rightFolder = argv


def undistort(camera: cc.CameraCalibration, r, p, img):
    mapx, mapy = cv2.initUndistortRectifyMap(camera.CameraMatrix, camera.DistortionCoefficients, r, p, camera.FrameSize, cv2.CV_32FC1)
    return cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)


stereoCalib = sc.StereoCalibration.load('Calibration')
l_img = cv2.imread(os.path.join(leftFolder, "Frames", "frame_20.png"))
r_img = cv2.imread(os.path.join(rightFolder, "Frames", "frame_20.png"))
r1, r2, p1, p2, q, _, _ = cv2.stereoRectify(stereoCalib.Left.CameraMatrix, stereoCalib.Left.DistortionCoefficients,
                                      stereoCalib.Right.CameraMatrix, stereoCalib.Right.DistortionCoefficients,
                                      stereoCalib.Left.FrameSize, stereoCalib.Rotation, stereoCalib.Translation)

cv2.imshow('frame', np.hstack([l_img, r_img]))
l_rect = cv2.undistort(l_img, stereoCalib.Left.CameraMatrix, stereoCalib.Left.DistortionCoefficients) ##undistort(stereoCalib.Right, r1, p1, l_img)
r_rect = cv2.undistort(r_img, stereoCalib.Right.CameraMatrix, stereoCalib.Right.DistortionCoefficients)##undistort(stereoCalib.Left, r2, p2, r_img)
cv2.imshow('undistorted', np.hstack([l_rect, r_rect]))
cv2.waitKey(0)
print("done")