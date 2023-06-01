import json
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QThread, QObject
from signalManager import SignalManager

class Option_data(QObject):
    def __init__(self):
        super().__init__()
        self.init_option()
        self.init_signal()

    def init_signal(self):
        self.optionSignals = SignalManager().optionSignals
        self.optionSignals.current_parameter.connect(self.parameter_received)

    def init_option(self):
        try:
            with open("C:/Users/82105/PycharmProjects/team4/option.json", "r") as option_file:
                option_data = json.load(option_file)
                self.temperature = option_data['parameter'][0]['temperature']
                self.max_tokens = option_data['parameter'][0]['max_tokens']

                self.openai_api_key = option_data['api_key'][0]['openai_api_key']

                self.path = option_data['path'][0]['1']

                self.quit_key = option_data['key'][0]['quit_key']
                self.pressing_mic_key = option_data['key'][0]['pressing_mic_key']
                self.show_content_key = option_data['key'][0]['show_content_key']
                self.copy_key = option_data['key'][0]['copy_key']

                self.model = option_data['model'][0]['model']
        except FileNotFoundError:
            self.temperature = 0.5
            self.max_tokens = 2048

            self.path = ""

            self.openai_api_key = ""

            self.quit_key = ""
            self.pressing_mic_key = ""
            self.show_content_key = ""
            self.copy_key = ""

            self.model = "wikipedia"

            print("에옹")
            self.save_option()

    # parameter 값을 option.json에 저장
    def save_option(self):
        option = {}
        option['parameter'] = []
        option['parameter'].append({
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        })
        option['api_key'] = []
        option['api_key'].append({
            "openai_api_key": self.openai_api_key
        })

        option['path'] = []
        option['path'].append({
            1: self.path
        })

        option['key'] = []
        option['key'].append({
            "quit_key": self.quit_key,
            "pressing_mic_key": self.pressing_mic_key,
            "show_content_key": self.show_content_key,
            "copy_key": self.copy_key
        })
        option['model'] = []
        option['model'].append({
            "model": self.model
        })

        with open("C:/Users/82105/PycharmProjects/team4/option.json", 'w') as outfile:
            json.dump(option, outfile)

    @pyqtSlot(list)
    def parameter_received(self, para):
        self.temperature = para[0]
        print(self.temperature)
        self.max_tokens = para[1]

    def add_api(self, key : str, value : str):
        self.option_api = []
        self.option_api.append({
            key: value
        })



if __name__ == "__main__":
    option = Option_data()