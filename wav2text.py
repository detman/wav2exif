import speech_recognition as sr
import sys
import os
from exif import Image

r = sr.Recognizer()

if len(sys.argv) == 1:
    cmd = sys.argv[0]
    print(f'usage {cmd} dir|file')
else:
    file = sys.argv[1]
    audios = []
    if os.path.isdir(file):
        audios.extend( [ file + f for f in os.listdir(file) if f.endswith('.WAV')])
    else:
        audios.append(file)

    for audio in audios:
        if not os.path.exists(audio):
            print(f'file not found: {audio}')
            continue

        print(f'audio {audio}')
        image_files = []

        for ext in ('.RAF','.JPG'):
            file = os.path.splitext(audio)[0]+ext
            if os.path.exists(file):
                image_files.append(file)

        if not image_files:
            print(f'.. no picture found for audio')
            continue

        with sr.AudioFile(audio) as source:
            audio = r.listen(source)
        text = r.recognize_google(audio, language="de_DE")
        print(f'.. speech2text: "{text}"')

        for file in image_files:
            image = Image(file)
            image.image_description = text
            with open(file, 'wb') as updated_file:
                print(f'.. update exif data of {file}')
                updated_file.write(image.get_file())
                updated_file.close()
