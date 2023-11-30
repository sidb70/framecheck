import backend.speech2text as speech2text
from backend.audio import Audio
import argparse
import backend.fact_checker as fact_checker
from typing import Tuple, Dict, List
import os
from typing import Union
from fastapi import FastAPI
app = FastAPI()


VIDEOS_DIR  = './.videos/{}/'

@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.get("/video/{id}")
def read_video(id: str):
    url = 'https://www.youtube.com/watch?v=' + id
    claims_results = main(url, id)
    return claims_results
    
def download_and_transcribe(url: str, id: str, video_dir: str) -> Tuple[str, Audio]:
    '''
    Downloads audio from youtube video and transcribes it
    :param url: url of youtube video
    :return: transcription of audio
    '''
    audio = Audio(url, id, video_dir)
    audio.split()
    five_sec_chunks = audio.audio_chunks_fivesec
    transcript_path = audio.get_path().strip('mp3') + 'txt'
    if not os.path.exists(transcript_path):
        transcription = speech2text.transcribe(five_sec_chunks)
        # save transcription
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, 'w') as f:
            f.write(transcription)
    else:
        with open(transcript_path, 'r') as f:
            transcription = f.read()
    print("transcription complete")
    return transcription, transcript_path, audio
def fact_check(transcript: str, video_base_dir: str) -> List[Dict[str, str]]:
    '''
    Checks the facts in the transcribed audio
    :param transcript: transcript of audio
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
    transcript, transcript_path, audio = download_and_transcribe(url, id, video_dir)
    results = fact_check(transcript, video_dir)
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

