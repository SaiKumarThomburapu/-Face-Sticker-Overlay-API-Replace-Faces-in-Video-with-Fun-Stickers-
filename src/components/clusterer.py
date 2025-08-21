
import numpy as np
from sklearn.cluster import DBSCAN
import sys
from src.entity.artifacts import ClustererArtifact
from src.entity.config_entity import ClustererConfig, ConfigEntity
from src.logger import logging
from src.constants import *
from src.exceptions import CustomException

class Clusterer:
    def __init__(self):
        self.config=ClustererConfig(config=ConfigEntity()) 
        logging.info("Clusterer initialized")

    def cluster(self, faces):
        try:
            embeddings = np.array([f["embedding"] for f in faces])
            db = DBSCAN(eps=self.config.eps, min_samples=self.config.min_samples, metric=self.config.metric).fit(embeddings)
            labels = db.labels_
            clustered = {}
            for i, lbl in enumerate(labels):
                if lbl == -1:
                    continue
                clustered.setdefault(lbl, []).append(faces[i])
            logging.info("Clustering completed successfully")
            return ClustererArtifact(clustered=clustered)
        except Exception as e:
            logging.error(f"Error in clustering: {str(e)}")
            raise CustomException(e, sys)



