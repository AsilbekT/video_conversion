from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from credentials import OUTPUT_PATH
from tasks.celery_app import convert_video_task
import os

app = FastAPI()


class VideoPayload(BaseModel):
    status: str
    message: str
    video_url: str
    content_id: int
    video_type: str


@app.post("/convert")
async def handle_video_conversion(video_payload: VideoPayload):
    video_url = video_payload.video_url
    content_id = video_payload.content_id
    video_type = video_payload.video_type

    if not os.path.exists(video_url):
        raise HTTPException(
            status_code=400, detail="Video file does not exist"
        )

    convert_video_task.delay(video_url, OUTPUT_PATH,
                             content_id, video_type)

    return {"status": "success", "message": "Video conversion initiated and database updated"}
