import cv2
import math
from ultralytics import YOLO

FOCAL_LENGTH = 515
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
HORIZ_CAM_CENTER = FRAME_WIDTH
GOLF_BALL_DIAMETER = 0.0427

MODEL_PATH = '../yolo11n_object365_ncnn_model'

BALL_WHITELIST = [82, 90, 94, 118, 156, 177, 185, 189, 239, 247, 364]

_model = None
_cap = None

def setup():
    global _model, _cap
    _model = YOLO(MODEL_PATH, task='detect')
    _cap = cv2.VideoCapture(0)
    _cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    _cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

def cleanup():
    global _cap
    if _cap is not None:
        _cap.release()
        _cap = None

def get_frame():
    if _cap is None:
        raise RuntimeError("Camera not initialised — call setup() first.")
    ret, frame = _cap.read()
    return frame if ret else None


def _closest_ball_box(frame):
    results = _model.predict(frame, conf=0.20, verbose=False, stream=True, half=True)
    closest_box = None
    max_width = 0

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id in BALL_WHITELIST:
                x1, _, x2, _ = box.xyxy[0]
                width = x2 - x1
                if width > max_width:
                    max_width = width
                    closest_box = box

    return closest_box

def get_target(frame):
    box = _closest_ball_box(frame)
    if box is None:
        return None

    x1, _, x2, _ = box.xyxy[0].tolist()
    w_px = x2 - x1

    if w_px < 5:
        return None

    cx_px = (x1 + x2) / 2

    angle_deg = math.degrees(math.atan2(cx_px - HORIZ_CAM_CENTER, FOCAL_LENGTH))

    distance_m = (GOLF_BALL_DIAMETER * FOCAL_LENGTH) / w_px

    return {
        'angle_deg': angle_deg,
        'distance_m': distance_m,
    }
