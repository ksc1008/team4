import queue
import os
import sys
import openai
import json
import urllib.request
from datetime import datetime
from gtts import gTTS

import speech_recognition as sr

import wave
from playsound import playsound
import threading
import sounddevice as sd
import soundfile as sf

from multiprocessing import Process, Queue, freeze_support
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QThread, QObject

from keyboardEvent import ShorCut

# from "ui 파일 이름" import Ui_MainWindow

# ==========================================================

q = queue.Queue()

os.makedirs("history", exist_ok=True)  # history 폴더 생성
#os.environ['OPENAI_API_KEY'] = '(Enter Key Here!)'  # 환경변수에 API_KEY값 지정
openai.api_key = os.getenv("OPENAI_API_KEY")
#
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant who is good at detailing."
    }
]


# ChatGPT API 함수 : ChatGPT 응답을 return
def query_chatGPT(prompt):
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = completion["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer


# QFileDialog로 부터 file_name을 입력받아 history를 오픈
def open_history(file_name):
    if file_name:
        with open(file_name, 'r') as f:
            data = json.load(f)
    return data


# QfileDialog로 부터 file_name을 입력받아 history를 저장
def save_history(file_name):
    if file_name:
        text = messages
        with open(file_name, 'w', encoding='UTF-8') as f:
            json.dump(text, f)


# 음성녹음 함수 : record.wav로 저장
def voice_recorder():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Recording Strated...")
        audio = r.listen(source)
        print("Recording Finished")
    with open("record.wav", "wb") as file:
        file.write(audio.get_wav_data())


# whisper API 함수 : wav파일을 입력받아 text를 return
def whisper_api(file):
    transcript = openai.Audio.transcribe("whisper-1", file)
    text = transcript['text']
    return text


def papago_kte(prompt):  # 파파고를 이용하여 한국어를 영어로 번역하는 함수
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

    result = json.loads(response_body.decode('utf-8'))  # json형식으로 온 response를 str형태로 변환
    return result['message']['result']['translatedText']


def papago_etk(prompt):  # 파파고를 이용하여 영어를 한국어로 번역하는 함수
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


# ==========================================================
# 녹음

# 녹음 시작 함수
def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()


# 녹음 종료 함수
def stop():
    global recorder
    global recording
    recording = False
    recorder.join()
    print('stop recording')


def complicated_record():
    with sf.SoundFile("record.wav", mode='w', samplerate=16000, subtype='PCM_16', channels=1) as file:
        with sd.InputStream(samplerate=16000, dtype='int16', channels=1, callback=complicated_save):
            while recording:
                file.write(q.get())


def complicated_save(indata, frames, time, status):
    q.put(indata.copy())


# ==========================================================
# Producer & Consumer

class Producer(QThread):
    def __init__(self, prompt_que, answer_que):
        super().__init__()
        self.prompt_que = prompt_que
        self.answer_que = answer_que
        self.shortcut = None

    def run(self):
        while True:
            if not self.prompt_que.empty():
                prompt = self.prompt_que.get()
                try:
                    answer = query_chatGPT(prompt)
                    answer = answer.strip()
                    self.answer_que.put(answer)

                except openai.error.Timeout as e:
                    # Handle timeout error, e.g. retry or log
                    msg = f"OpenAI API request timed out: {e}"
                    self.shortcut.throwError.emit(msg)

                    pass
                except openai.error.APIError as e:
                    # Handle API error, e.g. retry or log
                    msg = f"OpenAI API returned an API Error: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass
                except openai.error.APIConnectionError as e:
                    # Handle connection error, e.g. check network or log
                    msg = f"OpenAI API request failed to connect: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass
                except openai.error.InvalidRequestError as e:
                    # Handle invalid request error, e.g. validate parameters or log
                    msg = f"OpenAI API request was invalid: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass
                except openai.error.AuthenticationError as e:
                    # Handle authentication error, e.g. check credentials or log
                    msg = f"OpenAI API request was not authorized: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass
                except openai.error.PermissionError as e:
                    # Handle permission error, e.g. check scope or log
                    msg = f"OpenAI API request was not permitted: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass
                except openai.error.RateLimitError as e:
                    # Handle rate limit error, e.g. wait or log
                    msg = f"OpenAI API request exceeded rate limit: {e}"
                    self.shortcut.throwError.emit(msg)
                    pass


class Consumer(QThread):

    def __init__(self, answer_que):
        super().__init__()
        self.answer_que = answer_que
        self.shortcut = None

    def run(self):
        while True:
            if not self.answer_que.empty():
                data = self.answer_que.get()
                self.shortcut.message_arrived.emit(data)


class WhisperWorker(QThread):
    def __init__(self, audio_que, prompt_que):
        super().__init__()
        self.audio_que = audio_que
        self.prompt_que = prompt_que
        self.shortcut = None

    def run(self):
        while True:
            if not self.audio_que.empty():
                try:
                    t = self.audio_que.get()
                    audio = open("record.wav", "rb")
                    prompt = whisper_api(audio)
                    if len(prompt):
                        self.prompt_que.put(prompt)
                except openai.error.Timeout as e:
                  #Handle timeout error, e.g. retry or log
                  msg = f"OpenAI API request timed out: {e}"
                  self.shortcut.throwError.emit(msg)

                  pass
                except openai.error.APIError as e:
                  #Handle API error, e.g. retry or log
                  msg = f"OpenAI API returned an API Error: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass
                except openai.error.APIConnectionError as e:
                  #Handle connection error, e.g. check network or log
                  msg = f"OpenAI API request failed to connect: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass
                except openai.error.InvalidRequestError as e:
                  #Handle invalid request error, e.g. validate parameters or log
                  msg = f"OpenAI API request was invalid: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass
                except openai.error.AuthenticationError as e:
                  #Handle authentication error, e.g. check credentials or log
                  msg = f"OpenAI API request was not authorized: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass
                except openai.error.PermissionError as e:
                  #Handle permission error, e.g. check scope or log
                  msg = f"OpenAI API request was not permitted: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass
                except openai.error.RateLimitError as e:
                  #Handle rate limit error, e.g. wait or log
                  msg = f"OpenAI API request exceeded rate limit: {e}"
                  self.shortcut.throwError.emit(msg)
                  pass


class MyWindow(QObject):
    prompt_que = Queue()
    answer_que = Queue()
    audio_que = Queue()

    def __init__(self):
        super().__init__()
        # ====================================================
        self.whisperWorker = WhisperWorker(MyWindow.audio_que, MyWindow.prompt_que)
        self.whisperWorker.start()

        self.producer = Producer(MyWindow.prompt_que, MyWindow.answer_que)
        self.producer.start()

        self.consumer = Consumer(MyWindow.answer_que)
        self.consumer.start()

        # ====================================================
        self.shortcut = None

    def initiate(self, sc: ShorCut):
        self.shortcut = sc
        self.shortcut.mic_key.connect(self.on_record)
        self.shortcut.release_mic_key.connect(self.off_record)
        self.consumer.shortcut = sc
        self.producer.shortcut = sc
        self.whisperWorker.shortcut = sc

    # 레코드 시작 슬롯
    @pyqtSlot()
    def on_record(self):
        start()

    # 레코드 종료 & 위스퍼를 통해 stt
    @pyqtSlot()
    def off_record(self):
        stop()
        self.shortcut.start_prompt.emit()
        MyWindow.audio_que.put(0)

    @pyqtSlot(str)
    def on_message_arrived(self, data):
        self.shortcut.message_arrived.emit(data)