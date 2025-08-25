# pipeline/full_pipeline.py

import os
import sys
import uuid
from pathlib import Path
import cv2

from src.entity.config_entity import ConfigEntity
from src.components.face_extractor import FaceExtractor
from src.components.clusterer import Clusterer
from src.components.audio_merger import AudioMerger
from src.components.sticker_overlay import StickerOverlay
from src.utils.io_utils import save_uploaded_file, save_preview
from src.utils.video_utils import create_frame_map, process_video_frames, write_video
from src.logger import logging
from src.exceptions import CustomException
from src.constants import MAX_VIDEO_SIZE_MB, ALLOWED_STICKER_EXTENSIONS


# ===============================
# Upload Pipeline
# ===============================
async def upload_service(video, sticker, session_data):
    try:
        base_config = ConfigEntity()

        # Session-specific dir
        session_id = uuid.uuid4().hex
        session_dir = os.path.join(base_config.output_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)

        # Paths
        video_path = os.path.join(session_dir, base_config.input_video_filename)
        sticker_ext = Path(sticker.filename).suffix.lower()
        sticker_path = os.path.join(
            session_dir, f"{Path(base_config.sticker_filename).stem}{sticker_ext}"
        )

        await save_uploaded_file(video, video_path)
        await save_uploaded_file(sticker, sticker_path)

        # Validate video size
        try:
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
        except Exception:
            size_mb = -1

        if MAX_VIDEO_SIZE_MB is not None and size_mb > MAX_VIDEO_SIZE_MB:
            logging.error(f"Video size {size_mb:.2f}MB exceeds limit {MAX_VIDEO_SIZE_MB}MB")
            try:
                if os.path.exists(video_path): os.remove(video_path)
                if os.path.exists(sticker_path): os.remove(sticker_path)
            except Exception:
                pass
            return {"error": f"Video size {size_mb:.2f}MB exceeds limit {MAX_VIDEO_SIZE_MB}MB"}

        # Validate sticker extension
        ext = sticker_ext.lstrip(".")
        if ALLOWED_STICKER_EXTENSIONS and ext not in ALLOWED_STICKER_EXTENSIONS:
            logging.error(f"Sticker extension .{ext} not allowed. Allowed: {ALLOWED_STICKER_EXTENSIONS}")
            try:
                if os.path.exists(video_path): os.remove(video_path)
                if os.path.exists(sticker_path): os.remove(sticker_path)
            except Exception:
                pass
            return {
                "error": f"Sticker extension .{ext} not allowed. Allowed: {ALLOWED_STICKER_EXTENSIONS}"
            }

        # Face extraction
        face_extractor = FaceExtractor()
        faces_artifact = face_extractor.extract(video_path)
        faces = faces_artifact.all_faces

        # Clustering
        clusterer = Clusterer()
        cluster_artifact = clusterer.cluster(faces)
        clusters = cluster_artifact.clustered
        cleaned_clusters = {int(cid): face_list for cid, face_list in clusters.items()}

        # Store session data
        session_data[session_id] = {
            "video_path": video_path,
            "sticker_path": sticker_path,
            "clusters": cleaned_clusters
        }

        # Previews
        previews = {}
        for cid, face_list in cleaned_clusters.items():
            if not face_list:
                continue
            preview_path = save_preview(face_list[0]["crop"], session_dir, cid)
            previews[cid] = preview_path

        cluster_ids = list(previews.keys())
        logging.info(f"Uploaded session {session_id} with clusters {cluster_ids}")

        return {"session_id": session_id, "clusters": cluster_ids}

    except Exception as e:
        raise CustomException(e, sys)


# ===============================
# Render Pipeline
# ===============================
def render_service(session_id, cluster_ids, session_data):
    try:
        if session_id not in session_data:
            raise CustomException(f"Session not found: {session_id}", sys)

        base_config = ConfigEntity()
        data = session_data[session_id]

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
            raise CustomException(f"Sticker image failed to load: {sticker_path}", sys)

        # Parse cluster ids
        selected = [int(cid) for cid in str(cluster_ids).split(",") if cid.strip().isdigit()]
        frame_map = create_frame_map(selected, clusters)

        # Overlay
        sticker_overlay = StickerOverlay()
        frames = process_video_frames(video_path, frame_map, sticker_img, sticker_overlay)

        if not frames:
            raise CustomException("No frames were produced after processing.", sys)

        # Output paths
        output_dir = os.path.join(base_config.output_dir, session_id)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_config.output_video_filename)

        # Write video frames
        h, w = frames[0].shape[:2]
        write_video(frames, output_path, base_config.frame_rate, (w, h))

        # Merge audio
        audio_merger = AudioMerger()
        artifact = audio_merger.merge(video_path, output_path)

        logging.info(f"Rendered session {session_id} -> {artifact.final_output_path}")
        return artifact.final_output_path

    except Exception as e:
        logging.error(f"Render service error: {str(e)}")
        if isinstance(e, CustomException):
            raise
        raise CustomException(e, sys)




