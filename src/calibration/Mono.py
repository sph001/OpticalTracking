from typing import Tuple
import Utilities.CalibrationStoreage as calibrationStorage
import numpy as np
import cv2
import os


class CameraCalibration:
    Manifest: [] = []
    Criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    Flags = cv2.CALIB_FIX_K4 | cv2.CALIB_FIX_K5 | cv2.CALIB_FIX_K6
    ObjectPoints: [] = []
    ImagePoints: [] = []
    CameraMatrix: np.ndarray = np.ndarray([])
    DistortionCoefficients: np.ndarray = np.ndarray([])
    RotationVectors: np.ndarray = np.ndarray([])
    TranslationVectors: np.ndarray = np.ndarray([])
    FrameSize: Tuple[int, int] = (-1, -1)
    FileName: str = ""
    OutputDirectory: str = ""
    StoredNPArrays = ["Manifest", "ObjectPoints", "ImagePoints", "CameraMatrix",
                        "DistortionCoefficients", "RotationVectors", "TranslationVectors"]
    StoredConfig = ["FileName", "OutputDirectory", "FrameSize"]

    def __init__(self, filename):
        self.FileName = filename
        self.OutputDirectory = os.path.join("Calibration", os.path.basename(filename.replace(".avi", "")))

    @staticmethod
    def load(folder):
        mc = CameraCalibration("")
        calibrationStorage.load(folder, mc)
        return mc

    def save(self):
        calibrationStorage.save(self)

    def detect_chessboard(self, board_size, skip_interval=1):
        self.Manifest = []
        self.ObjectPoints = []
        self.ImagePoints = []
        frame_output = os.path.join(self.OutputDirectory, "Frames")
        video = cv2.VideoCapture(self.FileName)
        obj_points = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        obj_points[:, :2] = np.mgrid[0:board_size[1] * 3:3, 0:board_size[0] * 3:3].T.reshape(-1, 2)
        self.FrameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if not os.path.exists(self.OutputDirectory):
            os.mkdir(self.OutputDirectory)
        if not os.path.exists(frame_output):
            os.mkdir(frame_output)
        count = 0
        print("detecting chessboard")
        while True:
            count += skip_interval
            video.set(cv2.CAP_PROP_POS_FRAMES, count)
            ret, frame = video.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, board_size)
            if ret:
                self.Manifest.append(count)
                cv2.imwrite(os.path.join(frame_output, "frame_" + str(count) + ".png"), frame)
                self.ObjectPoints.append(obj_points)
                corners2 = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), self.Criteria)
                self.ImagePoints.append(corners2)
        print("\tdone")

    def calibrate(self):
        print("calculating calibration")
        print("Number of frames: " + str(len(self.Manifest)))
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.ObjectPoints, self.ImagePoints, self.FrameSize,
                                                           None, None)
        print("\tdone")
        if ret:
            self.CameraMatrix = mtx
            self.DistortionCoefficients = dist
            self.RotationVectors = rvecs
            self.TranslationVectors = rvecs

    def remove_indexes(self, indexes: []):
        self.Manifest = np.delete(self.Manifest, indexes, 0)
        self.ObjectPoints = np.delete(self.ObjectPoints, indexes, 0)
        self.ImagePoints = np.delete(self.ImagePoints, indexes, 0)



