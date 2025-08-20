# import uuid
# import os
# import sys
# from src.entity.config import ConfigEntity
# from src.components.face_extractor import FaceExtractor
# from src.components.clusterer import Clusterer
# from src.utils.io_utils import save_uploaded_file, save_preview
# from src.logger import logging
# from src.exceptions import CustomException
# from src.constants import *

# async def upload_service(video, sticker, session_data: dict) -> dict:
#     """
#     Process uploaded video and sticker files.
    
#     Args:
#         video: Uploaded video file
#         sticker: Uploaded sticker file  
#         session_data (dict): Session data storage
        
#     Returns:
#         dict: Session ID and cluster information
        
#     Raises:
#         CustomException: If upload processing fails
#     """
#     try:
#         logging.info("Starting upload service")
        
#         session_id = uuid.uuid4().hex
#         session_path = os.path.join(OUTPUT_DIR, session_id)
#         os.makedirs(session_path, exist_ok=True)
        
#         # Save files using constants
#         video_path = os.path.join(session_path, INPUT_VIDEO_FILENAME)
#         sticker_path = os.path.join(session_path, STICKER_FILENAME)
        
#         await save_uploaded_file(video, video_path)
#         await save_uploaded_file(sticker, sticker_path)
        
#         logging.info(f"Files saved for session: {session_id}")
        
#         # Face extraction with session_id
#         face_extractor = FaceExtractor(session_id=session_id)
#         face_artifact = face_extractor.extract(video_path)
        
#         # Clustering with session_id
#         clusterer = Clusterer(session_id=session_id)
#         cluster_artifact = clusterer.cluster(face_artifact.all_faces)
        
#         # Clean clusters (convert keys to native int)
#         cleaned_clusters = {}
#         for cid, face_list in cluster_artifact.clustered.items():
#             native_cid = int(cid)
#             cleaned_clusters[native_cid] = face_list
        
#         session_data[session_id] = {
#             "video_path": video_path,
#             "sticker_path": sticker_path,
#             "clusters": cleaned_clusters
#         }
        
#         # Generate previews
#         previews = {}
#         for cid, face_list in cleaned_clusters.items():
#             preview_path = save_preview(face_list[0]["crop"], session_path, cid)
#             previews[cid] = preview_path
        
#         cluster_ids = [int(k) for k in previews.keys()]
#         logging.info(f"Upload service completed. Session: {session_id}, Clusters: {cluster_ids}")
        
#         return {
#             "session_id": session_id,
#             "clusters": cluster_ids
#         }
        
#     except Exception as e:
#         logging.error(f"Error in upload service: {e}")
#         raise CustomException(e, sys)





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
        os.makedirs(os.path.join(OUTPUT_DIR, session_id), exist_ok=True)

        # Save files (using constants)
        video_path = os.path.join(OUTPUT_DIR, session_id, INPUT_VIDEO_FILENAME)
        sticker_path = os.path.join(OUTPUT_DIR, session_id, STICKER_FILENAME)
        await save_uploaded_file(video, video_path)
        await save_uploaded_file(sticker, sticker_path)

        # Face extraction
        fe_config = FaceExtractorConfig(base_config, session_id)
        face_extractor = FaceExtractor(fe_config)
        #face_extractor= FaceExtractor(session_id)
        faces = face_extractor.extract(video_path)

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
            preview_path = save_preview(face_list[0]["crop"], os.path.join(OUTPUT_DIR, session_id), cid)
            previews[cid] = preview_path

        cluster_ids = [int(k) for k in previews.keys()]
        logging.info(f"Uploaded session {session_id} with clusters {cluster_ids}")
        return {
            "session_id": session_id,
            "clusters": cluster_ids
        }
    except Exception as e:
        raise CustomException(e, sys)




