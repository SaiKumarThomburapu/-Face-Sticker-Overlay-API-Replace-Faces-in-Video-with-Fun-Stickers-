import cv2
from src.constants import *

async def save_uploaded_file(upload_file, path):
    with open(path, "wb") as f:
        f.write(await upload_file.read())

def save_preview(crop, session_path, cid):
    preview_path = f"{session_path}/{PREVIEW_FILENAME_PREFIX}{cid}{PREVIEW_EXTENSION}"
    cv2.imwrite(preview_path, crop)
    return preview_path

