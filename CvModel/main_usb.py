import cv2
from ultralytics import YOLO

# 1. Load your NCNN model
model = YOLO('yolo11n_object365_ncnn_model', task='detect')

# 2. Setup USB Camera (0 is usually the first USB cam)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
# Set resolution to match the model
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Set FPS to avoid "buffer lag"
cap.set(cv2.CAP_PROP_FPS, 30)
# 3. Setup Video Writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('robot_output.avi', fourcc, 10.0, (640, 480))

print("USB Cam YOLO Started. Press 'q' to stop...")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Run inference (stream=True for Pi 5 memory management)
        results = model.predict(frame, conf=0.25, verbose=False, stream=True, half=True)

        for result in results:
            annotated_frame = result.plot()
            
            # Display and Save
            cv2.imshow("Robot Feed", annotated_frame)
            out.write(annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    out.release()
    cv2.destroyAllWindows()