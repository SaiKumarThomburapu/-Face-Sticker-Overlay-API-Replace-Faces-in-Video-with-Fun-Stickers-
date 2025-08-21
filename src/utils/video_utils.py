import cv2
from src.constants import *
from src.components.sticker_overlay import StickerOverlay
from src.logger import logging
from src.exceptions import CustomException
import sys

def create_frame_map(selected, clusters):
    """Create mapping of frame index to face data"""
    frame_map = {}
    for cid in selected:
        for f in clusters.get(cid, []):
            frame_map.setdefault(f["frame"], []).append(f)
    return frame_map

def process_video_frames(video_path, frame_map, sticker_img, sticker_overlay: StickerOverlay):
    """Process video frames and apply sticker overlays"""
    try:
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise CustomException(f"Could not open video: {video_path}", sys)
        
        frames = []
        idx = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # SIMPLIFIED: Match working code pattern exactly
            if idx in frame_map:
                logging.info(f"Processing frame {idx} with {len(frame_map[idx])} faces")
                for f in frame_map[idx]:
                    frame= sticker_overlay.overlay(frame, f["bbox"], sticker_img)
                    #frame = artifact.frame  # Direct assignment like working code
            
            frames.append(frame)
            idx += 1
            
        cap.release()
        logging.info(f"Processed {len(frames)} frames total")
        return frames
        
    except Exception as e:
        if 'cap' in locals():
            cap.release()
        logging.error(f"Error processing video frames: {str(e)}")
        raise CustomException(e, sys)

def write_video(frames, output_path, frame_rate, size):
    """Write processed frames to output video"""
    try:
        if not frames:
            raise CustomException("No frames to write", sys)
            
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)
        
        if not out.isOpened():
            raise CustomException(f"Could not create video writer for: {output_path}", sys)
        
        for i, f in enumerate(frames):
            if f is None:
                logging.warning(f"Skipping None frame at index {i}")
                continue
            out.write(f)
            
        out.release()
        logging.info(f"Video written successfully: {output_path}")
        
    except Exception as e:
        if 'out' in locals():
            out.release()
        logging.error(f"Error writing video: {str(e)}")
        raise CustomException(e, sys)

