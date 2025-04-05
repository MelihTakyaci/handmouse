# HandMouse: Gesture-Based Mouse Controller

This project is a simple, camera-based system that allows you to control your mouse using hand gestures. Built using OpenCV, MediaPipe, and PyAutoGUI, the system detects your hand in real time and performs the following actions:

- Moves the mouse pointer based on your **middle finger tip** (more stable than palm)
- Simulates a **left click** when your **thumb is folded in** (instead of touching the index finger)
- Simulates a **right click** when your **thumb touches the index finger knuckle** (landmark 4 + 6)
- Triggers **desktop switching (MacOS)** when your **thumb and ring finger touch**, and you move your hand left/right
- Allows zoom in/out of the detection area with `i` and `o` keys
- ROI (Region of Interest) is centered dynamically and scaled proportionally to the screen
- **Settings pop-up window** opens when the icon at the top right is clicked
- **Slider-based smoothing factor control** is available in the settings window (adjustable between 1–10 in real-time)

## Controls
- `i` → Zoom in (reduce ROI size)
- `o` → Zoom out (increase ROI size)
- `q` → Quit the program

## Gestures
| Action                 | Gesture Description                                     |
|------------------------|----------------------------------------------------------|
| **Move Mouse**         | Move your **middle finger tip** within the red ROI box  |
| **Left Click**         | Fold in your **thumb** (thumb x < thumb joint x)        |
| **Right Click**        | Touch **thumb tip (4)** to **index finger knuckle (6)** |
| **Desktop Switch**     | Touch **thumb (4)** to **ring finger (16)**, then move hand **←/→** |

## How It Works
1. The webcam feed is processed using MediaPipe to detect hand landmarks.
2. The ROI (region of interest) is automatically centered and highlighted.
3. The cursor is moved based on the position of the **middle finger tip (landmark 12)**.
4. Left and right clicks are triggered based on gesture proximity between specific landmarks.
5. Desktop switch gestures use movement direction after an activation gesture.
6. The settings window provides a real-time slider to change mouse smoothing responsiveness (affects transition sharpness).

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

