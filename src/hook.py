import atexit
import signal
import sys

_triggered = False

def _goodbye():
    global _triggered
    if _triggered:
        return
    _triggered = True
    print("\n[focuslog] Program is shutting down.")

# Runs on normal interpreter shutdown
atexit.register(_goodbye)


def _signal_handler(signum, frame):
    _goodbye()
    sys.exit(0)

signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)