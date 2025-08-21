import uuid
import os
import sys
from pathlib import Path

from src.entity.config_entity import ConfigEntity
from src.components.face_extractor import FaceExtractor
from src.components.clusterer import Clusterer
from src.utils.io_utils import save_uploaded_file, save_preview
from src.logger import logging
from src.exceptions import CustomException
from src.constants import MAX_VIDEO_SIZE_MB, ALLOWED_STICKER_EXTENSIONS


async def upload_service(video, sticker, session_data):
    try:
        # --- Base Config (global constants) ---
        base_config = ConfigEntity()

        # --- Create session-specific directory ---
        session_id = uuid.uuid4().hex
        session_dir = os.path.join(base_config.output_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)

        # --- Save uploaded video + sticker into this session dir ---
        video_path = os.path.join(session_dir, base_config.input_video_filename)
        # Preserve sticker extension based on original filename
        sticker_ext = Path(sticker.filename).suffix.lower()  # e.g., ".png"
        sticker_path = os.path.join(session_dir, f"{Path(base_config.sticker_filename).stem}{sticker_ext}")

        await save_uploaded_file(video, video_path)
        await save_uploaded_file(sticker, sticker_path)

        # ================= VALIDATIONS =================
        # 1) Validate video size
        try:
            size_mb = os.path.getsize(video_path) / (1024 * 1024)
        except Exception:
            size_mb = -1  # Unexpected issue reading size (fail safe below)

        if MAX_VIDEO_SIZE_MB is not None and size_mb > MAX_VIDEO_SIZE_MB:
            logging.error(f"Video size {size_mb:.2f}MB exceeds limit {MAX_VIDEO_SIZE_MB}MB")
            # Cleanup and return an explicit error
            try:
                if os.path.exists(video_path): os.remove(video_path)
                if os.path.exists(sticker_path): os.remove(sticker_path)
            except Exception:
                pass
            return {
                "error": f"Video size {size_mb:.2f}MB exceeds limit {MAX_VIDEO_SIZE_MB}MB"
            }

        # 2) Validate sticker extension
        ext = sticker_ext.lstrip(".")  # "png", "jpg", etc.
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
        # ================================================

        # --- Face Extraction (pass session-specific video path) ---
        face_extractor = FaceExtractor()
        faces_artifact = face_extractor.extract(video_path)
        faces = faces_artifact.all_faces

        # --- Clustering (pass faces directly) ---
        clusterer = Clusterer()
        cluster_artifact = clusterer.cluster(faces)
        clusters = cluster_artifact.clustered

        # --- Clean clusters into int keys ---
        cleaned_clusters = {int(cid): face_list for cid, face_list in clusters.items()}

        # --- Store session data in memory ---
        session_data[session_id] = {
            "video_path": video_path,
            "sticker_path": sticker_path,
            "clusters": cleaned_clusters
        }

        # --- Generate previews for each cluster ---
        previews = {}
        for cid, face_list in cleaned_clusters.items():
            if not face_list:
                continue
            preview_path = save_preview(
                face_list[0]["crop"],  # first face crop in cluster
                session_dir,
                cid
            )
            previews[cid] = preview_path

        # --- Prepare response ---
        cluster_ids = list(previews.keys())
        logging.info(f"Uploaded session {session_id} with clusters {cluster_ids}")

        return {
            "session_id": session_id,
            "clusters": cluster_ids
        }

    except Exception as e:
        raise CustomException(e, sys)




