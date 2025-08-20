import cv2
import sys
import os
from src.constants import *
from src.exceptions import CustomException
from src.logger import logging

async def save_uploaded_file(upload_file, path: str) -> None:
    """
    Save uploaded file to specified path.
    
    Args:
        upload_file: FastAPI UploadFile object
        path (str): Destination file path
        
    Raises:
        CustomException: If file saving fails
    """
    try:
        logging.info(f"Saving uploaded file to: {path}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "wb") as f:
            content = await upload_file.read()
            f.write(content)
            
        logging.info(f"File saved successfully: {path}")
        
    except Exception as e:
        logging.error(f"Error saving file to {path}: {e}")
        raise CustomException(e, sys)

def save_preview(crop, session_path: str, cid: int) -> str:
    """
    Save face crop preview image.
    
    Args:
        crop: Face crop image array
        session_path (str): Session directory path
        cid (int): Cluster ID
        
    Returns:
        str: Path to saved preview image
        
    Raises:
        CustomException: If preview saving fails
    """
    try:
        logging.info(f"Saving preview for cluster {cid}")
        
        # Ensure session directory exists
        os.makedirs(session_path, exist_ok=True)
        
        preview_path = os.path.join(
            session_path, 
            f"{PREVIEW_FILENAME_PREFIX}{cid}{PREVIEW_EXTENSION}"
        )
        
        cv2.imwrite(preview_path, crop)
        logging.info(f"Preview saved: {preview_path}")
        
        return preview_path
        
    except Exception as e:
        logging.error(f"Error saving preview for cluster {cid}: {e}")
        raise CustomException(e, sys)


