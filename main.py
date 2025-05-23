from fastapi import FastAPI, Request
from pydantic import BaseModel
from anonymize_text import anonymize_text
from anonymize_image import anonymize_image
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/anonymize/text")
async def analyze_text(request: TextRequest):
    text = request.text
    result = anonymize_text(text)
    print(result)
    return result

@app.post("/anonymize/image")
async def anonymize_img(request: Request):
    image_bytes = await request.body()
    anonymized_bytes = anonymize_image(image_bytes)
    return StreamingResponse(BytesIO(anonymized_bytes), media_type="image/jpeg")