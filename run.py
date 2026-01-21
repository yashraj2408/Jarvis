 

import multiprocessing
import subprocess
import os

# To run Jarvis
def startJarvis():
        # Code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# To run hotword
def listenHotword():
        # Code for process 2
        print("Process 2 is running.")
        # Only attempt hotword if access key is configured
        access_key = os.getenv("PICOVOICE_ACCESS_KEY") or os.getenv("PV_ACCESS_KEY")
        if not access_key or access_key == "YOUR_PICOVOICE_ACCESS_KEY":
            print("Skipping hotword process: PICOVOICE_ACCESS_KEY not set or still placeholder.")
            return
        from engine.features import hotword
        try:
            hotword()
        except Exception as e:
            print("Hotword process exited with error:", e)


    # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join()

        # If hotword process is still running, terminate it cleanly
        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")