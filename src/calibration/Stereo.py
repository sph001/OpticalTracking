import cv2
import numpy as np
from calibration.Mono import CameraCalibration
import Utilities.CalibrationStoreage as calibrationStorage
from operator import attrgetter


class StereoCalibration:
    Rotation = []
    Translation = []
    Essential = []
    Fundamental = []
    OutputDirectory = "Calibration"
    Left = None
    Right = None
    StoredNPArrays = ["Rotation", "Translation",
                      "Essential", "Fundamental"]
    StoredConfig = ["Left-OutputDirectory", "Right-OutputDirectory"]

    @staticmethod
    def load(folder) -> 'StereoCalibration':
        sc = StereoCalibration(calibrationStorage.Complex, calibrationStorage.Complex)
        calibrationStorage.load(folder, sc)
        sc.Left = CameraCalibration.load(sc.Left.OutputDirectory)
        sc.Right = CameraCalibration.load(sc.Right.OutputDirectory)
        return sc

    def save(self):
        calibrationStorage.save(self)
        calibrationStorage.save(self.Left)
        calibrationStorage.save(self.Right)

    def __init__(self, left: CameraCalibration or calibrationStorage.Complex, right: CameraCalibration or calibrationStorage.Complex):
        self.Left = left
        self.Right = right

    def sync_data_sets(self):
        '''used to make sure that both cameras are calibrating off the same set of frames'''
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
        self.sync_data_sets()

        ret, lcm, ldc, rcm, rdc, r, t, e, f = cv2.stereoCalibrate(self.Left.ObjectPoints, self.Left.ImagePoints,
                                                                  self.Right.ImagePoints,
                                                                  self.Left.CameraMatrix, self.Left.DistortionCoefficients,
                                                                  self.Right.CameraMatrix, self.Right.DistortionCoefficients,
                                                                  self.Left.FrameSize)
        if ret:
            self.Left.CameraMatrix = lcm
            self.Left.DistortionCoefficients = ldc
            self.Right.CameraMatrix = rcm
            self.Right.DistortionCoefficients = ldc
            self.Rotation = r
            self.Translation = t
            self.Essential = e
            self.Fundamental = f

