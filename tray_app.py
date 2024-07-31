import sys
import os
import subprocess
import pyautogui
from PyQt5 import QtWidgets, QtGui
from speech_recognition_thread import SpeechRecognitionThread
from keyword_detection_thread import KeywordDetectionThread
from config import SPEECH_KEY, SERVICE_REGION, KEYWORD
import logging
from PyQt5.QtWidgets import QMessageBox

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        svg_icon_path = os.path.join(os.path.dirname(__file__), 'imgMic-button.chunk.svg')
        png_icon_path = os.path.join(os.path.dirname(__file__), 'microphone.png')

        if os.path.exists(svg_icon_path):
            self.setIcon(QtGui.QIcon(svg_icon_path))
        elif os.path.exists(png_icon_path):
            self.setIcon(QtGui.QIcon(png_icon_path))
        else:
            print("Icon file not found.")

        self.setToolTip("Speech-to-Text")

        self.menu = QtWidgets.QMenu(parent)
        self.restart_action = self.menu.addAction("Restart Application")
        self.restart_action.triggered.connect(self.restart_application)
        self.quit_action = self.menu.addAction("Quit")
        self.quit_action.triggered.connect(QtWidgets.qApp.quit)

        self.setContextMenu(self.menu)

        self.speech_thread = None
        self.keyword_thread = KeywordDetectionThread(KEYWORD)
        self.keyword_thread.keyword_detected.connect(self.start_transcription)
        self.keyword_thread.start()

        self.activated.connect(self.on_tray_activated)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def on_tray_activated(self, reason):
        if reason == self.Trigger:
            self.show_message("Tray Application", "Application is running")

    def restart_application(self):
        try:
            script_path = os.path.abspath(__file__)
            subprocess.Popen(['python', script_path], shell=True)
            QtWidgets.qApp.quit()
        except Exception as e:
            logging.error(f"Failed to restart application: {e}")
            QMessageBox.critical(None, "Error", f"Failed to restart application: {e}")

    def start_transcription(self):
        try:
            if self.speech_thread:
                self.speech_thread.stop()
                self.speech_thread.wait()

            self.speech_thread = SpeechRecognitionThread(SPEECH_KEY, SERVICE_REGION)
            self.speech_thread.recognized.connect(self.handle_recognition)
            self.speech_thread.start()
        except Exception as e:
            logging.error(f"Failed to start transcription: {e}")
            QMessageBox.critical(None, "Error", f"Failed to start transcription: {e}")

    def handle_recognition(self, text):
        try:
            window = pyautogui.getActiveWindow()
            if window:
                window.activate()  # Bring the intended window to the foreground
            pyautogui.typewrite(text)
        except Exception as e:
            logging.error(f"Failed to handle recognition: {e}")
            QMessageBox.critical(None, "Error", f"Failed to handle recognition: {e}")

    def show_message(self, title, message):
        self.showMessage(title, message, QtGui.QIcon(), 3000)

def main():
    app = QtWidgets.QApplication(sys.argv)
    tray = TrayApp()
    tray.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
