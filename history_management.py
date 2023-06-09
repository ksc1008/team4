import json
import time
import os

class History_manage(object):
    def __init__(self):
        os.makedirs("history", exist_ok=True)
        self.name_update()
    def name_update(self):
        now = time
        self.file_name = "history/history" + now.strftime('%Y%m%d-%H%M%S') + ".json"

    # QfileDialog로 부터 file_name을 입력받아 history를 저장
    def open_history(self, file_name):
        if file_name:
            with open(file_name, 'r') as f:
                data = json.load(f)
        return data

    def save_history(self, messages):
        self.name_update()
        if self.file_name:
            text = messages
            with open(self.file_name, 'w', encoding='UTF-8') as f:
                json.dump(text, f)


