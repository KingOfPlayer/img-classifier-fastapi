from fastapi import FastAPI, UploadFile,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.prediction.image_classifier import Object_detection

app = FastAPI(title="img-classifier-fastapi")

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*",
    "http://127.0.0.1:8089/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def read_main():
    return {"msg": "OK!"}

@app.post("/predict", status_code=200)
async def predict_torch(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed."
        )
    contents = await file.read()
    if not contents:
        raise HTTPException(
            status_code=400, detail="No file uploaded. Please upload an image."
        )
    prediction = Object_detection(contents)
    if not prediction:
        raise HTTPException(
            status_code=404, detail="Prediction failed. Please try again."
        )

    return {"status_code": 200,
            "predicted_label": prediction[0],
            "probability": prediction[1]}

@app.get("/UI", response_class=HTMLResponse)
async def ui():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Image Upload</title>
</head>
<body>
    <h1>Upload an Image</h1>
    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""