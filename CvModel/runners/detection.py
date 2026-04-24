import cv2
from ultralytics import YOLO

# Utils
from get_location import get_coordinates_from_bb
from navigate import Navigate

model = YOLO('yolo11n_object365_ncnn_model', task='detect')

# Golf balls and objects that could be mistaken for golf balls depending on lighting conditions
BALL_WHITELIST = [82, 90, 94, 118, 156, 177, 185, 189, 239, 247, 364]


def main_detection_loop():
    # Setup USB Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    navigator = Navigate()  # Initialize class used for all navigation functionality

    print("Detection Activated")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Run YOLOv11 inference
            results = model.predict(frame, conf=0.20, verbose=False, stream=True, half=True)

            for result in results:
                closest_box = None
                max_width = 0

                # Choose closest ball in the case of multiple balls
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    if class_id in BALL_WHITELIST:
                        x1, y1, x2, y2 = box.xyxy[0]
                        width = x2 - x1
                        
                        if width > max_width:
                            max_width = width
                            closest_box = box

                if closest_box:
                    coords = get_coordinates_from_bb(closest_box)
                    print(coords)  # For verification
		    navigator.move(coords[0], coords[1])  # Perform navigation flow
	            # Actions stop until finished
                
            # Stop early
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main_detection_loop()
