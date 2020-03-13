import cv2
import numpy as np
from calibration.Mono import CameraCalibration as calibration


class StereoCalibration:
    Rotation = []
    Translation = []
    Essential = []
    Fundamental = []

    def __init__(self, left: calibration, right: calibration):
        self.Left = left
        self.Left.load_calibration()
        self.Right = right
        self.Right.load_calibration()

    def sync_datasets(self):
        '''used to make sure that both cameras are calibrating off the same set of frames'''
        if len(self.Left.Manifest) == len(self.Right.Manifest):
            return
        lc = 0
        rc = 0
        lToDrop = []
        rToDrop = []
        for i in range(0, len(self.Left.Manifest)):
            if lc+i >= len(self.Left.Manifest) or rc+i >= len(self.Right.Manifest):
                break
            if self.Left.Manifest[lc+i] == self.Right.Manifest[rc+i]:
                continue
            while self.Left.Manifest[lc+i] < self.Right.Manifest[rc+i]:
                lToDrop.append(lc+i)
                lc += 1
            while self.Left.Manifest[lc+i] > self.Right.Manifest[rc+i]:
                rToDrop.append(rc+i)
                rc += 1
        self.Left.remove_indexes(lToDrop)
        self.Right.remove_indexes(rToDrop)

    def calibrate(self):
        self.sync_datasets()

        ret, lcm, ldc, rcm, rdc, r, t, e, f = cv2.stereoCalibrate(self.Left.ObjectPoints, self.Left.ImagePoints, self.Right.ImagePoints, (720, 576), None, None, None, None)
        if ret:
            self.Left.CameraMatrix = lcm
            self.Left.DistanceCoefficients = ldc
            self.Right.CameraMatrix = rcm
            self.Right.DistanceCoefficients = ldc
            self.Rotation = r
            self.Translation = t
            self.Essential = e
            self.Fundamental = f

    def load(self, folder):
        self.Rotation = np.load(folder+"\\StereoRotation.npy")
        self.Translation = np.load(folder+"\\StereoTranslation")
        self.Essential = np.load(folder+"\\StereoEssential")
        self.Fundamental = np.load(folder+"\\StereoFundamental")

    def save(self, output):
        self.Left.save()
        self.Right.save()
        np.save(output+"\\StereoRotation", self.Rotation)
        np.save(output+"\\StereoTranslation", self.Translation)
        np.save(output+"\\StereoEssential", self.Essential)
        np.save(output+"\\StereoFundamental", self.Fundamental)

