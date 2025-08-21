import cv2
import sys
import numpy as np
from src.entity.config_entity import StickerOverlayConfig, ConfigEntity
from src.logger import logging
from src.exceptions import CustomException

class StickerOverlay:
    def __init__(self):
        self.config = StickerOverlayConfig(config=ConfigEntity()) 
        logging.info("StickerOverlay initialized")
    
    def overlay(self, frame, bbox, sticker_img):
        try:
            if frame is None or sticker_img is None:
                logging.warning("Frame or sticker is None, skipping overlay")
                return frame

            x1, y1, x2, y2 = bbox
            h, w = frame.shape[:2]
            
            # Bounds clamp
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)
            
            face_w = x2 - x1
            face_h = y2 - y1
            
            if face_w <= 0 or face_h <= 0:
                logging.warning("Invalid face dimensions, skipping overlay")
                return frame
            
            # make sure sticker is numpy array and correct dtype
            sticker = np.array(sticker_img)
            if sticker.dtype != np.uint8:
                sticker = sticker.astype(np.uint8)

            # ensure sticker has 3 or 4 channels
            if sticker.ndim == 2:
                sticker = cv2.cvtColor(sticker, cv2.COLOR_GRAY2BGRA)

            if sticker.shape[2] == 3:
                # add alpha channel (opaque) so we can unify the blending flow
                alpha_channel = np.ones((sticker.shape[0], sticker.shape[1], 1), dtype=np.uint8) * 255
                sticker = np.concatenate([sticker, alpha_channel], axis=2)

            sticker_resized = cv2.resize(sticker, (face_w, face_h), interpolation=cv2.INTER_AREA)

            # blending with alpha
            alpha_s = sticker_resized[:, :, 3].astype(float) / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(3):
                frame[y1:y2, x1:x2, c] = (
                    alpha_s * sticker_resized[:, :, c] +
                    alpha_l * frame[y1:y2, x1:x2, c]
                ).astype(np.uint8)
            
            logging.debug(f"Sticker overlaid at bbox {bbox}")
            return frame

        except Exception as e:
            logging.error(f"Error in sticker overlay: {str(e)}")
            raise CustomException(e, sys)




