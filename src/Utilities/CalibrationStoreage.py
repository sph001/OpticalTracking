import numpy as np
import os
import cv2
from operator import attrgetter


class Complex(object):
    pass


def load(folder, new_calibration):
    new_calibration.OutputDirectory = folder
    load_data(new_calibration)
    load_config(new_calibration)


def save(obj):
    save_data(obj)
    save_config(obj)


def load_data(obj):
    for k in obj.StoredNPArrays:
        setattr(obj, k, np.load(os.path.join(obj.OutputDirectory, k + ".npy")))


def save_data(obj):
    for k in obj.StoredNPArrays:
        np.save(os.path.join(obj.OutputDirectory, k), getattr(obj, k))


def load_config(obj):
    fs = cv2.FileStorage(os.path.join(obj.OutputDirectory, "Config.yaml"), cv2.FILE_STORAGE_READ)
    for k in obj.StoredConfig:
        if not k == "FrameSize":
            if "-" in k:
                ks = k.split('-')
                setattr(getattr(obj, ks[0]), ks[1], fs.getNode(k).string())
            else:
                setattr(obj, k, fs.getNode(k).string())
        else:
            v = fs.getNode(k).mat()
            setattr(obj, k, (int(v[0]), int(v[1])))
    fs.release()


def save_config(obj):
    fs = cv2.FileStorage(os.path.join(obj.OutputDirectory, "Config.yaml"), cv2.FILE_STORAGE_WRITE)
    for k in obj.StoredConfig:
        fs.write(k, attrgetter(k.replace('-', '.'))(obj))
    fs.release()