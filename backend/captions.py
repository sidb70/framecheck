from yt_dlp import YoutubeDL
import os
import re

opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'outtmpl': '%(id)s.captions.%(ext)s',
    'quiet': True
}
TIME_STAMP_MATCH = '\d{2}:\d{2}:\d{2}\.\d+ --> \d{2}:\d{2}:\d{2}\.\d+'
def extract_transcript_from_captions(captions_path):
    file_lines = []
    with open(captions_path, 'r') as f:
        for i in range(3):
            # skip header lines
            f.readline()
        file_lines = [line.strip() for line in f.readlines() if line.strip() != '']
    transcript_pieces = []
    curr_time_stamp = ''
    curr_piece = ''
    for line in file_lines:
        if re.match(TIME_STAMP_MATCH, line):
            if curr_piece:
                transcript_pieces.append((curr_piece, curr_time_stamp))
                curr_piece = ''
            curr_time_stamp = line.split(' ')[0]
        else:
            curr_piece += line + ' '
    transcript = ''.join([p[0] for p in transcript_pieces])
    return transcript, transcript_pieces


def download_transcript(url, id, base_dir):
    out_path = base_dir + '/captions/{}.captions.en.vtt'.format(id)
    if not os.path.exists(out_path):
        print("downloading captions")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
            os.rename('{}.captions.en.vtt'.format(id), out_path)
    else:
        print("captions already downloaded")
    
    transcript_path = base_dir + '/captions/{}.transcript.txt'.format(id)
    if not os.path.exists(transcript_path):
        transcript, transcript_pieces = extract_transcript_from_captions(out_path)
        os.makedirs(os.path.dirname(transcript_path), exist_ok=True)
        with open(transcript_path, 'w') as f:
            f.write(transcript)
    else:
        with open(transcript_path, 'r') as f:
            transcript = f.read()
    return transcript, transcript_path

    