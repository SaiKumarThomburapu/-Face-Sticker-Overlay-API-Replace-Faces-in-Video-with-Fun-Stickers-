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
        self.config = AudioMergerConfig(config=ConfigEntity()) 
        logging.info("AudioMerger initialized")

    def merge(self, original_video, video_no_audio):
        session_dir = os.path.dirname(video_no_audio)
        final_output_path = os.path.join(session_dir, self.config.final_output_filename)
        try:
            temp_audio = os.path.join(session_dir, f"temp{self.config.temp_audio_extension}")

            # check if input video has audio
            try:
                probe = ffmpeg.probe(original_video)
                has_audio = any(stream.get("codec_type") == "audio" for stream in probe.get("streams", []))
            except Exception as probe_err:
                logging.warning(f"ffmpeg probe failed: {probe_err}. Will attempt to merge but fallback may be used.")
                has_audio = False

            if not has_audio:
                # no audio: just rename
                if os.path.exists(video_no_audio):
                    os.replace(video_no_audio, final_output_path)
                else:
                    raise CustomException(f"Video without audio not found: {video_no_audio}", sys)
                return AudioMergerArtifact(final_output_path=final_output_path)

            # extract audio
            extract_cmd = [
                "ffmpeg", "-y", "-i", original_video, "-vn", "-acodec", "copy", temp_audio
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

            # merge audio + video
            merge_cmd = [
                "ffmpeg", "-y", "-i", video_no_audio, "-i", temp_audio,
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", final_output_path
            ]
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)

            if os.path.exists(temp_audio):
                try:
                    os.remove(temp_audio)
                except Exception:
                    pass

            logging.info(f"Audio merged successfully into {final_output_path}")
            return AudioMergerArtifact(final_output_path=final_output_path)

        except Exception as e:
            logging.error(f"Error in audio merging: {str(e)}")
            # fallback: try rename if possible
            try:
                if os.path.exists(video_no_audio):
                    os.replace(video_no_audio, final_output_path)
                    logging.info("Fallback: moved video_no_audio to final output")
                    return AudioMergerArtifact(final_output_path=final_output_path)
            except Exception as ren_err:
                logging.error(f"Fallback rename failed: {ren_err}")
            raise CustomException(e, sys)




