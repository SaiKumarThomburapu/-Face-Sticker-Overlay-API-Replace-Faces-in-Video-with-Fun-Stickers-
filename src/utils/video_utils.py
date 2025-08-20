# import cv2
# import sys
# import os
# from src.constants import *
# from src.exceptions import CustomException
# from src.logger import logging

# def create_frame_map(selected_clusters, clusters):
#     """
#     Create mapping of frame indices to face data for selected clusters.
    
#     Args:
#         selected_clusters: List of selected cluster IDs
#         clusters: Dictionary of clustered face data
        
#     Returns:
#         dict: Frame index to face data mapping
        
#     Raises:
#         CustomException: If frame mapping fails
#     """
#     try:
#         logging.info(f"Creating frame map for clusters: {selected_clusters}")
        
#         frame_map = {}
#         for cid in selected_clusters:
#             cluster_faces = clusters.get(cid, [])
#             for face_data in cluster_faces:
#                 frame_idx = face_data["frame"]
#                 if frame_idx not in frame_map:
#                     frame_map[frame_idx] = []
#                 frame_map[frame_idx].append(face_data)
                
#         logging.info(f"Frame map created with {len(frame_map)} frames")
#         return frame_map
        
#     except Exception as e:
#         logging.error(f"Error creating frame map: {e}")
#         raise CustomException(e, sys)

# def process_video_frames(video_path: str, frame_map: dict, sticker_img, sticker_overlay):
#     """
#     Process video frames and apply sticker overlays.
    
#     Args:
#         video_path (str): Path to input video
#         frame_map (dict): Frame to face data mapping
#         sticker_img: Sticker image array
#         sticker_overlay: StickerOverlay component instance
        
#     Returns:
#         list: Processed video frames
        
#     Raises:
#         CustomException: If video processing fails
#     """
#     try:
#         logging.info(f"Processing video frames from: {video_path}")
        
#         cap = cv2.VideoCapture(video_path)
#         frames = []
#         frame_idx = 0
        
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
                
#             # Apply stickers if faces detected in this frame
#             if frame_idx in frame_map:
#                 for face_data in frame_map[frame_idx]:
#                     overlay_artifact = sticker_overlay.overlay(frame, face_data["bbox"], sticker_img)
#                     frame = overlay_artifact.frame
                    
#             frames.append(frame)
#             frame_idx += 1
            
#         cap.release()
#         logging.info(f"Processed {len(frames)} video frames")
        
#         return frames
        
#     except Exception as e:
#         logging.error(f"Error processing video frames: {e}")
#         raise CustomException(e, sys)

# def write_video(frames: list, output_path: str, frame_rate: int, size: tuple) -> None:
#     """
#     Write processed frames to output video file.
    
#     Args:
#         frames (list): List of processed frame arrays
#         output_path (str): Output video file path
#         frame_rate (int): Video frame rate
#         size (tuple): Video frame size (width, height)
        
#     Raises:
#         CustomException: If video writing fails
#     """
#     try:
#         logging.info(f"Writing video to: {output_path}")
        
#         # Ensure output directory exists
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
#         # Create video writer
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_path, fourcc, frame_rate, size)
        
#         # Write frames
#         for frame in frames:
#             out.write(frame)
            
#         out.release()
#         logging.info(f"Video written successfully: {output_path}")
        
#     except Exception as e:
#         logging.error(f"Error writing video to {output_path}: {e}")
#         raise CustomException(e, sys)





import cv2
from src.constants import *

def create_frame_map(selected, clusters):
    frame_map = {}
    for cid in selected:
        for f in clusters.get(cid, []):
            frame_map.setdefault(f["frame"], []).append(f)
    return frame_map

def process_video_frames(video_path, frame_map, sticker_img, sticker_overlay):
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx in frame_map:
            for f in frame_map[idx]:
                frame = sticker_overlay.overlay(frame, f["bbox"], sticker_img)
        frames.append(frame)
        idx += 1
    cap.release()
    return frames

def write_video(frames, output_path, frame_rate, size):
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)
    for f in frames:
        out.write(f)
    out.release()

