import sounddevice
from scipy.io.wavfile import write
import os
import sys
import openai
import json
import urllib.request
from datetime import datetime
from gtts import gTTS

import speech_recognition as sr

import pyaudio
import wave
from playsound import playsound

from multiprocessing import Process, Queue, freeze_support


os.environ['OPENAI_API_KEY'] = '(자신이 가진 charGPT API를 입력)' #환경변수에 API_KEY값 지정
openai.api_key = os.getenv("OPENAI_API_KEY")

#ChatGPT API 함수 : ChatGPT 응답을 return
def query_chatGPT(prompt):
    completion = openai.ChatCompletion.create(
         model = "gpt-3.5-turbo",
      messages = [{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]

#음성녹음 함수 : record.wav로 저장
def voice_recorder():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording Strated...")
        audio = r.listen(source)
        print("Recording Finished")
    with open("record.wav", "wb") as file:
        file.write(audio.get_wav_data())

#whisper API 함수 : wav파일을 입력받아 text를 return
def whisper_api(file):
    transcript = openai.Audio.transcribe("whisper-1", file)
    text = transcript['text']
    return text

def papago_kte(prompt): #파파고를 이용하여 한국어를 영어로 번역하는 함수
    client_id = "(자신이 가진 파파고 API ID를 입력)"  # 개발자센터에서 발급받은 Client ID 값
    client_secret = "(자신이 가진 파파고 비번을 입력)"  # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(prompt)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
    else:
        print("Error Code:" + rescode)

    result = json.loads(response_body.decode('utf-8')) #json형식으로 온 response를 str형태로 변환
    return result['message']['result']['translatedText']

def papago_etk(prompt): #파파고를 이용하여 영어를 한국어로 번역하는 함수
    client_id = "(자신이 가진 파파고 API ID를 입력)"  # 개발자센터에서 발급받은 Client ID 값
    client_secret = "(자신이 가진 파파고 비번을 입력)"  # 개발자센터에서 발급받은 Client Secret 값
    encText = urllib.parse.quote(prompt)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
    else:
        print("Error Code:" + rescode)

    result = json.loads(response_body.decode('utf-8'))
    return result['message']['result']['translatedText']



if __name__ == "__main__":

    #한국어로 목소리 녹음
    voice_recorder()
    audio_file = open("record.wav", "rb")
    question = whisper_api(audio_file)
    print(question)
    #파파고로 번역해서 영어로 질문
    papago_qestion = papago_kte(question)
    print("파파고 번역: " + papago_qestion)

    #chatGPT 영어 대답
    en_answer = query_chatGPT(papago_qestion)
    print("영어 대답 : " + en_answer)

    #chatGPT 대답 한국어로 번역
    kr_answer = papago_etk(en_answer)
    print("한국어 대답 : " + kr_answer)