# import cv2
# import sys
# import os
# from src.utils.video_utils import create_frame_map, process_video_frames, write_video
# from src.components.audio_merger import AudioMerger
# from src.components.sticker_overlay import StickerOverlay
# from src.entity.config import ConfigEntity
# from src.logger import logging
# from src.exceptions import CustomException
# from src.constants import *

# def render_service(session_id: str, cluster_ids: str, session_data: dict) -> str:
#     """
#     Render video with stickers based on selected clusters.
    
#     Args:
#         session_id (str): Session identifier
#         cluster_ids (str): Comma-separated cluster IDs
#         session_data (dict): Session data storage
        
#     Returns:
#         str: Path to rendered video with audio
        
#     Raises:
#         CustomException: If rendering fails
#     """
#     try:
#         logging.info(f"Starting render service for session: {session_id}")
        
#         if session_id not in session_data:
#             raise CustomException("Session not found", sys)
        
#         data = session_data[session_id]
#         video_path = data["video_path"]
#         sticker_img = cv2.imread(data["sticker_path"], cv2.IMREAD_UNCHANGED)
#         clusters = data["clusters"]
        
#         selected = [int(cid) for cid in cluster_ids.split(",") if cid.strip().isdigit()]
#         logging.info(f"Selected clusters: {selected}")
        
#         frame_map = create_frame_map(selected, clusters)
        
#         # Sticker overlay with session_id
#         sticker_overlay = StickerOverlay(session_id=session_id)
#         frames = process_video_frames(video_path, frame_map, sticker_img, sticker_overlay)
        
#         h, w = frames[0].shape[:2]
#         session_path = os.path.join(OUTPUT_DIR, session_id)
#         output_path = os.path.join(session_path, OUTPUT_VIDEO_FILENAME)
        
#         write_video(frames, output_path, FRAME_RATE, (w, h))
        
#         # Audio merging with session_id
#         audio_merger = AudioMerger(session_id=session_id)
#         artifact = audio_merger.merge(video_path, output_path)
        
#         logging.info(f"Render service completed for session: {session_id}")
#         return artifact.final_output_path
        
#     except Exception as e:
#         logging.error(f"Error in render service: {e}")
#         raise CustomException(e, sys)





import cv2
import sys
import os
from src.utils.video_utils import create_frame_map, process_video_frames, write_video
from src.components.audio_merger import AudioMerger
from src.components.sticker_overlay import StickerOverlay
from src.entity.config_entity import ConfigEntity, StickerOverlayConfig, AudioMergerConfig
from src.logger import logging
from src.exceptions import CustomException
from src.constants import *

def render_service(session_id, cluster_ids, session_data):
    try:
        if session_id not in session_data:
            raise CustomException("Session not found", sys)

        base_config = ConfigEntity()
        data = session_data[session_id]
        video_path = data["video_path"]
        sticker_img = cv2.imread(data["sticker_path"], cv2.IMREAD_UNCHANGED)
        clusters = data["clusters"]

        selected = [int(cid) for cid in cluster_ids.split(",") if cid.strip().isdigit()]

        frame_map = create_frame_map(selected, clusters)

        # Sticker overlay (using class)
        so_config = StickerOverlayConfig(base_config, session_id)
        sticker_overlay = StickerOverlay(so_config)
        frames = process_video_frames(video_path, frame_map, sticker_img, sticker_overlay)

        h, w = frames[0].shape[:2]
        output_path = os.path.join(OUTPUT_DIR, session_id, OUTPUT_VIDEO_FILENAME)
        write_video(frames, output_path, FRAME_RATE, (w, h))

        # Audio merging (using class)
        am_config = AudioMergerConfig(base_config, session_id)
        audio_merger = AudioMerger(am_config)
        audio_merger.merge(video_path, output_path)

        final_output_path = os.path.join(OUTPUT_DIR, session_id, FINAL_OUTPUT_FILENAME)
        logging.info(f"Rendered session {session_id}")
        return final_output_path
    except Exception as e:
        raise CustomException(e, sys)




