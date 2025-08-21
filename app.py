
import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from src.pipeline.upload_service import upload_service
from src.pipeline.render_service import render_service
from src.logger import logging

app = FastAPI()

# Ensure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

# In-memory session storage
session_data = {}

@app.post("/upload/")
async def upload_files(video: UploadFile = File(...), sticker: UploadFile = File(...)):
    try:
        result = await upload_service(video, sticker, session_data)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/render/")
def render_video(session_id: str = Form(...), cluster_ids: str = Form(...)):
    try:
        final_output_path = render_service(session_id, cluster_ids, session_data)
        return FileResponse(final_output_path, media_type="video/mp4", filename="output_sticker_overlay_with_audio.mp4")
    except Exception as e:
        logging.error(f"Render error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/debug/session/{session_id}")
def debug_session(session_id: str):
    if session_id not in session_data:
        return JSONResponse(status_code=404, content={"error":"session not found"})
    data = session_data[session_id]
    # return minimal info so we don't blow up HTTP response with images
    return {
        "video_path": data.get("video_path"),
        "sticker_path": data.get("sticker_path"),
        "clusters_count": len(data.get("clusters", {})),
        "clusters_keys": list(data.get("clusters", {}).keys())
    }






