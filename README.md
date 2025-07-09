# Face Sticker Overlay API

This is a fun and smart tool that can take a video, find all the people (faces) inside it, and let you choose which faces to cover with your own cool sticker — like an emoji or cartoon image. You can use this app to hide faces or just make your video more fun!

This project works completely as a **FastAPI** backend, so it’s ready to connect with any web or mobile app.

---

## What This App Can Do

* Accepts any video (like an `.mp4` file)
* Uses AI to find all the unique faces in the video
* Shows thumbnails (small pictures) of each face
* Lets you choose which faces you want to cover
* Overlays a sticker (like an emoji PNG image) on those faces throughout the whole video
* Gives you back a final video with those stickers in place

---

## How to Run This

### 1. Clone this Repo

```bash
git clone https://github.com/your-username/face-sticker-overlay-api.git
cd face-sticker-overlay-api
```

### 2. Install the Python Packages

You can use a virtual environment if you want.

```bash
pip install -r requirements.txt
```

### 3. Start the FastAPI Server

```bash
uvicorn main:app --reload
```

Go to your browser and open:

```
http://localhost:8000/docs
```

You'll see a page where you can test the app yourself!

---

## How to Use

### Step 1: List All Faces in a Video

1. Use the `/list-faces/` endpoint
2. Upload your video file
3. You’ll get small pictures of all the faces inside the video
4. Each picture will have a number (like Face #0, Face #1)

### Step 2: Replace Faces with a Sticker

1. Use the `/replace-faces/` endpoint
2. Upload the same video file again
3. Upload a PNG sticker (transparent background works best)
4. Type the face numbers you want to replace (e.g. `0,1,3`)
5. It will return a new video with those faces covered!

---

## How It Works (Simple Terms)

* It looks at the video frame by frame (every 1 second).
* It checks who is in the video by looking at their face features.
* If the same person appears many times, it groups them together.
* Then when you say “cover Face #2,” it finds all those spots and puts your sticker on top!

---

## Project Structure

```
face_sticker_api/
├── main.py                # FastAPI app and API routes
├── face_overlay.py        # AI logic for face detection, clustering, and processing
├── utils.py               # Helper functions for face math and sticker blending
├── models/
│   └── schema.py          # Request format definitions
├── outputs/               # Final videos saved here
├── requirements.txt       # All needed Python packages
└── README.md              # You’re reading it!
```

---

## Sample Test Tools

* Test everything inside [http://localhost:8000/docs](http://localhost:8000/docs)
* Or use Postman to try the APIs

---

## Use Cases

* Hide people in a video (privacy)
* Make memes or funny clips
* Replace faces with emojis for school projects
* Add cartoon effects to YouTube Shorts or Reels

---

## Built With

* FastAPI for the backend
* InsightFace for face detection and recognition
* OpenCV for image & video editing
* Python for all the magic

---

## Need Help?

If you’re stuck, open an issue or just ping me!
