import speech_recognition as sr
from openai import OpenAI

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")
        return speech_text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def ask_openai(question):
    client = OpenAI(api_key="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")


    stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
    stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

def main():
    speech_text = listen_to_speech()
    if speech_text:
        ask_openai(speech_text)

if __name__ == "__main__":
    main()