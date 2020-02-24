# PyDeceive
A simple script to deceive others by making you insvisible

# Lets understand this

### Firstly lets understand how to record video from a camera:

```python
import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

- OpenCV provides a very simple interface to this.(I am using the in-built webcam of my laptop)
```python
import cv2
```
- To capture a video, you need to create a VideoCapture object. Its argument can be either the device index or the name of a video file. Device index is just the number to specify which camera. Normally one camera will be connected (as in my case). So I simply pass 0 (or -1). You can select the second camera by passing 1 and so on. 

```python
cap = cv2.VideoCapture(0)
```
- Once it's created, we start an infinite loop and keep reading frames from the webcam until we encounter a keyboard interrupt

```python
while True:
    ret, frame = cap.read()
 ```

-Here, ret is a Boolean value returned by the read function, and it indicates whether or not the frame was captured successfully. If the frame is captured correctly, it's stored in the variable frame

- As we know, the ASCII value of Esc is 27. Once we encounter it, we break the loop and release the video capture object. The line cap.release() is important because it gracefully closes the webcam

```python    
        if c == 27:
             break

cap.release()
cv2.destroyAllWindows()
```
- Sometimes, ```cap``` may not have initialized the capture. In that case, this code shows error. You can check whether it is initialized or not by the method ```cap.isOpened()```. If it is True, OK. Otherwise open it using ```cap.open()```
```python
if not cap.isOpened():
    raise IOError("Cannot open webcam")
```
