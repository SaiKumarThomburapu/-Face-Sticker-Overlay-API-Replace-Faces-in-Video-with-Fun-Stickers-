import cv2
from src.constants import *
from src.components.sticker_overlay import StickerOverlay
from src.logger import logging
from src.exceptions import CustomException
import sys
import os
import numpy as np

def create_frame_map(selected, clusters):
    frame_map = {}
    for cid in selected:
        for f in clusters.get(cid, []):
            frame_map.setdefault(f["frame"], []).append(f)
    return frame_map

def process_video_frames(video_path, frame_map, sticker_img, sticker_overlay: StickerOverlay):
    try:
        if not os.path.exists(video_path):
            raise CustomException(f"Video path does not exist: {video_path}", sys)

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise CustomException(f"Could not open video: {video_path}", sys)

        frames = []
        idx = 0

        logging.info(f"Starting frame processing for {video_path}. Total frames with overlays: {len(frame_map)}")
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # defensive: ensure frame is valid np array
            if frame is None or not isinstance(frame, (np.ndarray,)):
                logging.warning(f"Invalid frame at index {idx}, skipping")
                idx += 1
                continue

            if idx in frame_map:
                logging.info(f"Processing frame {idx} with {len(frame_map[idx])} face(s)")
                for f in frame_map[idx]:
                    try:
                        frame = sticker_overlay.overlay(frame, f["bbox"], sticker_img)
                    except Exception as overlay_err:
                        logging.error(f"Overlay failed on frame {idx}, bbox={f.get('bbox')}: {overlay_err}")
                        # continue processing other faces/frames

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
    try:
        if not frames:
            raise CustomException("No frames to write", sys)

        # ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, frame_rate, size)

        if not out.isOpened():
            raise CustomException(f"Could not create video writer for: {output_path}", sys)

        for i, f in enumerate(frames):
            if f is None:
                logging.warning(f"Skipping None frame at index {i}")
                continue

            # confirm frame is correct size & 3 channels (BGR)
            if f.shape[1::-1] != size:
                # resize to the desired size to avoid writer issues
                f = cv2.resize(f, size)

            # If frame has alpha channel, drop it
            if f.ndim == 3 and f.shape[2] == 4:
                f = f[:, :, :3]

            # If grayscale, convert to BGR
            if f.ndim == 2:
                f = cv2.cvtColor(f, cv2.COLOR_GRAY2BGR)

            out.write(f)

        out.release()
        logging.info(f"Video written successfully: {output_path}")

    except Exception as e:
        if 'out' in locals():
            out.release()
        logging.error(f"Error writing video: {str(e)}")
        raise CustomException(e, sys)

