# EldenRingAI
An AI that currently is in beta, but will potentially move the character around based on facial features

For now the code can be run by simply executing 

```bash
python main.py
```

make sure that you have the following packages installed
```
opencv (cv2) and pydirectinput
```

if the camera is not working change line 109
```python
# Current
video_capture = cv2.VideoCapture(1)

# To any other digit e.g. 0
video_capture = cv2.VideoCapture(0)
```