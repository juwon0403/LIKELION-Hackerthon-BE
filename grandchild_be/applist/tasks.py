# tasks.py

from celery import shared_task
from gtts import gTTS
import os
from django.conf import settings

'''@shared_task
def create_tts_file(text):
    # TTS 생성 작업
    tts = gTTS(text=text, lang='ko', slow=False)
    
    # TTS를 임시 파일로 저장
    tts_file = os.path.join(settings.MEDIA_ROOT, 'temp_tts.mp3')
    tts.save(tts_file)
    
    # 임시 파일의 URL 구하기
    tts_url = settings.MEDIA_URL + 'temp_tts.mp3'

    return tts_url'''


'''@shared_task
def create_tts_file(text, task_id):
    # TTS 생성 작업
    tts = gTTS(text=text, lang='ko', slow=False)

    # TTS를 임시 파일로 저장
    tts_file = os.path.join(settings.MEDIA_ROOT, f'temp_tts_{task_id}.mp3')
    tts.save(tts_file)

    # 임시 파일의 URL 구하기
    tts_url = settings.MEDIA_URL + f'temp_tts_{task_id}.mp3'

    return tts_url'''
    
@shared_task
def create_tts_file(text, task_id):
    # TTS 생성 작업
    tts = gTTS(text=text, lang='ko', slow=False)
    
    # TTS를 임시 파일로 저장
    temp_filename = f'temp_tts_{task_id}.mp3'
    tts_file = os.path.join(settings.MEDIA_ROOT, temp_filename)
    tts.save(tts_file)
    
    # 임시 파일의 URL 구하기
    tts_url = settings.MEDIA_URL + temp_filename

    return tts_url

