from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
from ultralytics import YOLO

app = Flask(__name__)
socketio = SocketIO(app)
model = YOLO("yolov8x.pt") 

def generate_frames():
    camera = cv2.VideoCapture(0)  # index of primary camera

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame, conf=0.5, stream=True)

            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        class_idx = int(box.cls[0])  # class index
                        class_name = result.names[class_idx]  # class name from index
                        confidence = float(box.conf[0])  # confidence score

                        # draw the bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                        # draw the label text
                        label = f"{class_name} ({confidence:.2f})"
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # encode the frame
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    socketio.run(app, debug=True)