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

    def init_option(self):
        try:
            with open("option.json", "r") as option_file:
                option_data = json.load(option_file)
                self.data = option_data
                self.temperature = option_data['parameter'][0]['temperature']
                self.max_tokens = option_data['parameter'][0]['max_tokens']

                self.openai_api_key = option_data['api_key'][0]['openai_api_key']

                self.path = option_data['path']

                self.quit_key = option_data['key'][0]['quit_key']
                self.pressing_mic_key = option_data['key'][0]['pressing_mic_key']
                self.show_content_key = option_data['key'][0]['show_content_key']
                self.copy_key = option_data['key'][0]['copy_key']
                self.quit_key_combination = option_data['key'][0]['quit_key_combination']
                self.pressing_mic_key_combination = option_data['key'][0]['pressing_mic_key_combination']
                self.show_content_key_combination = option_data['key'][0]['show_content_key_combination']
                self.copy_key_combination = option_data['key'][0]['copy_key_combination']

                self.wikipedia = option_data['model'][0]['wikipedia']
                self.googlesearch = option_data['model'][0]['googlesearch']
                self.local = option_data['model'][0]['local']
        except FileNotFoundError:
            self.temperature = 0.5
            self.max_tokens = 2048

            self.path = ""

            self.openai_api_key = ""

            self.quit_key = ""
            self.quit_key_combination = ""
            self.pressing_mic_key = ""
            self.pressing_mic_key_combination = ""
            self.show_content_key = ""
            self.show_content_key_combination = ""
            self.copy_key = ""
            self.copy_key_combination = ""

            self.wikipedia = False
            self.googlesearch = False
            self.local = False

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

        option['path'] = self.path

        option['key'] = []
        option['key'].append({
            "quit_key": self.quit_key,
            "quit_key_combination" : self.quit_key_combination,
            "pressing_mic_key": self.pressing_mic_key,
            "pressing_mic_key_combination": self.pressing_mic_key_combination,
            "show_content_key": self.show_content_key,
            "show_content_key_combination": self.show_content_key_combination,
            "copy_key": self.copy_key,
            "copy_key_combination": self.copy_key_combination
        })
        option['model'] = []
        option['model'].append({
            "wikipedia": self.wikipedia,
            "googlesearch": self.googlesearch,
            "local": self.local
        })

        with open("option.json", 'w') as outfile:
            json.dump(option, outfile)

    def add_api(self, key : str, value : str):
        self.option_api = []
        self.option_api.append({
            key: value
        })

    def load_option(self):
        try:
            with open("option.json", "r") as option_file:
                option_data = json.load(option_file)
                self.temperature = option_data['parameter'][0]['temperature']
                self.max_tokens = option_data['parameter'][0]['max_tokens']

                self.openai_api_key = option_data['api_key'][0]['openai_api_key']

                self.path = option_data['path']

                self.quit_key = option_data['key'][0]['quit_key']
                self.pressing_mic_key = option_data['key'][0]['pressing_mic_key']
                self.show_content_key = option_data['key'][0]['show_content_key']
                self.copy_key = option_data['key'][0]['copy_key']
                self.quit_key_combination = option_data['key'][0]['quit_key_combination']
                self.pressing_mic_key_combination = option_data['key'][0]['pressing_mic_key_combination']
                self.show_content_key_combination = option_data['key'][0]['show_content_key_combination']
                self.copy_key_combination = option_data['key'][0]['copy_key_combination']

                self.model = option_data['model'][0]['model']
        except FileNotFoundError:
            self.temperature = 0.5
            self.max_tokens = 2048

            self.path = ""

            self.openai_api_key = ""

            self.quit_key = ""
            self.quit_key_combination = ""
            self.pressing_mic_key = ""
            self.pressing_mic_key_combination = ""
            self.show_content_key = ""
            self.show_content_key_combination = ""
            self.copy_key = ""
            self.copy_key_combination = ""

            self.wikipedia = False
            self.googlesearch = False
            self.local = False

            self.save_option()

if __name__ == "__main__":
    option = Option_data()