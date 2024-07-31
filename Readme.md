# Speech-to-Text Tray Application

This application listens for a keyword to activate speech recognition and outputs the recognized text to the active window. It runs in the system tray on Windows.

## Features

- Keyword detection to start speech recognition
- Continuous speech recognition using Azure Cognitive Services
- Outputs text to the active window
- Runs in the system tray with options to restart or quit

## Requirements

- Python 3.x
- PyQt5
- PyAutoGUI
- SpeechRecognition
- azure-cognitiveservices-speech

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/nullbytenomad/speech-to-text-tray-app.git
   cd speech-to-text-tray-app
