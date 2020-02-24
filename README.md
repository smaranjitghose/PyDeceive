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

#### Detecting the our magical cloak
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

- The Hue values are actually distributed over a circle (range between 0-360 degrees) but in OpenCV to fit into 8bit value the range is from 0-180. The red color is represented by 0-30 as well as 150-180 values.

- We use the range 0-10 and 170-180 to avoid detection of skin as red. For the saturation(S) values a high range of 120-255 is used because as our cloak would be of highly saturated red color. For the value parameter(V),the lower rangeis 70 so that we can detect red color in the wrinkles of the cloth as well
```python
    
    # Forming mask 1 for red range_1
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
 
    # Forming mask 2 for red range_2
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)
  ```

- Now we combine masks generated for both the red color ranges by doing an pixel-wise OR operation 

```python
    mask1 = mask1 + mask2 
 ```
### Segmenting out our magic cloak and making us invisible

The pixel values of the detected red color region are replaced with corresponding pixel values of the static background and an augmented output is generated which creates the magical effect. We use bitwise_and operation first to create an image with pixel values, corresponding to the detected region, equal to the pixel values of the static background and then add the output to the image  from which we had segmented out the red cloak

- Creating an inverted mask to segment out the cloak from the frame
```python
    mask2 = cv2.bitwise_not(mask1)
 ```
 
 - Segmenting the cloak out of the frame using ```bitwise_and``` and with the inverted mask
 ```python
    layer1 = cv2.bitwise_and(background, background, mask=mask1)
 ```
 -  Creating an image showing static background frame pixels only for the masked region
  ```python
    layer2 = cv2.bitwise_and(img, img, mask=mask2)
 ```
 
 - Finally combining the layers to make us invisible
 
 ```python
 final_output = cv2.addWeighted(layer1 , 1, layer2 , 1, 0)
 ```
 
 # Further Tasks:
 - Have a script to effectively find out HSV color value of any cloak we want to use
 - Try this trick with other colors
 - Create an GUI for this where you can input the color of your cloak and your spell is made!
 
 # License
 
 [MIT License](https://github.com/smaranjitghose/PyDeceive/blob/master/LICENSE)
 
 # Crafted with ❤️ by [Smaranjit Ghose](https://github.com/smaranjitghose)
