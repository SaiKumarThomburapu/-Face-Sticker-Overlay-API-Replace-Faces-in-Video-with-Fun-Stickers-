# Directory for session data and outputs
OUTPUT_DIR = "artifacts"

# File names and extensions
INPUT_VIDEO_FILENAME = "input.mp4"
STICKER_FILENAME = "sticker.png"
OUTPUT_VIDEO_FILENAME = "output.mp4"
FINAL_OUTPUT_FILENAME = "output_with_audio.mp4"
PREVIEW_FILENAME_PREFIX = "cluster_"
PREVIEW_EXTENSION = ".jpg"
TEMP_AUDIO_EXTENSION = "_audio.aac"

# Clustering parameters
EPS = 0.6
MIN_SAMPLES = 3
METRIC="cosine"

# Video frame rate
FRAME_RATE = 30

# Face model configuration
FACE_MODEL_NAME = "buffalo_l"
FACE_MODEL_PROVIDERS = ["CPUExecutionProvider"]



