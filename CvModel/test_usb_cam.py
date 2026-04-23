from ultralytics import YOLO


model = YOLO('yolo11n_object365.pt')


# Remove show=True, add save=True

# This will save the output to runs/detect/predict/

model.predict(source=1, save=True, conf=0.33) 