import os
import subprocess
import ffmpeg
import sys
from src.entity.artifacts import AudioMergerArtifact
from src.entity.config_entity import AudioMergerConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException


class AudioMerger:
    def __init__(self):
        self.config=AudioMergerConfig(config=ConfigEntity()) 
        logging.info("AudioMerger initialized")

    def merge(self, original_video, video_no_audio):
        # final_output_path = os.path.join(
        #     self.config.output_dir, session_id, self.config.final_output_filename
        #     )
        try:
            session_dir=os.path.dirname(video_no_audio)
            final_output_path=os.path.join(session_dir, self.config.final_output_filename)
            
            temp_audio = os.path.join(
                session_dir,
                f"temp{self.config.temp_audio_extension}"
            )

            # check if input video has audio
            probe = ffmpeg.probe(original_video)
            has_audio = any(stream["codec_type"] == "audio" for stream in probe["streams"])

            if not has_audio:
                os.rename(video_no_audio, final_output_path)
                return AudioMergerArtifact(final_output_path=final_output_path)

            # extract audio
            extract_cmd = [
                "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # merge audio + video
            merge_cmd = [
                "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output_path
            ]
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            os.remove(temp_audio)
            logging.info(f"Audio merged successfully into {final_output_path}")

            return AudioMergerArtifact(final_output_path=final_output_path)

        except Exception as e:
            logging.error(f"Error in audio merging: {str(e)}")
            # fallback: just rename video without audio
            os.rename(video_no_audio, final_output_path)
            raise CustomException(e, sys)




