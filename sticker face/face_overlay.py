import cv2
import numpy as np
import os
from insightface.app import FaceAnalysis
from utils import cosine_similarity, compute_centroid, overlay_sticker

def load_model():
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0)
    return app

def cluster_faces(video_path, model):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_gap = int(fps * 1)

    face_clusters = []
    face_thumbnails = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_gap == 0:
            faces = model.get(frame)
            for face in faces:
                emb = face.embedding
                matched = False
                for cluster in face_clusters:
                    if cosine_similarity(emb, compute_centroid(cluster)) > 0.6:
                        cluster.append(emb)
                        matched = True
                        break
                if not matched:
                    face_clusters.append([emb])
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    crop = frame[y1:y2, x1:x2]
                    if crop.size > 0:
                        face_thumbnails.append(crop)
        frame_idx += 1
    cap.release()

    centroids = [compute_centroid(c) for c in face_clusters]
    return centroids, face_thumbnails

def process_video(video_path, sticker_path, selected_indices, threshold=0.5):
    model = load_model()
    sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
    centroids, _ = cluster_faces(video_path, model)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_out = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = model.get(frame)
        for face in faces:
            emb = face.embedding
            for idx in selected_indices:
                if cosine_similarity(emb, centroids[idx]) > threshold:
                    frame = overlay_sticker(frame, face.bbox, sticker)
                    break
        frames_out.append(frame)
    cap.release()

    output_path = os.path.join("outputs", "output_swapped.mp4")
    os.makedirs("outputs", exist_ok=True)
    h, w = frames_out[0].shape[:2]
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for f in frames_out:
        out.write(f)
    out.release()

    return output_path, len(centroids), _

