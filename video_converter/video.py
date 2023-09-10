import subprocess
import uuid


class VideoConverter:
    def __init__(self, input_video, output_path, resolutions):
        self.input_video = input_video
        self.output_path = output_path
        # List of resolutions in format ["1280x720", "640x360", ...]
        self.resolutions = resolutions
        self.video_id = None  # unique video id

    def _generate_base_command(self):
        self.video_id = str(uuid.uuid4())
        return ['ffmpeg', '-i', self.input_video, '-filter_complex']

    def _generate_filter_complex_command(self):
        split_command = f'[0:v]split={len(self.resolutions)}' + ''.join(
            [f'[v{i}]' for i in range(len(self.resolutions))])
        scale_commands = ''.join(
            [f'[v{i}]scale={res.split("x")[0]}:{res.split("x")[1]}[v{i}out];' for i, res in enumerate(self.resolutions)])
        return f'"{split_command};{scale_commands[:-1]}"'

    def _generate_video_commands(self):
        video_commands = []
        bitrates = ['5M', '3M', '1M']
        for i in range(len(self.resolutions)):
            video_commands.append(
                f'-map [v{i}out] -c:v:{i} libx264 -x264-params nal-hrd=cbr:force-cfr=1 -b:v:{i} {bitrates[i]} -maxrate:v:{i} {bitrates[i]} -minrate:v:{i} {bitrates[i]} -bufsize:v:{i} {bitrates[i]} -preset slow -g 48 -sc_threshold 0 -keyint_min 48')
        return video_commands

    def _generate_audio_commands(self):
        return ['-map a:0 -c:a:0 aac -b:a:0 96k -ac 2', '-map a:0 -c:a:1 aac -b:a:1 96k -ac 2', '-map a:0 -c:a:2 aac -b:a:2 48k -ac 2']

    def _generate_hls_commands(self):

        return [
            '-f hls',
            '-hls_time 2',
            '-hls_playlist_type vod',
            '-hls_flags independent_segments',
            '-hls_segment_type mpegts',
            '-hls_segment_filename ' +
            f"{self.output_path}/{self.video_id}/stream_%v/data%02d.ts",
            '-master_pl_name ' +
            f'master.m3u8'
        ]

    def convert_video(self):
        command = (
            self._generate_base_command() +
            [self._generate_filter_complex_command()] +
            self._generate_video_commands() +
            self._generate_audio_commands() +
            self._generate_hls_commands() +
            ['-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2"'] +
            [f"{self.output_path}/{self.video_id}/stream_%v/final.m3u8"]
        )
        # print(self._generate_hls_commands())
        command = ' '.join(command)
        subprocess.run(command, shell=True, check=True)
