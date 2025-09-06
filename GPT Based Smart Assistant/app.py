import os
import speech_recognition as sr
import pyttsx3
import webbrowser
from openai import OpenAI
import apikey  # Your file holding API_KEY

# -------------------------
# Set API key safely in environment
# -------------------------
os.environ["OPENAI_API_KEY"] = apikey.API_KEY
client = OpenAI()  # Automatically picks up from environment
Model = "gpt-4o"

# -------------------------
# GPT Reply function
# -------------------------
def Reply(question):
    completion = client.chat.completions.create(
        model=Model,
        messages=[
            {'role': "system", "content": "You are a helpful assistant, capable of responding in both English and Tamil."},
            {'role': 'user', 'content': question}
        ],
        max_tokens=200
    )
    answer = completion.choices[0].message.content
    return answer

# -------------------------
# Text-to-speech setup
# -------------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------------
# Speech-to-text
# -------------------------
def takeCommand(language='en-in'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f'Listening ({language}).......')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print('Recognizing....')
        query = r.recognize_google(audio, language=language)
        print(f"User Said: {query} \n")
        return query
    except Exception as e:
        print("Say that again.....")
        return "None"

# -------------------------
# Main program
# -------------------------
if __name__ == '__main__':
    language_mode = 'en-in'  # Default language

    print("Voice Assistant Started (Say 'switch to Tamil' or 'தமிழுக்கு மாறு' to change language)")
    speak("Voice Assistant Started. You can speak in English or Tamil")

    while True:
        query = takeCommand(language_mode).lower()

        if query == "none" and language_mode == 'en-in':
            query = takeCommand('ta-IN').lower()
        elif query == "none" and language_mode == 'ta-IN':
            query = takeCommand('en-in').lower()

        if query == "none":
            continue

        # Language switching commands
        if "switch to tamil" in query or "தமிழுக்கு மாறு" in query:
            language_mode = 'ta-IN'
            speak("Switched to Tamil mode. தமிழ் பயன்முறைக்கு மாறியுள்ளது.")
            continue

        if "switch to english" in query or "ஆங்கிலத்திற்கு மாறு" in query:
            language_mode = 'en-in'
            speak("Switched to English mode")
            continue

        # Process command with GPT-4
        ans = Reply(query)
        print(ans)
        speak(ans)

        # Browser-related tasks
        if "open youtube" in query or "யூடியூப் திற" in query:
            webbrowser.open('https://www.youtube.com')

        if "open google" in query or "கூகிள் திற" in query:
            webbrowser.open('https://www.google.com')

        if "bye" in query or "விடைபெறுகிறேன்" in query:
            speak("Goodbye! நன்றி, மீண்டும் சந்திப்போம்!")
            break
