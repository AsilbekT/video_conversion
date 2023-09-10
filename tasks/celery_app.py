from botocore.config import Config
import os
from celery import Celery
from video_converter.video import VideoConverter
from app.utils.update_content_url import content_exists, update_content_url
import logging
from credentials import PLAYBACK_SERVICE

# Initialize a logger
logger = logging.getLogger(__name__)

# Create the Celery app
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",
    broker_connection_retry_on_startup=True,
)


@celery_app.task(name="tasks.convert_video_task")
def convert_video_task(temporary_path, output_path, content_id, video_type):
    # Check if the content exists in the database before initiating the conversion
    if not content_exists(content_id, video_type):
        logger.warning(
            f"No content found with ID {content_id} and type {video_type}. Aborting conversion.")
        return None

    # Instantiate the VideoConverter class
    converter = VideoConverter(
        input_video=None, output_path=None, resolutions=None)

    # Set up the VideoConverter instance
    resolutions = ["1280x720", "640x360", "426x240"]
    converter.input_video = temporary_path
    converter.output_path = output_path
    converter.resolutions = resolutions

    try:
        # Convert the video using VideoConverter
        converter.convert_video()
        video_id = converter.video_id
        video_path = f"{video_id}/master.m3u8"

        # Determine the correct URL type based on the video type and whether it's a trailer
        url_type = video_type

        # Update the content URL in the database
        update_content_url(content_id, video_path, url_type)

        # Remove the temporary file
        os.remove(temporary_path)
        logger.info(f"Successfully removed temporary file: {temporary_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    return output_path
