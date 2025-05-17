from lib.face_blur import face_blur

def anonymize_image(image_bytes: bytes) -> bytes:
    return face_blur(image_bytes)