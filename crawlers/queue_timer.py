import threading
import os
from dotenv import load_dotenv

load_dotenv()

TIMEOUT = int(os.getenv('TIMEOUT', 0))

timer = None

def reset_timer(callback):
    global timer
    if timer:
        timer.cancel()
    timer = threading.Timer(TIMEOUT, callback)
    timer.start()