# from celery import Celery
# from video_converter.video import VideoConverter

# # Create the Celery app
# celery_app = Celery(
#     "tasks",
#     broker="pyamqp://guest@localhost//",
#     broker_connection_retry_on_startup=True,
# )

# # Instantiate the VideoConverter class
# converter = VideoConverter()


# @celery_app.task(name="tasks.convert_video_task")
# def convert_video_task(temporary_path, output_path):
#     # Convert the video using VideoConverter

#     output_directory = "/Users/asilbekturgunboev/Desktop/video_conversion/converted_videos/"
#     resolutions = ["426x240", "640x360", "854x480", "1280x720"]
#     variants = [
#         {"name": "Low", "bitrate": 400000, "resolution": "426x240"},
#         {"name": "Medium", "bitrate": 800000, "resolution": "640x360"},
#         {"name": "High", "bitrate": 1600000, "resolution": "854x480"},
#         {"name": "Ultra", "bitrate": 4000000, "resolution": "1280x720"}
#     ]

#     # Convert the video with multiple resolutions
#     converter.convert_video(temporary_path, output_directory,
#                             resolutions, segment_time=10, playlist_size=0)

#     # Generate a list of playlist paths for each resolution
#     playlist_paths = [
#         f"{output_directory}_{i:03d}.m3u8" for i in range(1, len(resolutions) + 1)]

#     # Create the variant playlist
#     variant_playlist_path = "/Users/asilbekturgunboev/Desktop/video_conversion/variant_playlist_files/1.m3u8"
#     converter.create_variant_playlist(
#         playlist_paths, variant_playlist_path, variants)
#     return output_path
from celery import Celery
from video_converter.video import VideoConverter

# Create the Celery app
celery_app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",
    broker_connection_retry_on_startup=True,
)


@celery_app.task(name="tasks.convert_video_task")
def convert_video_task(temporary_path, output_path):
    # Instantiate the VideoConverter class
    converter = VideoConverter(
        input_video=None, output_path=None, resolutions=None)

    # Set up the VideoConverter instance
    resolutions = ["1280x720", "640x360", "426x240"]
    converter.input_video = temporary_path
    converter.output_path = output_path
    converter.resolutions = resolutions

    # Convert the video using VideoConverter
    converter.convert_video()

    # Return the output path
    return output_path
