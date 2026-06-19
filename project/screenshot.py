"""
screenshot.py

Captures timestamped screenshots using PyAutoGUI and stores them in the
screenshots/ folder.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pyautogui


class ScreenshotManager:
    """Creates and saves screenshots with unique timestamp-based filenames."""

    def __init__(self, output_dir: str = "screenshots") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self) -> Path:
        """Capture the current screen and save it as a PNG file."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = self.output_dir / f"screenshot_{timestamp}.png"
        image = pyautogui.screenshot()
        image.save(file_path)
        return file_path
