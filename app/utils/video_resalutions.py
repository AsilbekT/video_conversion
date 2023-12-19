import subprocess
import json


def get_video_resolution(video_path):
    """Get the resolution of the video."""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    video_info = json.loads(result.stdout)
    width = video_info['streams'][0]['width']
    height = video_info['streams'][0]['height']
    return width, height


def generate_resolutions(input_width, input_height):
    """Generate a list of resolutions for conversion based on input video resolution."""
    standard_resolutions = [
        ("3840x2160", 2160),  # 4K
        ("1920x1080", 1080),  # Full HD
        ("1280x720", 720),    # HD
        ("854x480", 480),     # SD
        ("640x360", 360),     # nHD
        ("426x240", 240)      # qHD
    ]
    return [res for res, height in standard_resolutions if height <= input_height]
