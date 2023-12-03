import backend.speech2text as speech2text
import backend.fact_checker as fact_checker
import backend.captions as captions
from typing import Tuple, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import argparse

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add the origin of your Next.js app
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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api/video/{id}")
def read_video(id: str):
    print("Received id: " + id)
    url = 'https://www.youtube.com/watch?v=' + id
    claims_results = main(url, id)
    return claims_results
    
def download_and_transcribe(url: str, id: str, base_dir: str) -> Tuple[str, str]:
    '''
    Gets the transcript of the video
    :param url: url of youtube video
    :return transcript: transcript of video
    :return transcript_path: path to transcript
    '''
    transcription, transcript_path = captions.download_transcript(url, id, base_dir)
    return transcription, transcript_path
def fact_check(transcript: str, video_base_dir: str) -> List[Dict[str, str]]:
    '''
    Checks the facts in the video transcript
    :param transcript: transcript of video
    '''
    claims, claims_path = fact_checker.extract_claims(transcript, video_base_dir)
    results = fact_checker.check_claims(claims, claims_path)
    return results
def main(url: str, id: str):
    '''
    Main function
    :param url: url of youtube video
    '''
    video_dir = VIDEOS_DIR.format(id)
    transcript, transcript_path = download_and_transcribe(url, id, video_dir)
    results = fact_check(transcript, video_dir)
    print("returning", len(results), "results")
    return results
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Fact check this video')
        parser.add_argument('url', type=str, help='url of video to fact check')
        args = parser.parse_args()
        url = args.url
    except SystemExit as e:
        url = input('url of video to fact check: ')
    main(url)

