# import numpy as np
# from sklearn.cluster import DBSCAN
# import sys
# from src.entity.artifacts import ClustererArtifact
# from Project.src.entity.config_entity import ClustererConfig, ConfigEntity
# from src.logger import logging
# from src.constants import *
# from src.exceptions import CustomException

# class Clusterer:
#     def __init__(self, session_id: str):
#         try:
#             self.clusterer_config = ClustererConfig(config=ConfigEntity(), session_id=session_id)
#         except Exception as e:
#             raise CustomException(e, sys)
#         logging.info("Clusterer initialized")
    
#     def cluster(self, faces) -> ClustererArtifact:
#         try:
#             logging.info(f"Starting clustering for {len(faces)} faces")
            
#             embeddings = np.array([f["embedding"] for f in faces])
#             db = DBSCAN(
#                 eps=self.clusterer_config.eps, 
#                 min_samples=self.clusterer_config.min_samples, 
#                 metric=self.clusterer_config.metric
#             ).fit(embeddings)
            
#             labels = db.labels_
#             clustered = {}
#             for i, lbl in enumerate(labels):
#                 if lbl == -1:  # Skip noise points
#                     continue
#                 clustered.setdefault(lbl, []).append(faces[i])
            
#             logging.info(f"Clustering completed successfully. Found {len(clustered)} clusters")
#             return ClustererArtifact(clustered=clustered)
            
#         except Exception as e:
#             logging.error(f"Error in clustering: {str(e)}")
#             raise CustomException(e, sys)





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
        self.clusterer=ClustererConfig(config=ConfigEntity())
        # self.config = config
        # self.eps = config.eps
        # self.min_samples = config.min_samples
        logging.info("Clusterer initialized")

    def cluster(self, faces):
        try:
            embeddings = np.array([f["embedding"] for f in faces])
            db = DBSCAN(eps=self.clusterer.eps, min_samples=self.clusterer.min_samples, metric=self.clusterer.metric).fit(embeddings)
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



