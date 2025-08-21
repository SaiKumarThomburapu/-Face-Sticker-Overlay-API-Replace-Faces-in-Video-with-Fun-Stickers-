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
            raise CustomException(f"Session not found: {session_id}", sys)

        base_config = ConfigEntity()
        data = session_data[session_id]

        # DEBUG / sanity: show what we have in session
        logging.info(f"Render service called for session: {session_id}")
        logging.info(f"Session keys: {list(data.keys())}")

        video_path = data.get("video_path")
        sticker_path = data.get("sticker_path")
        clusters = data.get("clusters", {})

        if not video_path or not os.path.exists(video_path):
            raise CustomException(f"Video path missing or doesn't exist: {video_path}", sys)
        if not sticker_path or not os.path.exists(sticker_path):
            raise CustomException(f"Sticker path missing or doesn't exist: {sticker_path}", sys)

        sticker_img = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
        if sticker_img is None:
            raise CustomException(f"Sticker image failed to load (cv2.imread returned None): {sticker_path}", sys)

        # parse cluster ids safely
        selected = [int(cid) for cid in str(cluster_ids).split(",") if cid.strip().isdigit()]

        frame_map = create_frame_map(selected, clusters)

        sticker_overlay = StickerOverlay()
        frames = process_video_frames(video_path, frame_map, sticker_img, sticker_overlay)

        if not frames:
            raise CustomException("No frames were produced after processing. Check video reading or frame_map.", sys)

        # Ensure output folder exists
        output_dir = os.path.join(base_config.output_dir, session_id)
        os.makedirs(output_dir, exist_ok=True)

        # Output video path (video without audio yet)
        output_path = os.path.join(output_dir, base_config.output_video_filename)

        # Write video frames
        h, w = frames[0].shape[:2]
        write_video(frames, output_path, base_config.frame_rate, (w, h))

        # Audio merging
        audio_merger = AudioMerger()
        artifact = audio_merger.merge(video_path, output_path)

        logging.info(f"Rendered session {session_id} -> {artifact.final_output_path}")
        return artifact.final_output_path

    except Exception as e:
        logging.error(f"Render service error: {str(e)}")
        # Re-wrap into CustomException if not already
        if isinstance(e, CustomException):
            raise
        raise CustomException(e, sys)




