import cv2
import time
# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
initia = 0
# To capture video from webcam.
cap = cv2.VideoCapture(0)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
counter_size = 0

def position_func(targetx, targety):
    print(targetx, targety)
    time.sleep(5)


while True:
    # Read the frame
    _, img = cap.read()

    cv2.rectangle(img, (310,250 ), (330, 230), (255, 0, 0), 2)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        if(w*h) > 0.65*initia or (w*h) == initia:
            initia = w*h
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            target_x = int( x+ (w/2))
            target_y = int ( y + (h/2))
            a1 = target_x - 10
            a2 = target_x + 10
            a3 = target_y - 10
            a4 = target_y + 10
            cv2.rectangle(img, (a1, a4), (a2, a3), (255, 0, 0), 2)
           # position_func(target_x, target_y)
        elif(w*h) < 0.65*initia:
            counter_size +=1
            if counter_size == 5:
                counter_size = 0
                initia = 100
            continue



    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
cap.release()