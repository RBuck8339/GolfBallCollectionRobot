import numpy as np

def get_coordinates_from_bb(box):
    """
    All variables are in meters, takes in a YOLO bounding box
    """

    # Constants
    GOLF_BALL_DIAMETER = 0.0427  # Estimated from google standard golf ball diameter, can help
    FOCAL_LENGTH = 550  # Estimate

    # Helps in calculations finding center of cam
    HORIZ_CAM_CENTER = 320
    VERT_CAM_CENTER = 240

    # Camera offsets from base frame
    X_OFFSET = 0.05  
    Y_OFFSET = 0.0  
    Z_OFFSET = 0.10  

    coords = box.xyxy[0].tolist()
    x1, y1, x2, y2 = coords
    w_px = x2 - x1
    cx_px = (x1 + x2) / 2
    cy_px = (y1 + y2) / 2

    # Calculate 3 offsets
    z_cam = (GOLF_BALL_DIAMETER * FOCAL_LENGTH) / w_px
    x_cam = (cx_px - HORIZ_CAM_CENTER) * z_cam / FOCAL_LENGTH
    y_cam = (cy_px - VERT_CAM_CENTER) * z_cam / FOCAL_LENGTH

    # 4. Transform to Base Frame
    robot_x = z_cam + X_OFFSET
    robot_y = x_cam + Y_OFFSET
    robot_z = Z_OFFSET - y_cam

    return np.array([robot_x, robot_y, robot_z])