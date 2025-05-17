from fastapi import FastAPI
from pydantic import BaseModel
from anonymizer import anonymize

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/anonymize")
async def analyze_text(request: TextRequest):
    text = request.text
    result = anonymize(text)
    print(result)
    return result
