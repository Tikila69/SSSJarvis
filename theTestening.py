import speech_recognition as sr
from gtts import gTTS
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Initialize ChatBot
chatbot = ChatBot("Assistant")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        return "I could not understand audio."
    except sr.RequestError as e:
        return "Could not request results; {0}".format(e)

def respond(text):
    response = chatbot.get_response(text)
    print(f"Response: {response}")
    tts = gTTS(text=str(response), lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")

def main():
    while True:
        query = listen_to_speech()
        if query:
            respond(query)

if __name__ == "__main__":
    main()