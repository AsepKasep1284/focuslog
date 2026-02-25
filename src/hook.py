from __future__ import annotations
import atexit
import signal
import sys
import threading
import weakref
from typing import Set

# registry holds weak references to Session objects so they can be GC'd normally
_registry_lock = threading.Lock()
_registry: "weakref.WeakSet" = weakref.WeakSet()
_printed = False
_printed_lock = threading.Lock()

def register(session) -> None:
    """Register a session to be included in the exit summary."""
    with _registry_lock:
        _registry.add(session)

def unregister(session) -> None:
    with _registry_lock:
        try:
            _registry.discard(session)
        except Exception:
            pass

def _collect_sessions() -> Set:
    with _registry_lock:
        return set(_registry)

def _print_summary_once() -> None:
    """
    Print summary of registered sessions once. This guards against multiple prints
    when multiple signals / atexit are called.
    """
    global _printed
    with _printed_lock:
        if _printed:
            return
        _printed = True

    sessions = _collect_sessions()
    if not sessions:
        return

    print("\n[focuslog] Sessions summary:")
    for s in sessions:
        try:
            # call the object's summary() method if present
            summary = getattr(s, "summary", None)
            if callable(summary):
                print("  -", summary())
            else:
                # fallback
                print("  -", repr(s))
        except Exception as ex:
            # be defensive: don't crash host process
            print("  - (error reading session)", ex)

def _atexit_handler() -> None:
    _print_summary_once()

def _signal_handler(signum, frame) -> None:
    # print summary, then exit with the same code
    _print_summary_once()
    # restore default handler and re-raise default to allow normal termination
    signal.signal(signum, signal.SIG_DFL)
    # On some platforms sys.exit may not deliver the same semantics as re-raising KeyboardInterrupt
    try:
        # try to exit cleanly
        sys.exit(0)
    except SystemExit:
        # if sys.exit was intercepted, force raise the signal as KeyboardInterrupt for SIGINT
        raise

# register atexit and common signals
atexit.register(_atexit_handler)
try:
    signal.signal(signal.SIGINT, _signal_handler)
except Exception:
    # some environments (like certain UIs) may not allow signal handling
    pass
try:
    signal.signal(signal.SIGTERM, _signal_handler)
except Exception:
    pass