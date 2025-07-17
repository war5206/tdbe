from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from app.schemas.hello_world import HelloWorldRequest, HelloWorldResponse
from app.services.aliyun.ASR.single import AliRecognizer

router = APIRouter(prefix="/asr", tags=["一句话语音识别"])

import subprocess
import tempfile
import os

def convert_webm_to_wav(webm_bytes: bytes) -> bytes:
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as input_file:
        input_file.write(webm_bytes)
        input_path = input_file.name

    output_path = input_path.replace(".webm", ".wav")

    try:
        subprocess.run([
            "ffmpeg", "-i", input_path,
            "-ar", "16000", "-ac", "1", "-f", "wav", output_path
        ], check=True)

        with open(output_path, "rb") as f:
            wav_bytes = f.read()

        return wav_bytes
    finally:
        os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)


@router.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    content = await file.read()
    wav_data = convert_webm_to_wav(content)
    
    recognizer = AliRecognizer(wav_data)

    result = recognizer.recognize()

    return {"text": result}