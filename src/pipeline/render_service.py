import cv2
import sys
import os
from src.utils.video_utils import create_frame_map, process_video_frames, write_video
from src.components.audio_merger import AudioMerger
from src.components.sticker_overlay import StickerOverlay
from src.entity.config_entity import ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

def render_service(session_id, cluster_ids, session_data):
    try:
        if session_id not in session_data:
            raise CustomException("Session not found", sys)

        base_config = ConfigEntity()
        data = session_data[session_id]
        video_path = data["video_path"]
        sticker_img = cv2.imread(data["sticker_path"], cv2.IMREAD_UNCHANGED)
        clusters = data["clusters"]

        # CRITICAL: Add sticker validation like working code
        if sticker_img is None:
            raise CustomException("Sticker image failed to load", sys)

        # parse cluster ids
        selected = [int(cid) for cid in cluster_ids.split(",") if cid.strip().isdigit()]

        frame_map = create_frame_map(selected, clusters)

        # Sticker overlay (uses your standard init)
        sticker_overlay = StickerOverlay()
        frames = process_video_frames(video_path, frame_map, sticker_img, sticker_overlay)

        # Ensure output folder exists
        output_dir = os.path.join(base_config.output_dir, session_id)
        os.makedirs(output_dir, exist_ok=True)

        # Output video path (video without audio yet)
        output_path = os.path.join(output_dir, base_config.output_video_filename)

        # Write video frames
        h, w = frames[0].shape[:2]
        write_video(frames, output_path, base_config.frame_rate, (w, h))

        # Audio merging (uses your standard init)
        audio_merger = AudioMerger()
        artifact = audio_merger.merge(video_path, output_path)

        logging.info(f"Rendered session {session_id}")
        return artifact.final_output_path

    except Exception as e:
        raise CustomException(e, sys)




