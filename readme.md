# Pokémon Go Real-Time Throw Assistant

Small experimental project that captures a scrcpy Android window, detects a colored target circle using OpenCV, and issues ADB swipe commands to simulate a throw.

Files
- [cv_test.py](cv_test.py) — simple OpenCV window test to verify display and OpenCV setup.
- [realtime_throw_assistant.py](realtime_throw_assistant.py) — main assistant: screen capture, circle detection, and ADB swipe logic.
- [readme.md](readme.md) — this file.

Quick overview
- Detection logic is implemented in [`find_target_circle`](realtime_throw_assistant.py).
- ADB swipe execution is performed by [`execute_adb_swipe`](realtime_throw_assistant.py).
- Configure the target scrcpy window title via the [`SCRCPY_WINDOW_TITLE`](realtime_throw_assistant.py) constant and set your ADB binary path in [`ADB_PATH`](realtime_throw_assistant.py).

Prerequisites
- Python 3.8+
- Windows (project uses `pywin32` / `win32gui` to find the scrcpy window)
- ADB (platform-tools) installed and reachable via the path set in [`ADB_PATH`](realtime_throw_assistant.py)
- scrcpy running and showing the device you want to control

Install Python dependencies
```sh
pip install opencv-python numpy mss pywin32