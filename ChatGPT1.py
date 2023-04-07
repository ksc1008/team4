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
from scipy.io.wavfile import write
import time
import keyboard

from multiprocessing import Process, Queue, freeze_support
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PySide6.QtCore import Signal, Slot, Qt, QTimer, QThread
from PySide6.QtGui import QIcon, QPixmap, QFont

from "ui 파일 이름" import Ui_MainWindow

# ==========================================================

q = queue.Queue()


os.makedirs("history", exist_ok=True) #history 폴더 생성
os.environ['OPENAI_API_KEY'] = '(자신이 가진 charGPT API를 입력)' #환경변수에 API_KEY값 지정
openai.api_key = os.getenv("OPENAI_API_KEY")
#
messages = [
    {
        "role" : "system",
        "content" : "You are a helpful assistant who is good at detailing."
    }
]
#ChatGPT API 함수 : ChatGPT 응답을 return
def query_chatGPT(prompt):
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    answer = completion["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer

#QFileDialog로 부터 file_name을 입력받아 history를 오픈
def open_history(file_name):
    if file_name:
        with open(file_name, 'r') as f:
            data = json.load(f)
    return data

#QfileDialog로 부터 file_name을 입력받아 history를 저장
def save_history(file_name):
    if file_name:
        text = messages
        with open(file_name, 'w', encoding='UTF-8') as f:
            json.dump(text, f)

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

# ==========================================================
# 녹음

#녹음 시작 함수
def start():
    global recorder
    global recording
    recording = True
    recorder = threading.Thread(target=complicated_record)
    print('start recording')
    recorder.start()

#녹음 종료 함수
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
#Producer & Consumer

class Producer(QThread):
    def __init__(self, prompt_que, answer_que):
        super().__init__()
        self.prompt_que = prompt_que
        self.answer_que = answer_que

    def run(self):
        while True:
            if not self.prompt_que.empty():
                prompt = self.prompt_que.get()
                answer = query_chatGPT(prompt)
                answer = answer.strip()
                self.answer_que.put(answer)
            else:
                continue

class Consumer(QThread):
    message_arrived = Signal(str)

    def __init__(self, answer_que):
        super().__init__()
        self.answer_que    = answer_que

    def run(self):
        while True:
            if not self.answer_que.empty():
                data = self.answer_que.get()
                self.message_arrived.emit(data)


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #super().__init__()
        QMainWindow.__init__(self, None, Qt.WindowStaysOnTopHint)
        self.setupUi(self)
        # ====================================================
        self.producer = Producer(prompt_que, answer_que)
        self.producer.start()

        self.consumer = Consumer(answer_que)
        self.consumer.start()

        # ====================================================
        self.consumer.message_arrived.connect(self.on_message_arrived)
        self.consumer.message_waiting.connect(self.on_message_waiting)
        self."녹화 시작 시그널이름"(self.on_record)
        self."녹화 종료 시그널이름"(self.off_record)

    #레코드 시작 슬롯
    @Slot(int)
    def on_record(self):
        start()

    #레코드 종료 & 위스퍼를 통해 stt
    @Slot(int)
    def off_record(self):
        stop()
        audio_file = open("record.wav", "rb")
        question = whisper_api(audio_file)

        if len(question):
            prompt_que.put(question)

    @Slot(str)
    def on_message_arrived(self, data):
        self.answer_arrived = True
        decorate = f"ChatGPT>: {data}"
        self.text_answer.append(decorate)
        self.text_answer.ensureCursorVisible()

if __name__ == "__main__":
    prompt_que = Queue()
    answer_que = Queue()

    if not QApplication.instance():
        print("QApplication(sys.argv)")
        app = QApplication(sys.argv)
    else:
        print("QApplication.instance()")
        app = QApplication.instance()

    win = MyWindow()
    win.show()