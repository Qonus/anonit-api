import pytesseract
from PIL import ImageFilter, Image
from io import BytesIO
from anonymize_text import analyze_text

def blur_sensitive_data(image_bytes: bytes) -> bytes:
    img = Image.open(BytesIO(image_bytes))
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    boxes_to_blur = []

    for i, word in enumerate(data['text']):
        if word.strip():
            results = analyze_text(text=word)
            if results:
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                boxes_to_blur.append((x, y, x + w, y + h))

    for box in boxes_to_blur:
        region = img.crop(box)
        blurred = region.filter(ImageFilter.GaussianBlur(radius=15))
        img.paste(blurred, box)

    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    output_bytes = output_buffer.getvalue()
    return output_bytes
