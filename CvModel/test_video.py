from ultralytics import YOLO

model = YOLO('yolo11n_object365_ncnn_model') 

# Remove show=True, add save=True
# This will save the output to runs/detect/predict/
model.predict(source=0, save=True, conf=0.5)