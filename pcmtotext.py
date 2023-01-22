import speech_recognition as sr

def speechToText(output):
    # create recognizer and open the audio file
    print(type(output))
    r = sr.Recognizer()
    with sr.AudioFile(output) as source:
        audio = r.record(source)

    # recognize speech using Google Speech Recognition
    text = r.recognize_google(audio)

    print(text)

    return text
# fileName="sample_output.wav"
# speechToText(fileName)