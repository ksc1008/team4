from pyfiglet import Figlet
import os
import sys
import openai
from datetime import datetime

from multiprocessing import Process, Queue, freeze_support

from PySide6.QtCore import Signal, Slot, Qt, QTimer, QThread
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon

from design.ui_001_myGPT import Ui_MainWindow
from animation import Sticker
from shortcut import ShorCut


openai.api_key = os.getenv("OPENAI_API_KEY")
#print(os.getenv("OPENAI_API_KEY"))
# Banner: "ChatGPT turbo GO"
text = Figlet(font="banner", width=120)
print(text.renderText("ChatGPT turbo Go"))


# Sends a prompt to openai, and returns messages received.
def query_chatGPT(prompt):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]


# Producer thread
# 1. When a message appears in `prompt_que`, query to openai.
# 2. When receive a reply, deliver it through `answer_que`.
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


# Consumer thread
# 1. Sends two signals while waiting for a reply from the Producer thread.
class Consumer(QThread):
    message_arrived = Signal(str)
    message_waiting = Signal(int)

    def __init__(self, answer_que):
        super().__init__()
        self.answer_que    = answer_que
        self.waiting_count = 0

    def run(self):
        while True:
            if not self.answer_que.empty():
                data = self.answer_que.get()
                self.message_arrived.emit(data)
                self.waiting_count = 0
            else:
                self.message_waiting.emit(self.waiting_count)
                self.waiting_count += 1

# GUI
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.second = None
        self.setupUi(self)
        self.width = 920
        self.height = 820
        self.left = 50
        self.top = 50
        flags = Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.waiting_count = 0
        self.submit_click_OK = False
        self.answer_arrived = False
        self.wait_a_moment = ""
        self.icon_position = 0
        self.process_icon = "😒 😥 😥 😲 😲 😲 😊 😊 😊 😊 🤣 🤣 🤣 🤣 😂 😂 😂 😂 😂 ❤️".split()

        # timer
        self.timer = QTimer()
        self.timer.setInterval(1_000)  # 1 sec
        self.timer.start()

        # Consumer thread
        self.consumer = Consumer(answer_que)
        self.consumer.start()

        # Producer thread
        self.producer = Producer(prompt_que, answer_que)
        self.producer.start()

        self.setWindowTitle("ChatGPT API tutorial")
        self.setWindowIcon(QIcon("image/ChatGPT.png"))

        # Shortcut
        self.shortcut = ShorCut()
        self.shortcut.start()

        # Signal
        self.shortcut.main_to_second.connect(self.shortcut_main_to_second)
        self.shortcut.second_to_main.connect(self.shortcut_second_to_main)
        self.shortcut.exit_key.connect(self.shortcut_exit_key)

        self.btn_submit.clicked.connect(self.on_btn_submit)
        self.btn_clear.clicked.connect(self.on_btn_clear)
        self.btn_exit.clicked.connect(self.on_btn_exit)

        self.timer.timeout.connect(self.on_display_current_time)

        self.consumer.message_arrived.connect(self.on_message_arrived)
        self.consumer.message_waiting.connect(self.on_message_waiting)

    # Slot
    @Slot()
    def on_btn_submit(self):
        question = self.text_prompt.toPlainText()
        decorate = question
        decorate = f"❓<font color='deeppink'>>: </font><font color='maroon'><strong>{decorate}</strong></font>"

        if len(question):
            prompt_que.put(question)
            self.text_answer.append(decorate)
            self.submit_click_OK = True
            self.answer_arrived = False
            self.wait_a_moment = ""
            self.icon_position = 0
            self.label_status.clear()
        else:
            self.submit_click_OK = False
            self.answer_arrived = False
            self.label_status.clear()
            self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_status.setText("질의(prompt)가 없습니다. 질의를 입력하여 주세요.")

    @Slot()
    def on_btn_clear(self):
        self.submit_click_OK = False
        self.answer_arrived = False
        self.wait_a_moment = ""
        self.icon_position = 0
        self.label_status.clear()
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setText("질의(prompt)가 없습니다. 질의를 입력하여 주세요.")
        self.text_prompt.clear()

    @Slot()
    def on_btn_exit(self):
        try:
            sys.exit(0)
        except SystemExit as e:
            self.close()
            print(f"on exit clocked...[{e}")

    @Slot()
    def on_display_current_time(self):
        time = datetime.now()
        self.lcd_clock.display(f"{time:%H:%M:%S}")

    @Slot(str)
    def on_message_arrived(self, data):
        self.answer_arrived = True
        decorate = f"😎>: {data}"
        self.text_answer.append(decorate)
        self.text_answer.ensureCursorVisible()

    @Slot(int)
    def on_message_waiting(self, value):
        if self.submit_click_OK and not self.answer_arrived:
            if (value % 20_000) == 1:  # 2초마다 이모지 표시
                self.wait_a_moment += self.process_icon[self.icon_position % 20]
                self.icon_position += 1
                self.label_status.setText(self.wait_a_moment)
            else:
                pass

    @Slot()
    def shortcut_main_to_second(self):
        self.hide()
        self.second = Sticker('gif/mint.gif', xy=[50, 50], size=0.2, on_top=True)
        # second가 존재하고 보이는 동안 이벤트 루프 실행
        while self.second is not None and self.second.isVisible():
            app.processEvents()

    @Slot()
    def shortcut_second_to_main(self):
        self.second.close()
        self.show()

    @Slot()
    def shortcut_exit_key(self):
        self.shortcut.stop()
        try:
            self.second.close()
            self.close()
        except AttributeError:
            pass
        self.close()



if __name__ == '__main__':
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

    # exit
    try:
        sys.exit(app.exec())
    except SystemExit:
        win.consumer.terminate()
        win.producer.terminate()
        win.timer.stop()
        win.shortcut.stop()
        win.shortcut.terminate()
        win.close()
