"""
main.py

Entry point for the AI-Based Gesture Controlled Desktop Assistant.

Run this file to start webcam capture, detect hand landmarks, recognize
gestures, and execute desktop actions such as mouse movement, clicking,
volume control, screenshots, and media control.
"""

from __future__ import annotations

import time
from typing import Optional

import cv2

from gesture_controller import GestureController, INDEX_TIP
from hand_detector import HandDetector
from media_control import MediaControl
from mouse_control import MouseControl
from screenshot import ScreenshotManager
from volume_control import VolumeControl


CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


def draw_status(frame, gesture_text: str, fps: int, volume_percent: Optional[int] = None) -> None:
    """Draw project UI information on the OpenCV frame."""

    cv2.rectangle(frame, (0, 0), (520, 115), (20, 20, 20), cv2.FILLED)
    cv2.putText(
        frame,
        f"Gesture: {gesture_text}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2,
    )
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    if volume_percent is not None:
        cv2.putText(
            frame,
            f"Volume: {volume_percent}%",
            (250, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 200, 0),
            2,
        )


def main() -> None:
    """Start the desktop assistant application."""

    detector = HandDetector()
    gestures = GestureController()
    mouse = MouseControl()
    volume = VolumeControl()
    screenshots = ScreenshotManager()
    media = MediaControl()

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

    previous_time = 0.0
    active_gesture = "NONE"
    volume_percent: Optional[int] = None

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Unable to read from webcam. Check camera permissions or camera index.")
                break

            # Mirror frame for a natural user experience.
            frame = cv2.flip(frame, 1)
            frame = detector.find_hands(frame, draw=True)
            landmarks = detector.get_landmarks(frame)
            frame_height, frame_width, _ = frame.shape
            volume_percent = None

            if landmarks:
                state = gestures.analyze(landmarks, detector.hand_label)
                active_gesture = state.name
                index_tip = landmarks[INDEX_TIP]

                if state.name in {"MOUSE MOVE", "VOLUME CONTROL", "DRAG"}:
                    mouse.move_cursor(index_tip, (frame_width, frame_height))

                if state.name == "LEFT CLICK" and gestures.can_trigger("left_click"):
                    mouse.left_click()
                elif state.name == "RIGHT CLICK" and gestures.can_trigger("right_click"):
                    mouse.right_click()
                elif state.name == "DOUBLE CLICK" and gestures.can_trigger("double_click"):
                    mouse.double_click()
                elif state.name == "DRAG":
                    mouse.start_drag()
                else:
                    mouse.stop_drag()

                if state.name == "VOLUME CONTROL":
                    volume_percent, _ = volume.set_volume_by_distance(state.distances["thumb_index"])

                if state.name == "SCREENSHOT" and gestures.can_trigger("screenshot"):
                    try:
                        saved_path = screenshots.capture()
                        active_gesture = f"SCREENSHOT SAVED: {saved_path.name}"
                        print(f"Screenshot saved: {saved_path}")
                    except Exception as error:
                        active_gesture = "SCREENSHOT FAILED"
                        print(f"Screenshot failed: {error}")

                if state.name == "PLAY/PAUSE" and gestures.can_trigger("play_pause"):
                    media.play_pause()
                elif state.name == "NEXT TRACK" and gestures.can_trigger("next_track"):
                    media.next_track()
                elif state.name == "PREVIOUS TRACK" and gestures.can_trigger("previous_track"):
                    media.previous_track()
            else:
                active_gesture = "NONE"
                mouse.stop_drag()

            current_time = time.time()
            fps = int(1 / (current_time - previous_time)) if previous_time else 0
            previous_time = current_time

            draw_status(frame, active_gesture, fps, volume_percent)
            cv2.imshow("Gesture Controlled Desktop Assistant", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Application interrupted by user.")
    except Exception as error:
        print(f"Unexpected error: {error}")
    finally:
        mouse.stop_drag()
        camera.release()
        cv2.destroyAllWindows()
        detector.close()


if __name__ == "__main__":
    main()
