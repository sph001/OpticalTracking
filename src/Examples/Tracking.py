from calibration.Mono import CameraCalibration
import cv2
import cv2.aruco as aruco
from PIL import Image

leftCalibFolder = "Calibration\\EndoscopeImageMemory_1_Calibration"
videoPath = r'EndoscopeImageMemory_0_X_Motion.avi'
calib = CameraCalibration.load(leftCalibFolder)
video = cv2.VideoCapture(videoPath)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters_create()
frames = []
output = cv2.VideoWriter('tracked.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, calib.FrameSize)
count = -1
while True:
    count += 1
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    frame = aruco.drawDetectedMarkers(frame, corners)
    rv, tv, _ = aruco.estimatePoseSingleMarkers(corners, 0.05, calib.CameraMatrix, calib.DistortionCoefficients)
    if rv is not None:
        pos = (round(tv[0][0][0], 2), round(tv[0][0][1], 2), round(tv[0][0][2], 2))
        frame = aruco.drawAxis(frame, calib.CameraMatrix, calib.DistortionCoefficients, rv, tv, 0.1)
        frame = cv2.putText(frame, str(pos), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
        cv2.imshow('frame', frame)
        output.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video.release()
output.release()
cv2.destroyAllWindows()
