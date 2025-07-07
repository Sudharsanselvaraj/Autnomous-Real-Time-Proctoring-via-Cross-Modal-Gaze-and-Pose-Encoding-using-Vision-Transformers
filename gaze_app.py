import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained gaze model
model = load_model("gaze_model.h5")  # Ensure this file is in the same folder
labels = ['down', 'front', 'left', 'right']

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    resized = cv2.resize(frame, (64, 64))
    norm = resized.astype("float32") / 255.0
    input_img = np.expand_dims(norm, axis=0)

    # Predict gaze direction
    pred = model.predict(input_img)
    label = labels[np.argmax(pred)]

    # Display prediction
    cv2.putText(frame, f"Gaze: {label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Real-Time Gaze Detection", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
