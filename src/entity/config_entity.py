from src.constants import *
import os

class ConfigEntity:
    def __init__(self):
        self.eps = EPS
        self.min_samples = MIN_SAMPLES
        self.metric = METRIC
        self.frame_rate = FRAME_RATE
        self.output_dir = OUTPUT_DIR
        self.temp_audio_extension = TEMP_AUDIO_EXTENSION
        self.input_video_filename = INPUT_VIDEO_FILENAME
        self.sticker_filename = STICKER_FILENAME
        self.output_video_filename = OUTPUT_VIDEO_FILENAME
        self.final_output_filename = FINAL_OUTPUT_FILENAME
        self.preview_filename_prefix = PREVIEW_FILENAME_PREFIX
        self.preview_extension = PREVIEW_EXTENSION

class FaceExtractorConfig:
    def __init__(self, config: ConfigEntity, session_id: str):
        self.output_dir = config.output_dir
        self.session_id = session_id
        self.input_video_filename = config.input_video_filename

class ClustererConfig:
    def __init__(self, config: ConfigEntity, session_id: str):
        self.eps = config.eps
        self.min_samples = config.min_samples
        self.metric = config.metric
        self.output_dir = config.output_dir
        self.session_id = session_id

class StickerOverlayConfig:
    def __init__(self, config: ConfigEntity, session_id: str):
        self.frame_rate = config.frame_rate
        self.output_dir = config.output_dir
        self.session_id = session_id
        self.sticker_filename = config.sticker_filename
        self.output_video_filename = config.output_video_filename

class AudioMergerConfig:
    def __init__(self, config: ConfigEntity, session_id: str):
        self.output_dir = config.output_dir
        self.session_id = session_id
        self.temp_audio_extension = config.temp_audio_extension
        self.final_output_filename = config.final_output_filename

# class ConfigEntity:
#     def __init__(self):
#         self.eps = EPS
#         self.min_samples = MIN_SAMPLES
#         self.metric=METRIC
#         self.frame_rate = FRAME_RATE
#         self.output_dir = OUTPUT_DIR
#         self.temp_audio_extension=TEMP_AUDIO_EXTENSION
#         self.input_video_file=INPUT_VIDEO_FILENAME
        

# class FaceExtractorConfig:
#     def __init__(self, config: ConfigEntity, session_id: str):
#         self.output_dir = config.output_dir
#         self.session_id = session_id
#         self.session_path = os.path.join(self.output_dir, session_id)
#         self.video_path = os.path.join(self.session_path, config.input_video_file)

# class ClustererConfig:
#     def __init__(self, config: ConfigEntity, session_id: str):
#         self.eps = config.eps
#         self.min_samples = config.min_samples
#         self.metric=config.metric
#         self.output_dir = config.output_dir
#         self.session_id = session_id
#         self.session_path = os.path.join(self.output_dir, session_id)

# class StickerOverlayConfig:
#     def __init__(self, config: ConfigEntity, session_id: str):
#         self.frame_rate = config.frame_rate
#         self.output_dir = config.output_dir
#         self.session_id = session_id
#         self.session_path = os.path.join(self.output_dir, session_id)
#         self.sticker_path = os.path.join(self.session_path, STICKER_FILENAME)
#         self.output_path = os.path.join(self.session_path, OUTPUT_VIDEO_FILENAME)

# class AudioMergerConfig:
#     def __init__(self, config: ConfigEntity, session_id: str):
#         self.output_dir = config.output_dir
#         self.session_id = session_id
#         self.temp_audio_extension=config.temp_audio_extension
#         self.session_path = os.path.join(self.output_dir, session_id)
#         self.final_output_path = os.path.join(self.session_path, FINAL_OUTPUT_FILENAME)



