import cv2
import numpy as np
import time
net = cv2.dnn.readNet('yolov3-tiny.weights','yolov3-tiny.cfg')
classes = []
with open('coco.names','r') as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture(0)


def move_motor_x_small():
    print("Small X")


def move_motor_x_large():
    print("Large X")


def move_motor_y_small():
    print("Small y")


def move_motor_y_large():
    print("Large y")


while True:
    _, img = cap.read()
    height, width, _ = img.shape
    cv2.rectangle(img, (310, 250), (330, 230), (255, 0, 0), 2)

    blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []
    highest_area = 100

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]

            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.4:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                if class_id == 0:
                    current_area = w*h
                    if current_area > highest_area:
                        boxes = []
                        confidences = []
                        class_ids = []
                        boxes.append([x, y, w, h])
                        confidences.append((float(confidence)))
                        class_ids.append(class_id)
                        print(class_ids)
                        highest_area = current_area
                        print("Highest area is" +str(highest_area))

                    else:
                        print("Lower area found")


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))

    if len(indexes)>0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            print (x,y,w,h)
            label = str(classes[class_ids[i]])

            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label + "" + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)
            target_x = x + 0.5*w
            target_y = y + 0.5*h
            current_x = 320
            current_y = 240
            if abs(target_x - current_x) > 10 and abs(target_x - current_x) > 70:
                move_motor_x_large()
            elif abs(target_x - current_x) > 10:
                move_motor_x_small()
            else:
                print("X Position Reached")

            if abs(target_y - current_y) > 10 and abs(target_y - current_y) > 70:
                move_motor_y_large()
            elif abs(target_y - current_y) > 10:
                move_motor_y_small()
            else:
                print("Y Position Reached")

        cv2.imshow('Image', img)
        time.sleep(0.5)
        key = cv2.waitKey(1)
        if key == 27:
            break

cap.release()
cv2.destroyAllWindows()
