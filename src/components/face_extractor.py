
import cv2
import numpy as np
import sys
from src.entity.artifacts import FaceExtractorArtifact
from src.entity.config_entity import FaceExtractorConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException
from src.constants import *
from insightface.app import FaceAnalysis

class FaceExtractor:
    def __init__(self, config=FaceExtractorConfig):
        self.config=config
        self.face_app=FaceAnalysis(
            name=self.config.face_model_name,
            providers=self.config.face_model_providers
        )
        
        #self.config=FaceExtractorConfig(config=ConfigEntity(), session_id=session_id)

        #self.face_app = FaceAnalysis(name=FACE_MODEL_NAME, providers=FACE_MODEL_PROVIDERS)
        self.face_app.prepare(ctx_id=0)
    
        logging.info("FaceExtractor initialized")

    def extract(self, video_path):
        try:
            cap = cv2.VideoCapture(video_path)
            all_faces = []
            frame_idx = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                faces = self.face_app.get(frame)
                for face in faces:
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    face_crop = frame[y1:y2, x1:x2]
                    if face_crop.size > 0:
                        emb = face.embedding / np.linalg.norm(face.embedding)
                        all_faces.append({
                            "frame": frame_idx,
                            "embedding": emb,
                            "crop": face_crop,
                            "bbox": (x1, y1, x2, y2)
                        })
                frame_idx += 1

            cap.release()
            logging.info("Faces extracted successfully")
            return FaceExtractorArtifact(all_faces=all_faces)
        except Exception as e:
            logging.error(f"Error in face extraction: {str(e)}")
            raise CustomException(e, sys)



