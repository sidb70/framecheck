from yt_dlp import YoutubeDL
import os
from pydub import AudioSegment
from typing import Tuple

class Chunk:
    def __init__(self, audio_path: str):
        self.audio_path = audio_path
        self.audio = AudioSegment.from_file(audio_path, format='mp3')
    def get_path(self) -> str:
        return self.audio_path

class AudioChunks:
    def __init__(self):
        self.audio_chunks = []
        self.curr_chunk=0
    def add_chunk(self, chunk: Chunk):
        self.audio_chunks.append(chunk)
    def __iter__(self):
        return self
    def __next__(self):
        return self.next()
    def next(self):
        if self.curr_chunk < len(self.audio_chunks):
            chunk = self.audio_chunks[self.curr_chunk]
            with open(chunk.get_path(), 'rb') as f:
                content = f.read()
            self.curr_chunk += 1
            return content 
        else:
            raise StopIteration
    def __len__(self):
        return len(self.audio_chunks)

class Audio:
    '''
    Manages audio for a youtube video
    '''
    def __init__(self,url: str, id: str, video_dir: str):
        '''
        Initializes AudioManager
        :param url: url of youtube video
        '''
        self.url = url
        self.id = id
        self.base_dir = video_dir
        self.audio_path= self.save_audio(url)
        self.audio = AudioSegment.from_file(self.audio_path, format='mp3')
        self.audio_chunks_onemin = AudioChunks()
        self.audio_chunks_fivesec = AudioChunks()
        self.curr_chunk=0
    def split(self):
        '''
        Splits audio into 5 second chunks and 1 minute chunks and saves them in .audio/video_id/
        '''
        if len(self.audio_chunks_onemin) == 0:
            chunks =[]
            for i in range(0, len(self.audio), 59000):
                chunks.append(self.audio[i:i+59000])

            for i in range(len(chunks)):
                chunk_path = './.videos/{}/audio/chunks_onemin/{}'.format(self.id, str(i) + '.mp3')
                chunks[i].export(chunk_path, format='mp3')
                chunk = Chunk(chunk_path)
                self.audio_chunks_onemin.add_chunk(chunk)
        if len(self.audio_chunks_fivesec) == 0:
            chunks =[]
            for i in range(0, len(self.audio), 5000):
                chunks.append(self.audio[i:i+5000])

            for i in range(len(chunks)):
                chunk_path = './.videos/{}/audio/chunks_fivesec/{}'.format(self.id, str(i) + '.mp3')
                chunks[i].export(chunk_path, format='mp3')
                chunk = Chunk(chunk_path)
                self.audio_chunks_fivesec.add_chunk(chunk)
        
    def to_mp3(self,audio_path: str) -> str:
        '''
        Converts audio to mp3
        '''
        if audio_path.split('.')[-1] == 'wav':
            wav_path = audio_path
            audio = AudioSegment.from_wav(wav_path)
            audio = audio.set_frame_rate(16000)
            mp3_path = wav_path.split('.')[0] + '.mp3'
            audio.export(mp3_path, format="mp3")
            os.remove(wav_path)
        else:
            mp3_path = audio_path
        return mp3_path
    def save_audio(self,url: str) -> Tuple[str,str]:
        '''
        Saves audio from youtube video into .audio/video_id
        chunks audio into 5 second chunks and saves them in .audio/video_id/chunks
        '''
        ydl_opts = {
            'outtmpl': '%(id)s.%(ext)s',
            'format': 'wav/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }]
        }
        out_path = self.base_dir + '/audio/{}.mp3'.format(self.id)
        if not os.path.exists(out_path):
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                # convert to mp3
                mp3_path = self.to_mp3('{}.wav'.format(self.id))
                # move to audio folder
                if not os.path.exists(self.base_dir + '/audio/chunks_onemin'.format(self.id)):
                    os.makedirs(self.base_dir + '/audio/chunks_onemin'.format(self.id))
                if not os.path.exists(self.base_dir + '/audio/chunks_fivesec'.format(self.id)):
                    os.makedirs(self.base_dir + '/audio/chunks_fivesec'.format(self.id))
                os.rename(mp3_path, out_path)

        return out_path
    def get_one_min_chunks(self) -> AudioChunks:
        '''
        Returns 1 minute chunks of audio
        '''
        return self.audio_chunks_onemin
    def get_five_sec_chunks(self) -> AudioChunks:
        '''
        Returns 5 second chunks of audio
        '''
        return self.audio_chunks_fivesec
    def get_path(self) -> str:
        '''
        Returns path of audio
        '''
        return self.audio_path
    