from fastapi import FastAPI, UploadFile, File
from tasks.celery_app import convert_video_task
import os

app = FastAPI()


@app.post("/convert")
async def handle_video_conversion(video: UploadFile = File(...)):
    # Save the uploaded video to a temporary file
    current_directory = os.getcwd()
    temporary_path = os.path.join(current_directory, video.filename)

    with open(temporary_path, "wb") as temp_file:
        temp_file.write(await video.read())

    # Define the output path for the converted video
    output_path = "/Users/asilbekturgunboev/Desktop/video_conversion/converted_videos"

    convert_video_task.delay(temporary_path, output_path)

    # Return the converted video URL or other response data
    return {"status": "success", "message": "Video recieved successfully"}
