# import os
# import subprocess
# import ffmpeg
# import sys
# from src.entity.artifacts import AudioMergerArtifact
# from Project.src.entity.config_entity import AudioMergerConfig, ConfigEntity
# from src.logger import logging
# from src.exceptions import CustomException
# from src.constants import *

# class AudioMerger:
#     def __init__(self, session_id: str):
#         try:
#             self.audio_merger_config = AudioMergerConfig(config=ConfigEntity(), session_id=session_id)
#         except Exception as e:
#             raise CustomException(e, sys)
#         logging.info("AudioMerger initialized")
    
#     def merge(self, original_video: str, video_no_audio: str) -> AudioMergerArtifact:
#         try:
#             # Create session-specific paths using config
#             session_path = os.path.join(self.audio_merger_config.output_dir, self.audio_merger_config.session_id)
#             final_output_path = os.path.join(session_path, self.audio_merger_config.final_output_filename)
            
#             probe = ffmpeg.probe(original_video)
#             has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
            
#             if not has_audio:
#                 os.rename(video_no_audio, final_output_path)
#                 logging.info("No audio found, renamed video file")
#                 return AudioMergerArtifact(final_output_path=final_output_path)
            
#             temp_audio = f"{final_output_path}{self.audio_merger_config.temp_audio_extension}"
            
#             extract_cmd = [
#                 "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
#             ]
#             subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
#             merge_cmd = [
#                 "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
#                 "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output_path
#             ]
#             subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
#             if os.path.exists(temp_audio):
#                 os.remove(temp_audio)
                
#             logging.info("Audio merged successfully")
#             return AudioMergerArtifact(final_output_path=final_output_path)
            
#         except Exception as e:
#             logging.error(f"Error in audio merging: {str(e)}")
#             raise CustomException(e, sys)




import os
import subprocess
import ffmpeg
import sys
from src.entity.artifacts import AudioMergerArtifact
from src.entity.config_entity import AudioMergerConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException
from src.constants import *

class AudioMerger:
    def __init__(self):
        self.audio_merger_config=AudioMergerConfig(config=ConfigEntity())
        #self.final_output_path = config.final_output_path
        logging.info("AudioMerger initialized")

    def merge(self, original_video, video_no_audio):
        try:
            probe = ffmpeg.probe(original_video)
            has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])

            if not has_audio:
                os.rename(video_no_audio, self.audio_merger_config.final_output_path)
                return

            temp_audio = f"{self.audio_merger_config.final_output_path}{self.audio_merger_config.temp_audio_extension}"
            extract_cmd = [
                "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            merge_cmd = [
                "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", self.audio_merger_config.final_output_path
            ]
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(temp_audio)
            logging.info("Audio merged successfully")
            return AudioMergerArtifact(final_output_path=self.audio_merger_config.final_output_path)
        except Exception as e:
            logging.error(f"Error in audio merging: {str(e)}")
            os.rename(video_no_audio, self.audio_merger_config.final_output_path)
            raise CustomException(e, sys)




