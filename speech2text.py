from google.cloud import speech
import os
from pydub import AudioSegment
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


def transcribe(stream):
    
    client = speech.SpeechClient.from_service_account_json('key.json')
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
    )
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    responses = client.streaming_recognize(streaming_config, requests)
    transcript = ''
    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            alternative = result.alternatives[0]
            # The alternatives are ordered from most likely to least.
            transcript += alternative.transcript
    return transcript
          
