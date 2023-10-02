from fastapi import FastAPI, File,UploadFile,Request, HTTPException,status
from fastapi.responses import HTMLResponse, FileResponse
import shutil
from pathlib import Path
from fastapi.templating import Jinja2Templates

app = FastAPI(debug=True)

video_dir = Path("static/videos")

templates = Jinja2Templates(directory="templetes")

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024

@app.post("/upload/")
async def upload_video(file: UploadFile):
    try: 
        video_dir.mkdir(parents=True)
    except FileExistsError:
        pass

    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds the upload limit")

    video_path = video_dir / file.filename
    with video_path.open("wb") as buffer :
        buffer.write(file_content)
    return{"message":"Video Uploaded Successfully"}


@app.get("/", response_class=HTMLResponse)
def get_upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request":request})

@app.get("/stream/{video_name}")
def stream_video(video_name: str):
    video_path = video_dir / video_name
    if video_path.exists():
        return FileResponse(video_path)
    else:
        return {"error":"Video not found"}