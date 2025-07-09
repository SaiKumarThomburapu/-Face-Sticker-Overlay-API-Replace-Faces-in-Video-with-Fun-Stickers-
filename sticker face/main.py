from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import shutil
import os
import uuid
import base64
from io import BytesIO
from PIL import Image
import cv2

from face_overlay import process_video, load_model, cluster_faces
from models.schema import FaceReplaceRequest

app = FastAPI()

@app.post("/replace-faces/")
async def replace_faces(
    video: UploadFile = File(...),
    sticker: UploadFile = File(...),
    selected_indices: str = Form(...)
):
    vid_path = f"temp_{uuid.uuid4().hex}.mp4"
    sticker_path = f"temp_{uuid.uuid4().hex}.png"

    with open(vid_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    with open(sticker_path, "wb") as buffer:
        shutil.copyfileobj(sticker.file, buffer)

    selected = list(map(int, selected_indices.split(",")))

    output_path, num_faces, _ = process_video(vid_path, sticker_path, selected)

    return FileResponse(output_path, media_type="video/mp4", filename="output_swapped.mp4")

@app.post("/list-faces/")
async def list_faces(video: UploadFile = File(...)):
    temp_path = f"temp_{uuid.uuid4().hex}.mp4"
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(video.file, f)

    model = load_model()
    centroids, thumbnails = cluster_faces(temp_path, model)

    face_data = []
    for idx, face in enumerate(thumbnails):
        img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        buffered = BytesIO()
        pil_img.save(buffered, format="PNG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
        face_data.append({
            "index": idx,
            "thumbnail_base64": f"data:image/png;base64,{encoded_img}"
        })

    return JSONResponse(content={"faces": face_data})

