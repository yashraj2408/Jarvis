import pyttsx3
import speech_recognition as sr
import eel
import time
import re
from gtts import gTTS
import playsound
import os
import tempfile

def speak(text, lang='en'):
    try:
        eel.DisplayMessage(text)
        eel.receiverText(text)

        if lang == 'en':
            # Initialize pyttsx3 in a platform-appropriate way. On Windows use 'sapi5',
            # on other platforms let pyttsx3 select the default driver.
            try:
                if os.name == 'nt':
                    engine = pyttsx3.init('sapi5')
                else:
                    engine = pyttsx3.init()

                voices = engine.getProperty('voices')
                # Prefer a male-sounding voice if available
                for voice in voices:
                    if "male" in voice.name.lower() or "david" in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                else:
                    if voices:
                        engine.setProperty('voice', voices[0].id)  # fallback

                engine.setProperty('rate', 160)  # slower, JARVIS-like
                engine.say(text)
                engine.runAndWait()
            except Exception as e:
                # Common failure on some platforms is missing comtypes dependency used by sapi5 driver.
                # Fall back to gTTS-based playback which works cross-platform but requires network.
                print(f"pyttsx3 TTS failed, falling back to gTTS: {e}")
                filename = os.path.join(tempfile.gettempdir(), "temp_voice_fallback.mp3")
                tts = gTTS(text=text, lang='en')
                tts.save(filename)
                playsound.playsound(filename)
                time.sleep(0.5)
                try:
                    os.remove(filename)
                except Exception:
                    pass

        else:
            filename = "temp_voice.mp3"
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)
            playsound.playsound(filename)
            time.sleep(1)
            os.remove(filename)

    except Exception as e:
        print(f"Error in speak(): {e}")

def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
        elif "translate" in query:
            from engine.features import translate_text

            # Extract text and language
            try:
                match = re.search(r'translate\s+"?(.+?)"?\s+to\s+(\w+)', query)
                if match:
                    sentence = match.group(1)
                    language = match.group(2).lower()

                    # Map language name to language code
                    language_codes = {
                        'hindi': 'hi',
                        'spanish': 'es',
                        'french': 'fr',
                        'german': 'de',
                        'telugu': 'te',
                        'tamil': 'ta',
                        'korean': 'ko',
                        'japanese': 'ja',
                        'english': 'en'
                        # Add more if needed
                    }

                    if language in language_codes:
                        translated_text = translate_text(sentence, language_codes[language])
                        speak(translated_text, lang=language_codes[language])
                        eel.DisplayMessage(f"Translated: {translated_text}")

                    else:
                        speak("Sorry, I don't support that language yet.")
                else:
                    speak("Please say the sentence clearly like 'translate how are you to hindi'")
            except Exception as e:
                print(f"Translation Parsing Error: {e}")
                speak("Something went wrong in translation")

        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")
    
    eel.ShowHood()