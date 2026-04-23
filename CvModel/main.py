import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import time

# 1. Load your NCNN model - ensure the folder is in the same directory
model = YOLO('yolo11n_object365_ncnn_model', task='detect')

# 2. Setup the IMX Camera (Optimized for Pi 5)
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)})
picam2.configure(config)
picam2.start()

# 3. Setup Video Writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('robot_output.avi', fourcc, 10.0, (640, 480)) # Bumped to 10fps

print("Pi 5 YOLO Inference Started. Press Ctrl+C to stop...")

try:
    while True:
        # Capture frame
        frame = picam2.capture_array()

        # Run inference - added stream=True and half=True for Pi 5 speed
        results = model.predict(frame, conf=0.25, verbose=False, stream=True, half=True)

        for result in results:
            # Draw the bounding boxes
            annotated_frame = result.plot()

            # Convert RGB to BGR for OpenCV
            annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

            # Display on the HDMI monitor
            cv2.imshow("Robot Feed", annotated_frame_bgr)
            
            # Save to file
            out.write(annotated_frame_bgr)

            # Print what we see
            if len(result.boxes) > 0:
                print(f"Seeing {len(result.boxes)} objects")
            else:
                print("Searching...")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Stopping...")

finally:
    picam2.stop()
    out.release()
    cv2.destroyAllWindows()