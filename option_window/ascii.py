import csv

# keyboard에서 입력된 key값을 ascii code로 변환하는 class
class Keyboard_ascii():
    def __init__(self):
        mydict = {}
        with open('option_window/asciidict.csv', mode='r') as file:
            reader = csv.reader(file)
            self.result = dict()
            for row in reader:
                self.result[row[0]] = row[1]


    def keytoascii(self, key: str):
        return int(self.result[key.lower()])

    def combination_ascii(self, comb: str):
        if comb == "Ctrl":
            return 0x11
        elif comb == "Shift":
            return 0x10
        elif comb == "Alt":
            return 0x12
        else:
            return -1