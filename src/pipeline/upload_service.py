import uuid
import os
import sys
from src.entity.config_entity import ConfigEntity, FaceExtractorConfig, ClustererConfig
from src.components.face_extractor import FaceExtractor
from src.components.clusterer import Clusterer
from src.utils.io_utils import save_uploaded_file, save_preview
from src.logger import logging
from src.exceptions import CustomException
from src.constants import *

async def upload_service(video, sticker, session_data):
    try:
        base_config = ConfigEntity()
        session_id = uuid.uuid4().hex
        os.makedirs(os.path.join(base_config.output_dir, session_id), exist_ok=True)

        # Save files (using constants)
        video_path = os.path.join(base_config.output_dir, session_id, base_config.input_video_filename)
        sticker_path = os.path.join(base_config.output_dir, session_id, base_config.sticker_filename)
        await save_uploaded_file(video, video_path)
        await save_uploaded_file(sticker, sticker_path)

        # Face extraction
        fe_config = FaceExtractorConfig(base_config, session_id)
        face_extractor = FaceExtractor(fe_config)
        faces_artifact = face_extractor.extract(video_path)
        faces=faces_artifact.all_faces

        # Clustering
        cl_config = ClustererConfig(base_config, session_id)
        clusterer = Clusterer(cl_config)
        cluster_artifact=clusterer.cluster(faces)
        clusters = cluster_artifact.clustered

        # Clean clusters (as in original code)
        cleaned_clusters = {}
        for cid, face_list in clusters.items():
            native_cid = int(cid)
            cleaned_clusters[native_cid] = face_list

        session_data[session_id] = {
            "video_path": video_path,
            "sticker_path": sticker_path,
            "clusters": cleaned_clusters
        }

        # Generate previews
        previews = {}
        for cid, face_list in cleaned_clusters.items():
            preview_path = save_preview(face_list[0]["crop"], os.path.join(base_config.output_dir, session_id), cid)
            previews[cid] = preview_path

        cluster_ids = [int(k) for k in previews.keys()]
        logging.info(f"Uploaded session {session_id} with clusters {cluster_ids}")
        return {
            "session_id": session_id,
            "clusters": cluster_ids
        }
    except Exception as e:
        raise CustomException(e, sys)




