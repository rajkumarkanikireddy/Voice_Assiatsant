import pyaudio  # pip install pyaudio
import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install SpeechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib
import urllib.parse  # Used for YouTube search
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Define authorized user's voice password
AUTHORIZED_PASSWORD = "hello assistant"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am your assistant. Please tell me how may I help you.")

def takeCommand():
    """It takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # Adjusts to background noise
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

def verify_voice():
    """Unlocks the assistant using a predefined voice password"""
    speak("Please say the unlock password.")
    attempts = 3
    while attempts > 0:
        password_attempt = takeCommand()
        if password_attempt == AUTHORIZED_PASSWORD:
            speak("Access granAted. Welcome back!")
            return True
        else:
            attempts -= 1
            speak(f"Incorrect password. You have {attempts} attempts left.")
    
    speak("Too many failed attempts. Access denied.")
    return False

def play_youtube_video(query):
    """Search and play the first YouTube video based on the query"""
    query = query.replace("play", "").strip()
    search_query = urllib.parse.quote(query)
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    
    # Open search results first
    speak(f"Searching for {query} on YouTube.")
    webbrowser.open(youtube_url)
    time.sleep(2)
    
    # Open first video (optional)
    webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}&sp=EgIQAQ%3D%3D")

if __name__ == "__main__":
    if verify_voice():  # User must unlock with voice password
        wishMe()

        while True:
            query = takeCommand()

            # Wikipedia Search
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            # Open websites
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")

            elif 'open google' in query:
                webbrowser.open("google.com")

            elif 'open stackoverflow' in query:
                webbrowser.open("stackoverflow.com")

            # Play Music
            elif 'play music' in query:
                music_dir = 'C:\\Users\\rajkumar\\Music'  # Change this path
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No music files found in the directory.")

            # Time Query
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")

            # Open VS Code or any other application
            elif 'open code' in query:
                codePath = "C:\\Users\\rajkumar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                os.startfile(codePath)

            # Send Email
            elif 'email to me' in query:
                try:
                    speak("What should I say?")
                    content = takeCommand()
                    to = "Xyz@gmail.com"  # Change recipient email
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry, I was unable to send the email.")

            # YouTube Video Search & Play
            elif 'play' in query:
                play_youtube_video(query)

            #after this command, the assistant will stop working
            elif 'exit' in query or 'stop' in query:
                speak("Goodbye! Have a great day.")
                break