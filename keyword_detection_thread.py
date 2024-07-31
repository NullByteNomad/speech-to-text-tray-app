import speech_recognition as sr
from PyQt5.QtCore import QThread, pyqtSignal

class KeywordDetectionThread(QThread):
    keyword_detected = pyqtSignal()

    def __init__(self, keyword="activate"):
        super().__init__()
        self.keyword = keyword
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def run(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

        while True:
            with self.mic as source:
                audio = self.recognizer.listen(source)
            try:
                recognized_text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {recognized_text}")
                if self.keyword.lower() in recognized_text.lower():
                    self.keyword_detected.emit()
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")