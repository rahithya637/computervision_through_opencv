"""
volume_control.py

Controls Windows system volume using Pycaw. The gesture distance is mapped
linearly to the audio endpoint's supported volume range.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:
    """Handles system volume changes through Pycaw."""

    def __init__(self, min_hand_distance: float = 25.0, max_hand_distance: float = 220.0) -> None:
        self.min_hand_distance = min_hand_distance
        self.max_hand_distance = max_hand_distance
        self.volume = None
        self.min_volume = -65.25
        self.max_volume = 0.0
        self.is_available = False

        try:
            self._initialize_audio_endpoint()
            self.is_available = True
        except Exception as error:
            print(f"Volume control disabled: {error}")

    def _initialize_audio_endpoint(self) -> None:
        """Initialize the Windows audio endpoint used by Pycaw."""

        devices = AudioUtilities.GetSpeakers()

        # Newer Pycaw versions expose EndpointVolume directly on AudioDevice.
        # Older versions require activating the COM endpoint manually.
        if hasattr(devices, "EndpointVolume"):
            self.volume = devices.EndpointVolume
        else:
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume = interface.QueryInterface(IAudioEndpointVolume)

        self.min_volume, self.max_volume, _ = self.volume.GetVolumeRange()

    def set_volume_by_distance(self, distance: float) -> Tuple[int, float]:
        """
        Convert hand distance to system volume.

        Returns volume percentage and raw Pycaw volume scalar for UI display.
        """

        volume_scalar = float(
            np.interp(
                distance,
                (self.min_hand_distance, self.max_hand_distance),
                (0.0, 1.0),
            )
        )
        volume_scalar = float(np.clip(volume_scalar, 0.0, 1.0))
        volume_percent = int(volume_scalar * 100)
        volume_percent = int(np.clip(volume_percent, 0, 100))

        if self.volume is not None and self.is_available:
            self.volume.SetMasterVolumeLevelScalar(volume_scalar, None)

        return volume_percent, volume_scalar
