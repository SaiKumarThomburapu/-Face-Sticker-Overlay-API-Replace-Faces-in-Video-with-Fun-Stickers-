import streamlit as st
import cv2
import numpy as np
import tempfile
import os
from insightface.app import FaceAnalysis
from PIL import Image

# Setup face detector
@st.cache_resource
def load_model():
    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0)
    return app

app = load_model()

# Utils
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def compute_centroid(cluster):
    return np.mean(np.stack(cluster), axis=0)

def is_same_person(emb, cluster, threshold=0.6):
    sims = [cosine_similarity(emb, e) for e in cluster]
    return np.mean(sims) > threshold

def overlay_sticker(frame, bbox, sticker_img):
    x1, y1, x2, y2 = bbox.astype(int)
    h, w = frame.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    face_w, face_h = x2 - x1, y2 - y1
    if face_w <= 0 or face_h <= 0:
        return frame

    sticker_resized = cv2.resize(sticker_img, (face_w, face_h))
    if sticker_resized.shape[2] == 4:
        alpha_s = sticker_resized[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(3):
            frame[y1:y2, x1:x2, c] = (
                alpha_s * sticker_resized[:, :, c] +
                alpha_l * frame[y1:y2, x1:x2, c]
            )
    else:
        frame[y1:y2, x1:x2] = sticker_resized

    return frame

# App
st.title("🎭 Face Sticker Overlay App")

st.markdown("Upload a **video** and a **sticker (PNG)** to overlay on selected faces. This app clusters the same person across frames so you only see one face per identity.")

uploaded_video = st.file_uploader("Upload a video", type=["mp4"])
uploaded_sticker = st.file_uploader("Upload a sticker (PNG)", type=["png"])

if uploaded_video and uploaded_sticker:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        video_path = temp_video.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_sticker:
        temp_sticker.write(uploaded_sticker.read())
        sticker_path = temp_sticker.name

    st.video(video_path)

    sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_gap = int(fps * 1)  # 1 frame per second for clustering

    face_clusters = []
    face_thumbnails = []

    st.info("Detecting and clustering faces...")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_gap == 0:
            faces = app.get(frame)
            for face in faces:
                emb = face.embedding
                matched = False
                for cluster in face_clusters:
                    if is_same_person(emb, cluster):
                        cluster.append(emb)
                        matched = True
                        break
                if not matched:
                    face_clusters.append([emb])
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    face_crop = frame[y1:y2, x1:x2]
                    if face_crop.size > 0:
                        face_thumbnails.append(face_crop)
        frame_idx += 1
    cap.release()

    centroids = [compute_centroid(cluster) for cluster in face_clusters]

    st.success(f"✅ Found {len(centroids)} unique faces across video")

    selected_idxs = []
    st.subheader("👉 Select Faces to Replace with Sticker")

    cols = st.columns(4)
    for i, thumb in enumerate(face_thumbnails):
        with cols[i % 4]:
            st.image(thumb, width=150, caption=f"Face #{i}")
            if st.checkbox(f"Replace Face #{i}"):
                selected_idxs.append(i)

    if st.button("🚀 Replace and Download"):
        cap = cv2.VideoCapture(video_path)
        frames_out = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            faces = app.get(frame)
            for face in faces:
                emb = face.embedding
                for idx in selected_idxs:
                    centroid = centroids[idx]
                    if cosine_similarity(emb, centroid) > 0.5:  # Relaxed matching
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

        st.video(output_path)
        with open(output_path, "rb") as f:
            st.download_button("📥 Download Final Video", f, file_name="output_swapped.mp4")

