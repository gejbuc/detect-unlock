# Face Detection Project

A simple face detection system using OpenCV's Haar Cascade classifier. Supports both image files and real-time webcam detection with configurable parameters.

## Overview

This project provides a face detection script that can detect faces in static images or from a webcam feed. It includes configuration files for tuning detection parameters.

## Project Structure

```
detect-unlock/
├── scripts/
│   ├── face_detect.py   # Main face detection script
│   ├── config.json      # JSON configuration file
│   └── config.py        # Python configuration module
├── src/                 # Implementation (system logic)
├── tests/               # Verification (behavioral guarantees)
└── README.md            # Project overview
```

## Requirements

- Python 3.x
- OpenCV (cv2)

Install OpenCV:
```bash
pip install opencv-python
```

## Quick Start

### Detect faces in an image:
```bash
python scripts/face_detect.py --image path/to/photo.jpg
```

### Detect faces from webcam:
```bash
python scripts/face_detect.py --webcam
```

## Configuration

### Using JSON config file:
```bash
python scripts/face_detect.py --webcam --config config.json
```

### Using presets:
```bash
# Fast detection (higher scale factor, lower accuracy)
python scripts/face_detect.py --webcam --preset fast

# Accurate detection (lower scale factor, more checks)
python scripts/face_detect.py --image photo.jpg --preset accurate

# Detect small faces
python scripts/face_detect.py --image photo.jpg --preset small_faces
```

Available presets: fast, accurate, small_faces, large_only, high_quality

### Using command-line overrides:
```bash
python scripts/face_detect.py --webcam --scale 1.05 --neighbors 6 --min-size 20
```

## Tunable Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| scaleFactor | Image scale reduction per step. Higher = faster but may miss faces. Lower = more accurate but slower. | 1.01 - 1.5 |
| minNeighbors | Minimum detections required to confirm a face. Higher = fewer false positives. Lower = more detections. | 3 - 7 |
| minSize | Minimum face size in pixels. Smaller = detect more faces but slower. | 15 - 100 |

## Configuration Files

### config.json
Human-readable JSON configuration file. Edit values directly:
```json
{
  "detection": {
    "scaleFactor": 1.1,
    "minNeighbors": 5,
    "minSize": {"width": 30, "height": 30}
  },
  "drawing": {
    "rectangle": {
      "color": {"blue": 0, "green": 255, "red": 0},
      "thickness": 2
    }
  }
}
```

### config.py
Python configuration module. Import and use programmatically:
```python
import config

# Modify parameters
config.SCALE_FACTOR = 1.05
config.MIN_NEIGHBORS = 6

# Get parameters for detectMultiScale
params = config.get_detection_params()
```

## Usage Examples

### Real-time webcam with fast preset:
```bash
python scripts/face_detect.py --webcam --preset fast
```

### Image detection with custom config:
```bash
python scripts/face_detect.py --image group_photo.jpg --config config.json
```

### Override config file with CLI arguments:
```bash
python scripts/face_detect.py --webcam --config config.json --scale 1.2 --neighbors 4
```

## Controls

- Press q to quit the webcam mode
- Window displays face count and current detection parameters
