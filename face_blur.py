import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_blur(image_bytes: bytes) -> bytes:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_region = img[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
        img[y:y+h, x:x+w] = blurred_face

    _, buffer = cv2.imencode('.jpg', img)
    return buffer.tobytes()

if __name__ == "__main__":
    input = '../../examples/10group.jpg'
    output = '../../anonymized_examples/anonymized_3.jpg'
    # blur_face()