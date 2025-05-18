from face_blur import face_blur
from ocr import blur_sensitive_data

def anonymize_image(image_bytes: bytes) -> bytes:
    return blur_sensitive_data(face_blur(image_bytes))