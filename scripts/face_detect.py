"""
Face Detection Script with Config Support

Usage:
    python face_detect.py --image <path_to_image>
    python face_detect.py --webcam
    
    # Use config files:
    python face_detect.py --webcam --config config.json
    python face_detect.py --image photo.jpg --preset fast
"""

import cv2
import argparse
import sys
from pathlib import Path
import config


def load_face_detector(model_name: str = "default"):
    """Load the pre-trained Haar Cascade face detector."""
    model_path = config.CascadeConfig.get_model_path(model_name)
    face_cascade = cv2.CascadeClassifier(model_path)
    
    if face_cascade.empty():
        raise RuntimeError(f"Failed to load face cascade classifier: {model_path}")
    
    return face_cascade


def detect_faces(gray, face_cascade):
    """Detect faces using configured parameters."""
    params = config.get_detection_params()
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=params[0],
        minNeighbors=params[1],
        minSize=params[2],
        maxSize=params[3],
        flags=params[4]
    )
    return faces


def draw_faces(img, faces):
    """Draw rectangles around detected faces."""
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), config.RECTANGLE_COLOR, config.RECTANGLE_THICKNESS)
    return img


def detect_in_image(image_path, face_cascade):
    """Detect faces in a static image."""
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray, face_cascade)
    img = draw_faces(img, faces)
    
    print(f"Found {len(faces)} face(s) | scale={config.SCALE_FACTOR}, neighbors={config.MIN_NEIGHBORS}, minSize={config.MIN_SIZE}")
    
    cv2.imshow('Face Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return len(faces)


def detect_from_webcam(face_cascade):
    """Detect faces in real-time from webcam."""
    cap = cv2.VideoCapture(config.CAPTURE_DEVICE)
    
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")
    
    if config.FRAME_WIDTH > 0:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    
    print(f"Running | scale={config.SCALE_FACTOR}, neighbors={config.MIN_NEIGHBORS}, minSize={config.MIN_SIZE} | Press q to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray, face_cascade)
        frame = draw_faces(frame, faces)
        
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, config.TEXT_SCALE, config.TEXT_COLOR, config.TEXT_THICKNESS)
        
        cv2.imshow('Face Detection - Press q to quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Face Detection using OpenCV with Config Support')
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--image', type=str, help='Path to image file')
    input_group.add_argument('--webcam', action='store_true', help='Use webcam')
    
    parser.add_argument('--config', type=str, default=None, help='Path to JSON config file')
    parser.add_argument('--preset', type=str, default=None, choices=list(config.PRESETS.keys()), help='Use preset')
    parser.add_argument('--scale', type=float, default=None, help='Override scaleFactor')
    parser.add_argument('--neighbors', type=int, default=None, help='Override minNeighbors')
    parser.add_argument('--min-size', type=int, default=None, help='Override min face size')
    
    args = parser.parse_args()
    
    try:
        if args.config:
            config.update_from_dict(config.load_from_json(args.config))
            print(f"Loaded config: {args.config}")
        
        if args.preset:
            config.apply_preset(args.preset)
        
        if args.scale:
            config.SCALE_FACTOR = args.scale
        if args.neighbors:
            config.MIN_NEIGHBORS = args.neighbors
        if args.min_size:
            config.MIN_SIZE = (args.min_size, args.min_size)
        
        print("Loading face detector...")
        face_cascade = load_face_detector()
        
        if args.image:
            detect_in_image(args.image, face_cascade)
        else:
            detect_from_webcam(face_cascade)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()