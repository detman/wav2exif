# wav2exif

This script scans the SD card written by Fuji X cameras and searches for audio/voice recordings (.WAV files).

The wav is converted to (ascii) text, and the text is written as an exif description tag to the coresponding .JPG or .RAF file.

Very simple umlaut 2 ascii conversion is applied ( 'ö' -> 'oe' etc).

## installation (mac)

```bash
brew install portaudio 
python3 -m venv env
source env/bin/activate

pip install pyaudio
pip install SpeechRecognition
pip install exif
```
