# focuslog

<p align="center">
  <img width="1280" src="/assets/easteregg.jpeg" alt="Easter Egg">
</p>

Tiny Python library for tracking focus/work sessions.

It provides a minimal `Session` object to measure how long a task runs,
and automatically prints a session summary when the Python program exits.

This project is intentionally small and dependency-free.

---

## Why?

Many apps need a lightweight way to measure how long users spend doing something:

- CLI tools
- productivity apps
- study timers
- automation scripts
- experiments / research tools

`focuslog` is designed to be a tiny building block for those apps.

---

## Installation

From GitHub:

```bash
pip install git+https://github.com/AsepKasep1284/focuslog.git
````

Local development:

```bash
pip install -e .
```

---

## Quick Example

```python
from focuslog import Session
import time

session = Session("Morning routine")
session.start()

time.sleep(3)

session.stop()
```

When the program exits, focuslog automatically prints:

```
[focuslog] Sessions summary:
  - Session 'Morning routine' [done] — 0m, 3s
```

It also works when the program is stopped with **Ctrl+C**.

---

## Basic Usage

```python
from focuslog import Session

s = Session("Study")
s.start()

# ... your code ...

s.stop()
print(s.duration())
```

### Public API

* `Session.start()`
* `Session.stop()`
* `Session.duration() -> timedelta`
* `Session.summary() -> str`
* `Session.register()` / `Session.unregister()`

By default, sessions automatically register themselves to be printed at exit.

You can disable this:

```python
s = Session("Temp", auto_register=False)
```

---

## Exit Hooks

focuslog automatically prints a summary when the interpreter shuts down using:

* `atexit`
* `SIGINT` (Ctrl+C)
* `SIGTERM`

This is useful for CLI tools and long-running scripts.

The library never modifies files or sends network requests.
It only prints a short summary to stdout.

---

## License

MIT License.

