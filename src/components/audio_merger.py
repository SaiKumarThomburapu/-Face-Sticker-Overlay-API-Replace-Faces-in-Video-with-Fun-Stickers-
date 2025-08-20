import os
import subprocess
import ffmpeg
import sys
from src.entity.artifacts import AudioMergerArtifact
from src.entity.config_entity import AudioMergerConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

class AudioMerger:
    def __init__(self, session_id: str):
        try:
            self.config = AudioMergerConfig(config=ConfigEntity(), session_id=session_id)
            self.final_output_path = os.path.join(self.config.output_dir, self.config.session_id, self.config.final_output_filename)
            logging.info("AudioMerger initialized")
        except Exception as e:
            raise CustomException(e, sys)

    def merge(self, original_video, video_no_audio):
        try:
            probe = ffmpeg.probe(original_video)
            has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])

            if not has_audio:
                os.rename(video_no_audio, self.final_output_path)
                return AudioMergerArtifact(final_output_path=self.final_output_path)

            temp_audio = f"{self.final_output_path}{self.config.temp_audio_extension}"
            extract_cmd = [
                "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            merge_cmd = [
                "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", self.final_output_path
            ]
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(temp_audio)
            logging.info("Audio merged successfully")
            return AudioMergerArtifact(final_output_path=self.final_output_path)
        except Exception as e:
            logging.error(f"Error in audio merging: {str(e)}")
            os.rename(video_no_audio, self.final_output_path)
            raise CustomException(e, sys)



# import os
# import subprocess
# import ffmpeg
# import sys
# from src.entity.artifacts import AudioMergerArtifact
# from src.entity.config_entity import AudioMergerConfig, ConfigEntity
# from src.logger import logging
# from src.exceptions import CustomException
# from src.constants import *

# class AudioMerger:
#     def __init__(self):
#         self.audio_merger_config=AudioMergerConfig(config=ConfigEntity())
#         #self.final_output_path = config.final_output_path
#         logging.info("AudioMerger initialized")

#     def merge(self, original_video, video_no_audio):
#         try:
#             probe = ffmpeg.probe(original_video)
#             has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])

#             if not has_audio:
#                 os.rename(video_no_audio, self.audio_merger_config.final_output_path)
#                 return

#             temp_audio = f"{self.audio_merger_config.final_output_path}{self.audio_merger_config.temp_audio_extension}"
#             extract_cmd = [
#                 "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
#             ]
#             subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#             merge_cmd = [
#                 "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
#                 "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", self.audio_merger_config.final_output_path
#             ]
#             subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#             os.remove(temp_audio)
#             logging.info("Audio merged successfully")
#             return AudioMergerArtifact(final_output_path=self.audio_merger_config.final_output_path)
#         except Exception as e:
#             logging.error(f"Error in audio merging: {str(e)}")
#             os.rename(video_no_audio, self.audio_merger_config.final_output_path)
#             raise CustomException(e, sys)




