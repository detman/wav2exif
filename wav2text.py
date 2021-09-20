import speech_recognition as sr
import sys
import os

def audio2text(audio):
    """
    get audio as text
    EXIF image description is ascii based, we have to replace umlauts and convert to ascii
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio = r.listen(source)

    text = r.recognize_google(audio, language="de_DE.utf8")
    print(f'fetched {file}: {text}')
    return text

def updateExif(file,text):
    os.system(f'exiftool -ImageDescription="{text}" {file}')


if len(sys.argv) == 1:
    cmd = sys.argv[0]
    print(f'usage {cmd} dir|file')
else:
    file = sys.argv[1]
    audios = []
    if os.path.isdir(file):
        if not file.endswith('/'):
            file += '/'

        audios.extend( [ file + f for f in os.listdir(file) if f.endswith('.WAV')])
    else:
        audios.append(file)

    """
    loop over all WAV files
    """
    for audio in audios:
        if not os.path.exists(audio):
            print(f'file not found: {audio}')
            continue

        # find all related images (JPG und RAF)
        image_files = []

        for ext in ('.RAF','.JPG'):
            file = os.path.splitext(audio)[0]+ext
            if os.path.exists(file):
                image_files.append(file)

        if not image_files:
            print(f'.. no picture found for audio')
            continue

        text = audio2text(audio)

        for file in image_files:
            updateExif(file,text)
