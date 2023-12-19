from celery import Celery
from video_converter.video import VideoConverter
from app.utils.video_resalutions import get_video_resolution, generate_resolutions
from app.utils.update_content_url import content_exists, update_content_url
import logging
import os

# Initialize logger and Celery app (assuming credentials and other necessary imports are done)
logger = logging.getLogger(__name__)
celery_app = Celery("tasks", broker="pyamqp://guest@localhost//",
                    broker_connection_retry_on_startup=True)


@celery_app.task(name="tasks.convert_video_task")
def convert_video_task(temporary_path, output_path, content_id, video_type):
    if not content_exists(content_id, video_type):
        logger.warning(
            f"No content found with ID {content_id} and type {video_type}. Aborting conversion.")
        return None

    try:
        # Get input video resolution
        # input_width, input_height = get_video_resolution(temporary_path)

        # # Generate dynamic resolutions based on input video
        # resolutions = generate_resolutions(input_width, input_height)

        # Instantiate the VideoConverter class
        converter = VideoConverter(
            input_video=temporary_path,
            output_path=output_path,
            resolutions=['1280x720', '640x360', '426x240']
        )

        # Convert the video
        converter.convert_video()
        video_id = converter.video_id
        video_path = f"{video_id}/master.m3u8"

        # Update content URL in the database
        update_content_url(content_id, video_path, video_type)

        # Remove the temporary file
        os.remove(temporary_path)
        logger.info(f"Successfully removed temporary file: {temporary_path}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Ensure temporary file is removed even if an error occurs
        if os.path.exists(temporary_path):
            os.remove(temporary_path)
            logger.error(
                f"Temporary file removed after error: {temporary_path}")

    return output_path
