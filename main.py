import os
import sys
import eel

from engine.features import *
from engine.command import *
from engine.auth import recoganize
def start():
    
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        # Only run device.bat on Windows; on other systems the command won't exist.
        if os.name == 'nt':
            subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")
    # Open the app URL in a platform-appropriate way instead of using Windows-only start
    try:
        url = "http://localhost:8000/index.html"
        if sys.platform == 'darwin':
            subprocess.Popen(["open", url])
        elif os.name == 'nt':
            # Use start via shell on Windows
            subprocess.Popen(f'start msedge.exe --app="{url}"', shell=True)
        else:
            # Linux and others: try xdg-open or fallback to webbrowser
            try:
                subprocess.Popen(["xdg-open", url])
            except Exception:
                import webbrowser
                webbrowser.open(url)
    except Exception as e:
        print("Unable to open browser automatically:", e)

    eel.start('index.html', mode=None, host='localhost', block=True)