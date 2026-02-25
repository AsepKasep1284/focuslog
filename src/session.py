from __future__ import annotations
import datetime
import threading
from typing import Optional

# keep this minimal and dependency-free
class Session:
    """
    Simple focus/work session object.

    Usage:
        s = Session("Morning")
        s.start()
        ... do stuff ...
        s.stop()
        print(s.duration())  # timedelta
    """

    def __init__(self, name: Optional[str] = None, auto_register: bool = True):
        self.name = name or "session"
        self._start: Optional[datetime.datetime] = None
        self._end: Optional[datetime.datetime] = None
        self._lock = threading.Lock()
        # auto register to global exit hook registry (so the library prints on exit)
        self._registered = False
        if auto_register:
            # import here to avoid circular import at module import time
            from . import hook as _hook
            _hook.register(self)
            self._registered = True

    def start(self) -> None:
        with self._lock:
            if self._start is None:
                self._start = datetime.datetime.now()
                self._end = None

    def stop(self) -> None:
        with self._lock:
            if self._start is None:
                # starting implicitly if someone calls stop first
                self._start = datetime.datetime.now()
            if self._end is None:
                self._end = datetime.datetime.now()

    def duration(self) -> datetime.timedelta:
        with self._lock:
            if self._start is None:
                return datetime.timedelta(0)
            end = self._end or datetime.datetime.now()
            return end - self._start

    def is_active(self) -> bool:
        with self._lock:
            return self._start is not None and self._end is None

    def summary(self) -> str:
        """Return a short human readable summary of the session."""
        dur = self.duration()
        # pretty formatting: Hh Mm Ss
        total_seconds = int(dur.total_seconds())
        hours, rem = divmod(total_seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        parts = []
        if hours:
            parts.append(f"{hours}h")
        if minutes or (hours and seconds):
            parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        status = "active" if self.is_active() else "done"
        return f"Session '{self.name}' [{status}] — {', '.join(parts)}"

    def unregister(self) -> None:
        """If previously auto-registered, remove from the global registry."""
        if not self._registered:
            return
        from . import hook as _hook
        _hook.unregister(self)
        self._registered = False

    def register(self) -> None:
        """(Re-)register the session to be printed at exit."""
        if self._registered:
            return
        from . import hook as _hook
        _hook.register(self)
        self._registered = True

    def __repr__(self) -> str:
        return f"<Session name={self.name!r} active={self.is_active()}>"