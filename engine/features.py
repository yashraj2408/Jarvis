import os
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser

import eel
import pyaudio
import pyautogui
import pywhatkit as kit
import pvporcupine
from urllib.parse import quote
from playsound import playsound
from googletrans import Translator
from hugchat import hugchat

from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term, remove_words

# -------------------------------------------------
# Database connection
# -------------------------------------------------
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# -------------------------------------------------
# Assistant start sound
# -------------------------------------------------
@eel.expose
def playAssistantSound():
    music_dir = os.path.join("www", "assets", "audio", "start_sound.mp3")
    if os.path.exists(music_dir):
        playsound(music_dir)

# -------------------------------------------------
# Open apps / websites (macOS)
# -------------------------------------------------
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()
    if not query:
        return

    try:
        # Check system commands from database
        cursor.execute("SELECT path FROM sys_command WHERE name = ?", (query,))
        result = cursor.fetchone()
        if result:
            speak(f"Opening {query}")
            subprocess.run(["open", result[0]])
            return

        # Check web commands from database
        cursor.execute("SELECT url FROM web_command WHERE name = ?", (query,))
        result = cursor.fetchone()
        if result:
            speak(f"Opening {query}")
            webbrowser.open(result[0])
            return

        # Try opening app by name
        speak(f"Opening {query}")
        subprocess.run(["open", "-a", query])

    except Exception as e:
        speak("Something went wrong")
        print(e)

# -------------------------------------------------
# Play YouTube
# -------------------------------------------------
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak(f"Playing {search_term} on YouTube")
    kit.playonyt(search_term)

# -------------------------------------------------
# Hotword detection (Jarvis / Alexa)
# -------------------------------------------------
def hotword():
    """
    Listens for hotwords using Picovoice Porcupine.
    Reads access key from environment variable PICOVOICE_ACCESS_KEY.
    """
    ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY") or os.getenv("PV_ACCESS_KEY")
    if not ACCESS_KEY or ACCESS_KEY == "YOUR_PICOVOICE_ACCESS_KEY":
        raise RuntimeError(
            "Picovoice AccessKey is not set. Set PICOVOICE_ACCESS_KEY in your environment."
        )

    porcupine = None
    paud = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keywords=["jarvis", "alexa"]
        )
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotwords...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Hotword detected!")
                pyautogui.keyDown("command")
                pyautogui.press("j")
                pyautogui.keyUp("command")
                time.sleep(2)

    except Exception as e:
        print("Error in hotword detection:", e)

    finally:
        if porcupine:
            try:
                porcupine.delete()
            except Exception:
                pass
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()

# -------------------------------------------------
# Find contact
# -------------------------------------------------
def findContact(query):
    words_to_remove = [
        ASSISTANT_NAME, "make", "a", "to", "phone",
        "call", "send", "message", "whatsapp", "video"
    ]
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ?",
            ('%' + query + '%',)
        )
        result = cursor.fetchone()
        if result:
            mobile = str(result[0])
            if not mobile.startswith("+91"):
                mobile = "+91" + mobile
            return mobile, query

        raise Exception("Contact not found")

    except:
        speak("Contact not found")
        return 0, 0

# -------------------------------------------------
# WhatsApp message / call (macOS)
# -------------------------------------------------
def whatsApp(mobile_no, message, flag, name):
    encoded_message = quote(message)
    if flag == "message":
        url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        subprocess.run(["open", url])
        time.sleep(5)
        pyautogui.press("enter")
        speak(f"Message sent to {name}")
    elif flag in ["call", "video call"]:
        url = f"whatsapp://send?phone={mobile_no}"
        subprocess.run(["open", url])
        speak(f"Opening WhatsApp chat with {name}")

# -------------------------------------------------
# Chatbot (HugChat)
# -------------------------------------------------
def chatBot(query):
    chatbot = hugchat.ChatBot(
        cookie_path=os.path.join("engine", "cookies.json")
    )
    cid = chatbot.new_conversation()
    chatbot.change_conversation(cid)
    response = chatbot.chat(query)
    speak(response)
    return response

# -------------------------------------------------
# Translate text
# -------------------------------------------------
def translate_text(text, target_language):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_language)
        speak(f"The translation is {translated.text}")
        return translated.text
    except Exception as e:
        speak("Translation failed")
        print(e)
        return ""
