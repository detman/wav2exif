import speech_recognition as sr
import sys
import os
from exif import Image
from unidecode import unidecode

def remove_umlaut(string):
    # https://gist.github.com/johnberroa/cd49976220933a2c881e89b69699f2f7
    """
    Removes umlauts from strings and replaces them with the letter+e convention
    :param string: string to remove umlauts from
    :return: unumlauted string
    """
    u = 'ü'.encode()
    U = 'Ü'.encode()
    a = 'ä'.encode()
    A = 'Ä'.encode()
    o = 'ö'.encode()
    O = 'Ö'.encode()
    ss = 'ß'.encode()

    string = string.encode()
    string = string.replace(u, b'ue')
    string = string.replace(U, b'Ue')
    string = string.replace(a, b'ae')
    string = string.replace(A, b'Ae')
    string = string.replace(o, b'oe')
    string = string.replace(O, b'Oe')
    string = string.replace(ss, b'ss')

    string = string.decode('utf-8')
    return string

def audio2text(audio):
    """
    get audio as text
    EXIF image description is ascii based, we have to replace umlauts and convert to ascii
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio) as source:
        audio = r.listen(source)

    text = r.recognize_google(audio, language="de_DE.utf8")
    text = remove_umlaut(text)
    ascii = text.encode('ascii','ignore').decode('utf-8')
    return text,ascii


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

        text,ascii = None,None

        for file in image_files:
            image = Image(file)
            
            # only set description if not set
            if not hasattr(image,'image_description'):

                if not text:
                    text,ascii = audio2text(audio)

                image.image_description = ascii
                image.user_comment = text
                with open(file, 'wb') as updated_file:
                    print(f'.. update {file}: "{ascii}"')
                    updated_file.write(image.get_file())
                    updated_file.close()
