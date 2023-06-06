import json
import time

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant who is good at detailing."
    }
]

messages.append({"role": "user", "content": "prompt"})

class History_manage(object):
    def __init__(self):
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

if __name__ == "__main__":
    history_manage = History_manage()
    history_manage.save_history(messages)
    his = history_manage.open_history(history_manage.file_name)
    i=1
    while True:
        try:
            print(his[i]['content'])
            i = i+1
        except IndexError:
            break

