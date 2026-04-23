from ultralytics import YOLO
model = YOLO('yolo11n_object365.pt')
# Export to NCNN (very efficient for Pi CPU)
model.export(format='ncnn')