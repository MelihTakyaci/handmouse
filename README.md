# HandMouse: Gesture-Based Mouse Controller

This project is a simple, camera-based system that allows you to control your mouse using hand gestures. Built using OpenCV, MediaPipe, and PyAutoGUI, the system detects your hand in real time and performs the following actions:

- Moves the mouse pointer based on your **palm position**
- Simulates a **mouse click** when your **index finger and thumb come close together**
- Allows zoom in/out of the detection area with `i` and `o` keys
- ROI (Region of Interest) is centered dynamically on the camera frame

## Controls
- `i` → Zoom in (reduce ROI size)
- `o` → Zoom out (increase ROI size)
- `q` → Quit the program

## How It Works
1. The webcam feed is processed using MediaPipe to detect hand landmarks.
2. The ROI (region of interest) is automatically centered and highlighted.
3. The cursor is moved based on the position of landmark 9 (palm area).
4. A click is simulated when the distance between landmarks 4 and 8 is small enough (thumb and index finger).

## Requirements
Install the necessary dependencies with:

```bash
pip install -r requirements.txt
```

## Requirements.txt
```
opencv-python
mediapipe
pyautogui
numpy
```

---

❤️ by Melih Takyaci