import queue
import os
import sys
import openai
import json
import urllib.request
from datetime import datetime
from gtts import gTTS

import speech_recognition as sr
from google.cloud import speech

import pyaudio
from six.moves import queue

import wave
from playsound import playsound
import threading
import sounddevice as sd
import soundfile as sf

from multiprocessing import Process, Queue, freeze_support
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QThread, QObject

from keyboardEvent import KeyboardEvents

# from "ui 파일 이름" import Ui_MainWindow

# ==========================================================
from signalManager import SignalManager, KeyboardSignal, OverlaySignal

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

sttprompt = Queue()
streaming_queue = Queue()

os.makedirs("history", exist_ok=True)  # history 폴더 생성
os.environ['OPENAI_API_KEY'] = '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'  #환경변수에 API_KEY값 지정
openai.api_key = os.getenv("OPENAI_API_KEY")
#
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant who is good at detailing."
    }
]

#parameter 값을 option.json에 저장
def save_option():
    option = {}
    option['data'] = []
    option['data'].append({
        "temperature" : TEMPERATURE,
        "max_tokens" : MAX_TOKENS
    })
    with open("option.json", 'w') as outfile:
        json.dump(option,outfile)

def change_option():
    global TEMPERATURE
    global MAX_TOKENS
    save_option()

#ChatGPT Hyperparameter option.json 파일 열기 / 생성
try:
    with open("option.json", "r") as option_file:
        option_data = json.load(option_file)
        TEMPERATURE = option_data['data'][0]['temperature']
        MAX_TOKENS = option_data['data'][0]['max_tokens']
except FileNotFoundError:
    TEMPERATURE = 0.5
    MAX_TOKENS = 2048
    save_option()

# ChatGPT API 함수 : ChatGPT 응답을 return
def query_chatGPT(prompt):
    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
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




# ==========================================================
# 녹음

class MicrophoneStream(object):  # record stream을 chunk단위로 generator yielding 으로 생성

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            if not recording: # 녹음이 끝이 났을 때, 마지막 반복을 빠져나오기 위한 명령어
                return data

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

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


def complicated_record(): # Google STT 를 이용하여 Streaming 음성인식 처리
    language_code = "ko-KR"  # 한국어 코드

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        num_chars_printed = 0
        for response in responses:
            if not recording:
                sttprompt.put(transcript + overwrite_chars)
                break

            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript


            overwrite_chars = " " * (num_chars_printed - len(transcript))

            data = transcript + overwrite_chars

            if not result.is_final:
                streaming_queue.put(data)
                num_chars_printed = len(transcript)

            else:
                streaming_queue.put(data)
                num_chars_printed = 0




# ==========================================================
# Producer & Consumer

class Streaming(QThread):
    def __init__(self, streaming_que):
        super().__init__()
        self.streaming_que = streaming_que

    def run(self):
        while True:
            if not self.streaming_que.empty():
                data = self.streaming_que.get()
                #SignalManager().overlaySignals.answer_streaming.emit(data)

class Producer(QThread):
    def __init__(self, prompt_que, answer_que):
        super().__init__()
        self.prompt_que = prompt_que
        self.answer_que = answer_que
        self.overlaySignals = SignalManager().overlaySignals

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
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.APIError as e:
                    # Handle API error, e.g. retry or log
                    msg = f"OpenAI API returned an API Error: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.APIConnectionError as e:
                    # Handle connection error, e.g. check network or log
                    msg = f"OpenAI API request failed to connect: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.InvalidRequestError as e:
                    # Handle invalid request error, e.g. validate parameters or log
                    msg = f"OpenAI API request was invalid: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.AuthenticationError as e:
                    # Handle authentication error, e.g. check credentials or log
                    msg = f"OpenAI API request was not authorized: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.PermissionError as e:
                    # Handle permission error, e.g. check scope or log
                    msg = f"OpenAI API request was not permitted: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass
                except openai.error.RateLimitError as e:
                    # Handle rate limit error, e.g. wait or log
                    msg = f"OpenAI API request exceeded rate limit: {e}"
                    self.overlaySignals.throw_error.emit(msg)
                    pass


class Consumer(QThread):

    def __init__(self, answer_que):
        super().__init__()
        self.answer_que = answer_que

    def run(self):
        while True:
            if not self.answer_que.empty():
                data = self.answer_que.get()
                SignalManager().overlaySignals.message_arrived.emit(data)



class MyWindow(QObject):
    prompt_que = Queue()
    answer_que = Queue()
    audio_que = Queue()

    def __init__(self):
        super().__init__()
        # ====================================================
        #streaming google stt 사용으로 whisper 사용하지 않음
        #self.whisperWorker = WhisperWorker(MyWindow.audio_que, MyWindow.prompt_que)
        #self.whisperWorker.start()
        self.streaming = Streaming(streaming_queue)
        self.streaming.start()

        self.producer = Producer(MyWindow.prompt_que, MyWindow.answer_que)
        self.producer.start()

        self.consumer = Consumer(MyWindow.answer_que)
        self.consumer.start()

        # ====================================================
        self.keyboardSignals = KeyboardSignal
        self.overlaySignals = OverlaySignal

        self.readyToRecord = True
        self.recording = False

        self.initiateSignals()

    def initiateSignals(self):
        self.keyboardSignals = SignalManager().keyboardSignals
        self.overlaySignals = SignalManager().overlaySignals
        self.keyboardSignals.mic_key.connect(self.on_record)
        self.keyboardSignals.release_mic_key.connect(self.off_record)

        # better way?
        self.overlaySignals.message_arrived.connect(self.reset)
        self.overlaySignals.throw_error.connect(self.reset)

    # 레코드 시작 슬롯
    @pyqtSlot()
    def on_record(self):
        if self.readyToRecord:
            print('start record')
            start()
            self.readyToRecord = False
            self.recording = True
            self.overlaySignals.on_start_rec.emit()

    # 레코드 종료 & 위스퍼를 통해 stt
    @pyqtSlot()
    def off_record(self):
        if self.recording:
            self.recording = False
            print('stop record')
            stop()
            self.overlaySignals.start_prompt.emit()
            prompt = sttprompt.get()
            MyWindow.prompt_que.put(prompt)
            MyWindow.audio_que.put(0)
            self.overlaySignals.on_stop_rec.emit()

    @pyqtSlot()
    def stop(self):
        #self.whisperWorker.terminate()
        self.producer.terminate()
        self.consumer.terminate()
        self.streaming.terminate()

    @pyqtSlot()
    def reset(self):
        self.readyToRecord = True