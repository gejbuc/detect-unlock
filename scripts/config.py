"""
Face Detection Configuration Module

Python configuration for face detection parameters.
"""

import cv2
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import json


# ============================================================================
# Cascade Configuration
# ============================================================================

class CascadeConfig:
    """Configuration for the Haar Cascade classifier."""
    
    ALTERNATE_MODELS = {
        "default": "haarcascade_frontalface_default.xml",
        "alt": "haarcascade_frontalface_alt.xml",
        "alt2": "haarcascade_frontalface_alt2.xml",
        "profile": "haarcascade_profileface.xml",
    }
    
    @classmethod
    def get_model_path(cls, model_name: str = "default") -> str:
        return cv2.data.haarcascades + cls.ALTERNATE_MODELS.get(model_name, cls.ALTERNATE_MODELS["default"])


# ============================================================================
# Detection Parameters
# ============================================================================

SCALE_FACTOR = 1.1          # Image scale reduction per step (1.01-1.5)
MIN_NEIGHBORS = 5           # Min detections to confirm face (3-7)
MIN_SIZE = (30, 30)        # Minimum face size (width, height)
MAX_SIZE = (0, 0)          # Maximum face size (0,0 = no limit)


# ============================================================================
# Drawing Configuration
# ============================================================================

RECTANGLE_COLOR = (0, 255, 0)      # BGR: Green
RECTANGLE_THICKNESS = 2
TEXT_COLOR = (0, 255, 0)          # BGR: Green
TEXT_THICKNESS = 2
TEXT_SCALE = 1.0


# ============================================================================
# Video Configuration
# ============================================================================

CAPTURE_DEVICE = 0         # Webcam device index
CAMERA_INDEX = 0           # Selected camera index
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


# ============================================================================
# Output Configuration
# ============================================================================

SAVE_RESULTS = False
OUTPUT_DIRECTORY = Path("output")


# ============================================================================
# Functions
# ============================================================================

def get_detection_params() -> Tuple[float, int, Tuple[int, int], Tuple[int, int], int]:
    """Get detection parameters for detectMultiScale."""
    return (SCALE_FACTOR, MIN_NEIGHBORS, MIN_SIZE, MAX_SIZE, cv2.CASCADE_SCALE_IMAGE)


def load_from_json(json_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)


def save_to_json(config_dict: Dict[str, Any], json_path: str, indent: int = 2) -> None:
    """Save configuration to JSON file."""
    with open(json_path, 'w') as f:
        json.dump(config_dict, f, indent=indent)


def update_from_dict(config_dict: Dict[str, Any]) -> None:
    """Update global config from dictionary."""
    global SCALE_FACTOR, MIN_NEIGHBORS, MIN_SIZE, MAX_SIZE
    global RECTANGLE_COLOR, RECTANGLE_THICKNESS
    global CAMERA_INDEX, CAPTURE_DEVICE, FRAME_WIDTH, FRAME_HEIGHT, SAVE_RESULTS
    
    if "detection" in config_dict:
        d = config_dict["detection"]
        SCALE_FACTOR = d.get("scaleFactor", SCALE_FACTOR)
        MIN_NEIGHBORS = d.get("minNeighbors", MIN_NEIGHBORS)
        ms = d.get("minSize", {})
        MIN_SIZE = (ms.get("width", MIN_SIZE[0]), ms.get("height", MIN_SIZE[1]))
    
    if "camera" in config_dict:
        c = config_dict["camera"]
        CAMERA_INDEX = c.get("index", CAMERA_INDEX)
    
    if "drawing" in config_dict:
        g = config_dict["drawing"].get("rectangle", {})
        c = g.get("color", {})
        RECTANGLE_COLOR = (c.get("blue", 0), c.get("green", 255), c.get("red", 0))
        RECTANGLE_THICKNESS = g.get("thickness", RECTANGLE_THICKNESS)
    
    if "video" in config_dict:
        v = config_dict["video"]
        CAPTURE_DEVICE = v.get("capture_device", CAPTURE_DEVICE)
        FRAME_WIDTH = v.get("frame_width", FRAME_WIDTH)
        FRAME_HEIGHT = v.get("frame_height", FRAME_HEIGHT)
    
    if "output" in config_dict:
        o = config_dict["output"]
        SAVE_RESULTS = o.get("save_results", SAVE_RESULTS)


def to_dict() -> Dict[str, Any]:
    """Convert all configs to dictionary."""
    return {
        "detection": {
            "scaleFactor": SCALE_FACTOR,
            "minNeighbors": MIN_NEIGHBORS,
            "minSize": {"width": MIN_SIZE[0], "height": MIN_SIZE[1]},
            "maxSize": {"width": MAX_SIZE[0], "height": MAX_SIZE[1]},
        },
        "drawing": {
            "rectangle": {
                "color": {"blue": RECTANGLE_COLOR[0], "green": RECTANGLE_COLOR[1], "red": RECTANGLE_COLOR[2]},
                "thickness": RECTANGLE_THICKNESS,
            }
        },
        "video": {"capture_device": CAPTURE_DEVICE, "frame_width": FRAME_WIDTH, "frame_height": FRAME_HEIGHT},
        "output": {"save_results": SAVE_RESULTS, "output_directory": str(OUTPUT_DIRECTORY)},
    }


# ============================================================================
# Presets
# ============================================================================

PRESETS = {
    "fast": {"detection": {"scaleFactor": 1.3, "minNeighbors": 3, "minSize": {"width": 60, "height": 60}}},
    "accurate": {"detection": {"scaleFactor": 1.05, "minNeighbors": 6, "minSize": {"width": 20, "height": 20}}},
    "small_faces": {"detection": {"scaleFactor": 1.1, "minNeighbors": 4, "minSize": {"width": 15, "height": 15}}},
    "large_only": {"detection": {"scaleFactor": 1.2, "minNeighbors": 5, "minSize": {"width": 100, "height": 100}}},
    "high_quality": {"detection": {"scaleFactor": 1.05, "minNeighbors": 8, "minSize": {"width": 30, "height": 30}}, "drawing": {"rectangle": {"color": {"blue": 255, "green": 0, "red": 0}, "thickness": 3}}},
}


def apply_preset(preset_name: str) -> None:
    """Apply a preset configuration."""
    if preset_name in PRESETS:
        update_from_dict(PRESETS[preset_name])
        print(f"Applied preset: {preset_name}")
    else:
        print(f"Unknown preset: {preset_name}. Available: {list(PRESETS.keys())}")


if __name__ == "__main__":
    print("Current detection parameters:")
    print(f"  scaleFactor: {SCALE_FACTOR}")
    print(f"  minNeighbors: {MIN_NEIGHBORS}")
    print(f"  minSize: {MIN_SIZE}")
    print(f"\nAvailable presets: {list(PRESETS.keys())}")