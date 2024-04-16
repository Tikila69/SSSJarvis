import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import RPi.GPIO as GPIO
import requests
import json

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

def weatherChecker(when):
    data = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hønefoss,NO/'+when+'?key=LZXY8XB4SR6YC6RSFVVS952JG').json()


    description = data["days"][0]["description"]
    high = data["days"][0]["tempmax"]
    low = data["days"][0]["tempmin"]
    
    return description, high, low

def turn_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)


r = sr.Recognizer()


engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', "english")

GPIO.setmode(GPIO.BOARD)

red_pin = 5
green_pin = 3

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

turn_off(green_pin)
turn_off(red_pin)

cont = True



while cont:
    with sr.Microphone(device_index=2) as source:
        turn_off(red_pin)
        turn_on(green_pin)
        audio = r.listen(source)
        speech = r.recognize_google(audio)
        if "hey jarvis" in speech.lower():
            try:
                turn_off(green_pin)
                turn_on(red_pin)
                engine.say("Yes, sir?")
                turn_off(red_pin)
                turn_on(green_pin)
                engine.runAndWait()
                audio = r.listen(source)
                speech = r.recognize_google(audio)
                if "shut down" in speech.lower():
                    turn_off(green_pin)
                    turn_on(red_pin)
                    engine.say("Shutting down")
                    cont = False
                    turn_off(green_pin)
                    turn_off(red_pin)
                elif "weather" in speech.lower():
                    turn_off(green_pin)
                    turn_on(red_pin)
                    print("You said: " + speech)
                    try:
                        responseToday = weatherChecker("today")
                        responseTomorrow = weatherChecker("tomorrow")
                        engine.say("today it will be "+str(responseToday[0])+" with a high of "+str(round((responseToday[1]-32)/1.8,1))+" and a low of "+str(round((responseToday[2]-32)/1.8, 1))+". Tomorrow it will be "+str(responseTomorrow[0])+" with a high of "+str(round((responseTomorrow[1]-32)/1.8,1))+" and a low of "+str(round((responseTomorrow[2]-32)/1.8, 1)))
                        engine.runAndWait()
                    except sr.UnknownValueError:
                        print("Google Speech Recognition could not understand audio")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                else:
                    try:
                        turn_off(green_pin)
                        turn_on(red_pin)
                        speech = r.recognize_google(audio)
                        print("You said: " + speech)
                        #response = ask_openai(speech)
                        engine.say(str(response))
                        engine.runAndWait()
                    except sr.UnknownValueError:
                        engine.say("I am sorry, I could not understand what you said")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
