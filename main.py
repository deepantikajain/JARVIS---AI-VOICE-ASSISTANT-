import speech_recognition as sr
import webbrowser
import requests
import pygame
import os

from gtts import gTTS
import musicLibrary
from ai import aiProcess

# Speech recognizer
recognizer = sr.Recognizer()

# News API key
newsapi = "23f69feb7cc842f19caee9365bd841a7"


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def processCommand(command):
    command = command.lower()
    print("command received:", command)
    # Open websites
    if "open" in command and "google" in command:
        speak("opening google")
        webbrowser.open("https://google.com")

    elif "open" in command and "youtube" in command:
        speak("opening youtube")
        webbrowser.open("https://youtube.com")

    elif "open" in command and "linkedin" in command:
        speak("opening linkedin")
        webbrowser.open("https://linkedin.com")

    # Play music
    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        link = musicLibrary.music.get(song)

        if link:
            webbrowser.open(link)
        else:
            speak("Song not found")

    # News
    elif "news" in command:
        response = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if len(articles) == 0:
                speak("Sorry, I could not find any news")
                return

            speak("Here are the top headlines")

            for article in articles[:5]:
                speak(article["title"])
        else:
            speak("News service is not available right now")

    # Anything else → AI
    else:
        answer = aiProcess(command)
        if answer.strip() == "":
            speak("i could not answer")
        else:
            speak(answer)


if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            # Listen for wake word
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2)
                word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes")

                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio)
                processCommand(command)

        except Exception as e:
            print("Error:", e)
