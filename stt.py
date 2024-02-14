import os
import speech_recognition as sr
import pyttsx3
import openai


def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # You can change the model if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
        ],
    )
    return response.choices[0].message['content']

# obtain audio from the microphone
r = sr.Recognizer()

# convert text to speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# continuously listen for "hey jarvis"
while True:
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            speech = r.recognize_google(audio)
            if "hey jarvis" in speech.lower():
                print("I am listening...")
                audio = r.listen(source)
                
                try:
                    print("You said: " + r.recognize_google(audio))
                    engine.say("You said: " + r.recognize_google(audio))
                    engine.runAndWait()
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))