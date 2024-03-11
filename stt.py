import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import weatherChecker

def ask_openai(question):
    response = ""
    client = OpenAI(api_key="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")
    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
    stream=True,
    )
    for chunk in stream:
        response+=chunk.choices[0].delta.content or ""

    return response

# obtain audio from the microphone
r = sr.Recognizer()

# convert text to speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

cont = True

# continuously listen for "hey jarvis"
while cont:
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        speech = r.recognize_google(audio)
        if "hey jarvis" in speech.lower():
            try:
                engine.say("Yes, sir?")
                print("Yes, sir?")
                engine.runAndWait()
                audio = r.listen(source)
                speech = r.recognize_google(audio)
                if "shut down" in speech.lower():
                    cont = False

                elif "weather" in speech.lower():
                    print("You said: " + speech)
                    try:
                        responseToday = weatherChecker.weatherChecker("today")
                        responseTomorrow = weatherChecker.weatherChecker("tomorrow")
                        engine.say("today it will be "+str(responseToday[0])+" with a high of "+str(round((responseToday[1]-32)/1.8,1))+" and a low of "+str(round((responseToday[2]-32)/1.8, 1))+". Tomorrow it will be "+str(responseTomorrow[0])+" with a high of "+str(round((responseTomorrow[1]-32)/1.8,1))+" and a low of "+str(round((responseTomorrow[2]-32)/1.8, 1)))
                        engine.runAndWait()
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                else:
                    try:
                        speech = r.recognize_google(audio)
                        print("You said: " + speech)
                        #response = ask_openai(speech)
                        print("Response: ", response)
                        engine.say(str(response))
                        engine.runAndWait()
                    except sr.UnknownValueError:
                        engine.say("I am sorry, I could not understand what you said")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))