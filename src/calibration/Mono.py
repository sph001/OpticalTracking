import numpy as np
import cv2
import os


class CameraCalibration:
    Manifest = []
    ObjectPoints = []
    ImagePoints = []
    CameraMatrix = []
    DistortionCoefficients = []
    RotationVectors = []
    TranslationVectors = []
    frameSize = (-1, -1)
    Directory = ""
    FileName = ""
    OutputDirectory = ""

    def __init__(self, directory, filename):
        filename = filename.replace(".\\Calibration\\", "\\")
        self.Directory = directory + "\\"
        self.FileName = filename
        self.OutputDirectory = self.Directory + "Calibration\\" + filename.replace(".avi", "")
        self.Criteria = (cv2.TermCriteria_EPS + cv2.TermCriteria_MAX_ITER, 30, 0.001)

    def detect_chessboard(self, board_size, skip_interval=1):
        frame_output = self.OutputDirectory + "\\Frames"
        video = cv2.VideoCapture(self.FileName)
        obj_points = np.zeros((board_size[0] * board_size[1], 3), np.float32)
        obj_points[:, :2] = np.mgrid[0:board_size[1] * 3:3, 0:board_size[0] * 3:3].T.reshape(-1, 2)
        self.frameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        if not os.path.exists(self.OutputDirectory):
            os.mkdir(self.OutputDirectory)
        if not os.path.exists(frame_output):
            os.mkdir(frame_output)
        count = 0
        print("detecting chessboard")
        while True:
            count += 1
            ret, frame = video.read()
            if not ret:
                break
            if count % skip_interval == 0:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, board_size, None)
                if ret:
                    np.append(self.Manifest, count)
                    cv2.imwrite(frame_output + "\\frame_" + str(count) + ".png", frame)
                    np.append(self.ObjectPoints, obj_points)
                    corners2 = cv2.cornerSubPix(gray, corners, (3, 3), (-1, -1), self.Criteria)
                    np.append(self.ImagePoints, corners2)
        print("\tdone")

    def calibrate(self):
        print("calculating calibration")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self.ObjectPoints, self.ImagePoints, self.frameSize, None, None)
        print("\tdone")
        if ret:
            self.CameraMatrix = mtx
            self.DistortionCoefficients = dist
            self.RotationVectors = rvecs
            self.TranslationVectors = rvecs

    def load_calibration(self):
        self.Manifest = self.load_file(self.OutputDirectory, "Manifest")
        self.ObjectPoints = self.load_file(self.OutputDirectory, "ObjectPoints")
        self.ImagePoints = self.load_file(self.OutputDirectory, "ImagePoints")

    def remove_indexes(self, indexes: []):
        self.Manifest = np.delete(self.Manifest, indexes, 0)
        self.ObjectPoints = np.delete(self.ObjectPoints, indexes, 0)
        self.ImagePoints = np.delete(self.ImagePoints, indexes, 0)

    def save(self):
        np.save(self.OutputDirectory + "\\ObjectPoints", self.ObjectPoints)
        np.save(self.OutputDirectory + "\\ImagePoints", self.ImagePoints)
        np.save(self.OutputDirectory + "\\Manifest", self.Manifest)
        np.save(self.OutputDirectory + "\\CameraMatrix", self.CameraMatrix)
        np.save(self.OutputDirectory + "\\DistortionCoefficients", self.DistortionCoefficients)
        np.save(self.OutputDirectory + "\\RotationVectors", self.RotationVectors)
        np.save(self.OutputDirectory + "\\TranslationVectors", self.TranslationVectors)

    @staticmethod
    def load_file(directory, name) -> np.ndarray:
        file = directory + "\\" + name + ".npy"
        return np.load(file)
