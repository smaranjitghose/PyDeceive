# PyDeceive
A simple script to deceive others by making you insvisible

# Lets understand this

## Firstly lets understand how to access our camera:

#### Recording a video
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

- Here, ret is a Boolean value returned by the read function, and it indicates whether or not the frame was captured successfully. If the frame is captured correctly, it's stored in the variable frame

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
#### Saving a video

We create a VideoWriter object with following parameters for this:
- First we specify the output file name (eg: output.avi). 
- Second we specify the FourCC code.
                - FourCC is a 4-byte code used to specify the video codec.
                - The list of available codes can be found in [fourcc.org](http://www.fourcc.org/codecs.php).
                - It is platform dependent
- Third we specify the number of frames per second (fps) and frame size should be passed. 
- Lastly we specify the isColor flag. If it is True, encoder expect color frame, otherwise it works with grayscale frame

```python
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('wizard_smaran.avi' , fourcc, 20.0, (640,480))
```
   
## Now coming to our magic spell

#### Extracting our background
- We will replace the current frame pixels corresponding to the cloth with the background pixels to generate the effect of an invisibility cloak. For this we need to store the frame of a static background
```python
background = 0
for i in range(30):
    ret, background = cap.read()
```
- As the background is static we could have used a single capture. 
- However at times the image captured is a bit dark compared to when multiple frames are captured. 
- Thus capturing multiple images of static background with a for loop is more preferrble
- Averaging over multiple frames also reduces noise

#### Detecting the color of our magical cloak

- By default we are using a red color cloak for our magic trick 
- For an RGB (Red-Green-Blue) image we can simply threshold the R channel and get our mask. 
- However this is not effective since the RGB values are highly sensitive to illumination. 
- Although our cloak would be of red color,there might be certain parts where, due-to shadow, Red channel values of the corresponding pixels are quite low and we could be exposed!
- Thus we transform the color space of our image from RGB to HSV (Hue – Saturation – Value)

```python
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 ```

- **Wait!..Now what is HSV?**

| Channel | What it means |
| ------- | ----------------------------------------------------------------------------------- |
| Hue(H) | This channel encodes color information, expressed as a number from 0 to 360 degrees |
| Saturation(S) |This channel encodes the intensity/purity of color. For example, pink is less saturated than red.It basically describes the amount of grey in a particular colour, from 0 to 100 percent. Reducing this component toward zero introduces more grey and produces a faded effect|
| Value(V) | This channel encodes the brightness or intensity of the colour,from 0–100 percent, where 0 is completely black, and 100 is the brightest and reveals the most colour. Shading and gloss components of an image appear in this channel. |

Unlike RGB which is defined in relation to primary colors, HSV is defined in a way that is similar to how humans perceive color.



