import backend.speech2text as speech2text
import backend.fact_checker as fact_checker
import backend.captions as captions
from typing import Tuple, Dict, List
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import argparse
import uuid

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://wwww.framecheck.tech",
    "https://www.framecheck.tech",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VIDEOS_DIR  = './.videos/{}/'
tasks = {}
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/tasks/{task_id}")
async def task_status(task_id: str):
    print("Received task id: " + task_id)
    if task_id in tasks:
        return tasks[task_id]
@app.post("/api/video/{video_id}")
async def read_video(video_id: str, background_tasks: BackgroundTasks):
    print("Received id: " + video_id)
    url = 'https://www.youtube.com/watch?v=' + video_id
    unique_id = str(uuid.uuid4())
    tasks[unique_id] = {'status': 'PENDING', 'results': []}
    background_tasks.add_task(process_video, url, video_id, unique_id)
    return {"taskId": unique_id}

async def process_video(url: str, video_id: str, unique_id: str):
    print("Processing video with id: " + video_id)
    video_dir = VIDEOS_DIR.format(video_id)
    transcript, transcript_path = await download_and_transcribe(url, video_id, video_dir)

    results = await fact_check(transcript, video_dir)
    tasks[unique_id] = {'status': 'SUCCESS', 'results': results}

async def download_and_transcribe(url: str, video_id: str, base_dir: str) -> Tuple[str, str]:
    transcription, transcript_path = await captions.download_transcript(url, video_id, base_dir)
    return transcription, transcript_path

async def fact_check(transcript: str, video_base_dir: str) -> List[Dict[str, str]]:
    claims, claims_path = await fact_checker.extract_claims(transcript, video_base_dir)
    results = await fact_checker.check_claims(claims, claims_path)
    return results

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Fact check this video')
        parser.add_argument('url', type=str, help='url of video to fact check')
        args = parser.parse_args()
        url = args.url
    except SystemExit as e:
        url = input('url of video to fact check: ')
    import asyncio
    asyncio.run(main(url))
