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
        self.face_model_name=FACE_MODEL_NAME
        self.face_model_providers=FACE_MODEL_PROVIDERS

class FaceExtractorConfig:
    def __init__(self, config: ConfigEntity):
        self.output_dir = config.output_dir
        self.input_video_filename = config.input_video_filename
        self.face_model_name=config.face_model_name
        self.face_model_providers=config.face_model_providers

class ClustererConfig:
    def __init__(self, config: ConfigEntity):
        self.eps = config.eps
        self.min_samples = config.min_samples
        self.metric = config.metric
        self.output_dir = config.output_dir
        

class StickerOverlayConfig:
    def __init__(self, config: ConfigEntity):
        self.frame_rate = config.frame_rate
        self.output_dir = config.output_dir
        self.sticker_filename = config.sticker_filename
        self.output_video_filename = config.output_video_filename

class AudioMergerConfig:
    def __init__(self, config: ConfigEntity):
        self.output_dir = config.output_dir
        self.temp_audio_extension = config.temp_audio_extension
        self.final_output_filename = config.final_output_filename

 
