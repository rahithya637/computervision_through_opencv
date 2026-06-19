# AI-Based Gesture Controlled Desktop Assistant

This project is a B.Tech AIML mini project that uses a webcam, OpenCV, MediaPipe hand landmarks, and PyAutoGUI to control desktop actions through hand gestures. No custom machine learning model training is required.

## Features

- Mouse cursor movement using the index fingertip
- Left click, right click, and double click gestures
- Drag and drop gesture
- Windows volume control using Pycaw
- Timestamped screenshot capture in `screenshots/`
- Media controls for play/pause, next track, and previous track
- Live hand landmark drawing
- Current gesture display
- FPS counter
- ESC key exit

## Gesture Mapping

| Gesture | Action |
| --- | --- |
| Index finger raised | Move mouse cursor |
| Thumb tip + index tip touching | Left click |
| Thumb tip + middle tip touching | Right click |
| Index tip + middle tip touching | Double click |
| Thumb tip + ring tip touching | Drag and drop |
| Thumb and index raised with changing distance | Volume control |
| All fingers raised | Screenshot |
| Index + middle raised | Play/Pause |
| Index + middle + ring raised | Next track |
| Index + middle + ring + pinky raised | Previous track |

## Project Structure

```text
Gesture_Desktop_Assistant/
├── main.py
├── hand_detector.py
├── gesture_controller.py
├── mouse_control.py
├── volume_control.py
├── screenshot.py
├── media_control.py
├── screenshots/
├── requirements.txt
└── README.md
```

## Module Explanation

`hand_detector.py` initializes MediaPipe Hands, detects landmarks from webcam frames, draws hand landmarks, and returns landmark coordinates in pixel form.

`gesture_controller.py` contains gesture recognition logic, Euclidean distance calculation, finger state detection, and action cooldown/debouncing.

`mouse_control.py` maps index fingertip webcam coordinates to screen coordinates and performs mouse movement, clicks, double clicks, and drag/drop operations.

`volume_control.py` uses Pycaw to control Windows system volume by mapping thumb-index distance to the supported audio volume range.

`screenshot.py` saves screenshots with timestamp-based filenames inside the `screenshots/` folder.

`media_control.py` sends media key presses using PyAutoGUI.

`main.py` integrates all modules, captures webcam frames, calculates FPS, displays UI text, handles ESC exit, and safely releases resources.

## Installation

Use Python 3.10 or 3.11 on Windows for best compatibility with MediaPipe and Pycaw.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Press `ESC` while the webcam window is active to close the application.

## Notes for Demonstration

- Keep your hand clearly visible to the webcam.
- Use a plain background and good lighting for better landmark detection.
- If clicks happen too quickly or too slowly, adjust `action_cooldown` in `GestureController`.
- If touch gestures are difficult to trigger, adjust `touch_threshold` in `GestureController`.
- Move slowly during volume control because system volume changes in real time.

## Professional Improvements Included

- Object-oriented module design
- Debouncing to prevent repeated clicks and screenshots
- Screen-coordinate scaling using NumPy interpolation
- Drag state management to avoid stuck mouse button presses
- Exception handling and clean resource release
- Timestamp-based screenshot filenames
- Beginner-friendly comments and clear module separation
