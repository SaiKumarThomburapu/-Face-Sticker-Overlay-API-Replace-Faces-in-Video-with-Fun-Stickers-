import cv2
import sys
from src.entity.artifacts import StickerOverlayArtifact
from src.entity.config_entity import StickerOverlayConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

class StickerOverlay:
    def __init__(self, session_id: str):
        try:
            self.sticker_overlay_config = StickerOverlayConfig(config=ConfigEntity(), session_id=session_id)
        except Exception as e:
            raise CustomException(e, sys)
        logging.info("StickerOverlay initialized")
    
    def overlay(self, frame, bbox, sticker_img) -> StickerOverlayArtifact:
        try:
            x1, y1, x2, y2 = bbox
            h, w = frame.shape[:2]
            
            # Ensure bounds are within frame
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            
            face_w = x2 - x1
            face_h = y2 - y1
            
            if face_w <= 0 or face_h <= 0:
                logging.warning("Invalid face dimensions, skipping overlay")
                return StickerOverlayArtifact(frame=frame)
            
            sticker_resized = cv2.resize(sticker_img, (face_w, face_h))
            
            # Handle alpha channel if present
            if sticker_resized.shape[2] == 4:
                alpha_s = sticker_resized[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (
                        alpha_s * sticker_resized[:, :, c] +
                        alpha_l * frame[y1:y2, x1:x2, c]
                    )
            else:
                frame[y1:y2, x1:x2] = sticker_resized[:, :, :3]
            
            logging.info("Sticker overlaid successfully")
            return StickerOverlayArtifact(frame=frame)
            
        except Exception as e:
            logging.error(f"Error in sticker overlay: {str(e)}")
            raise CustomException(e, sys)





# import cv2
# import sys
# from src.entity.artifacts import StickerOverlayArtifact
# from src.entity.config import StickerOverlayConfig, ConfigEntity
# from src.logger import logging
# from src.exceptions import CustomException

# class StickerOverlay:
#     def __init__(self, session_id:str):
#         self.config =StickerOverlayConfig(config=ConfigEntity(), session_id= session_id)
#         logging.info("StickerOverlay initialized")

#     def overlay(self, frame, bbox, sticker_img):
#         try:
#             x1, y1, x2, y2 = bbox
#             h, w = frame.shape[:2]

#             x1 = max(0, x1)
#             y1 = max(0, y1)
#             x2 = min(w, x2)
#             y2 = min(h, y2)

#             face_w = x2 - x1
#             face_h = y2 - y1

#             if face_w <= 0 or face_h <= 0:
#                 return frame

#             sticker_resized = cv2.resize(sticker_img, (face_w, face_h))

#             if sticker_resized.shape[2] == 4:
#                 alpha_s = sticker_resized[:, :, 3] / 255.0
#                 alpha_l = 1.0 - alpha_s

#                 for c in range(3):
#                     frame[y1:y2, x1:x2, c] = (
#                         alpha_s * sticker_resized[:, :, c] +
#                         alpha_l * frame[y1:y2, x1:x2, c]
#                     )
#             else:
#                 frame[y1:y2, x1:x2] = sticker_resized[:, :, :3]

#             logging.info("Sticker overlaid successfully")
#             return StickerOverlayArtifact(frame=frame)
#         except Exception as e:
#             logging.error(f"Error in sticker overlay: {str(e)}")
#             raise CustomException(e, sys)



