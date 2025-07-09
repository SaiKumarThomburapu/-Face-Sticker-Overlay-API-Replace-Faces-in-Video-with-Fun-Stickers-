import numpy as np
import cv2

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def compute_centroid(cluster):
    return np.mean(np.stack(cluster), axis=0)

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
