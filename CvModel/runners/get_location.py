import numpy as np

def get_coordinates_from_bb(box):
    # Constants
    GOLF_BALL_DIAMETER = 0.0427 
    FOCAL_LENGTH = 515
    
    HORIZ_CAM_CENTER = 320
    VERT_CAM_CENTER = 240

    coords = box.xyxy[0].tolist()
    x1, y1, x2, y2 = coords
    w_px = x2 - x1
    
    # Helps reduce false positives
    if w_px < 5: 
        return None

    cx_px = (x1 + x2) / 2
    cy_px = (y1 + y2) / 2

    # 1. Distance from camera to ball (Forward)
    z_cam = (GOLF_BALL_DIAMETER * FOCAL_LENGTH) / w_px
    
    # 2. Horizontal offset from center (Side-to-side)
    x_cam = (cx_px - HORIZ_CAM_CENTER) * z_cam / FOCAL_LENGTH
    
    # 3. Vertical offset (Up/Down)
    y_cam = (cy_px - VERT_CAM_CENTER) * z_cam / FOCAL_LENGTH

    # 4. Map to Robot Frame
    # [Forward Distance, Left/Right, Up/Down]
    return np.array([z_cam, x_cam, -y_cam])
