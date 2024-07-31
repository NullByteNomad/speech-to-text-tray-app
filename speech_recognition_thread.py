import azure.cognitiveservices.speech as speechsdk
from PyQt5.QtCore import QThread, pyqtSignal

class SpeechRecognitionThread(QThread):
    recognized = pyqtSignal(str)

    def __init__(self, speech_key, service_region):
        super().__init__()
        self.speech_key = speech_key
        self.service_region = service_region
        self.recognizer = None
        self.running = False

    def run(self):
        try:
            speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
            speech_config.speech_recognition_language = "en-US"
            speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EnableAudioLogging, "true")
            speech_config.set_property(speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption, "TrueText")

            audio_input = speechsdk.AudioConfig(use_default_microphone=True)
            self.recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

            def recognized_cb(evt):
                self.recognized.emit(evt.result.text)

            self.recognizer.recognized.connect(recognized_cb)

            self.running = True
            self.recognizer.start_continuous_recognition()
            while self.running:
                self.msleep(100)
            self.recognizer.stop_continuous_recognition()
        except Exception as e:
            print(f"Speech recognition error: {e}")

    def stop(self):
        self.running = False