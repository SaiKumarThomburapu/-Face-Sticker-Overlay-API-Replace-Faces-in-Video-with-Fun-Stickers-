import cv2

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
        
        # Check if this frame has faces to overlay
        if idx in frame_map:
            for face_data in frame_map[idx]:
                # Get the bounding box for this face
                bbox = face_data["bbox"]
                # Apply the overlay and GET THE MODIFIED FRAME BACK
                frame = sticker_overlay.overlay(frame, bbox, sticker_img)
        
        frames.append(frame)
        idx += 1
    
    cap.release()
    return frames

def write_video(frames, output_path, frame_rate, size):
    # Ensure the codec is supported for .mp4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use (*'avc1') for H.264 if available
    out = cv2.VideoWriter(output_path, fourcc, frame_rate, size)
    
    for frame in frames:
        out.write(frame)
    
    out.release()




# import cv2
# from src.constants import *

# def create_frame_map(selected, clusters):
#     frame_map = {}
#     for cid in selected:
#         for f in clusters.get(cid, []):
#             frame_map.setdefault(f["frame"], []).append(f)
#     return frame_map

# def process_video_frames(video_path, frame_map, sticker_img, sticker_overlay):
#     cap = cv2.VideoCapture(video_path)
#     frames = []
#     idx = 0

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if idx in frame_map:
#             for f in frame_map[idx]:
#                 frame = sticker_overlay.overlay(frame, f["bbox"], sticker_img)
#         frames.append(frame)
#         idx += 1
#     cap.release()
#     return frames

# def write_video(frames, output_path, frame_rate, size):
#     out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)
#     for f in frames:
#         out.write(f)
#     out.release()

