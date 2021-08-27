# wav2exif

This script scans the SD card written by Fuji X cameras and searches for audio recordings (.WAV files).

The wav is converted to text, and the text is written as an exif description tag to the coresponding .JPG or .RAF file

## installation (mac)

  brew install portaudio 
  python3 -m venv env
  source env/bin/activate

  pip install pyaudio
  pip install SpeechRecognition
  pip install exif
