import speech_recognition as sr

# create recognizer and open the audio file
r = sr.Recognizer()
with sr.AudioFile("sample_output.wav") as source:
    audio = r.record(source)

# recognize speech using Google Speech Recognition
text = r.recognize_google(audio)

print(text)