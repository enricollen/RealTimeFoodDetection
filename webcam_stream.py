from ultralytics import YOLO

model = YOLO("yolov8s.pt")

results = model(source="0", show=True, conf=0.5, stream=True)  # accepts all formats

for r in results:
    boxes = r.boxes  # Boxes object for bbox outputs
    masks = r.masks  # Masks object for segment masks outputs
    probs = r.probs  # Class probabilities for classification outputs
    print(boxes)
    print(masks)
    print(probs)