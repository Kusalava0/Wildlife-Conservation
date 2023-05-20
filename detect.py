import cv2
import torch
from ultralytics import YOLO
import cv2
import cvzone
import math
from playsound import playsound
from test import send_alert
import os
from PIL import Image
import time
# specify the path of the audio file
audio_file_path = 'police-operation-siren-144229.mp3'
import datetime

intial = 0
# Model
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5l, yolov5x, etc.
model = torch.hub.load('ultralytics/yolov5', 'custom', 'C:/Users/dkb03/Desktop/Wildlife-Conservation/ml_model/md_v5a.0.0.pt')# custom trained model
model_ppe = YOLO("C:/Users/dkb03/Desktop/Wildlife-Conservation/ml_model/best.pt")
model_ani = YOLO("C:/Users/dkb03/Desktop/Wildlife-Conservation/ml_model/Re_best.pt")



def generate_frames(video_path):
    # Initialize the video capture object
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(video_path)

    # Initialize the list to store the frames
    classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone',
                'Safety Vest', 'machinery', 'vehicle']
    classAniNames = ["Person",
            "Elephant",
            "Leopard",
            "Arctic_Fox",
            "Chimpanzee",
            "Jaguar",
            "Lion",
            "Orangutan",
            "Panda",
            "Panther",
            "Rhino",
            "Cheetah"]
    # Loop through the frames of the video
    while cap.isOpened():
        # Read the next frame
        ret, frame = cap.read()
        height_org, width_org, channels = frame.shape
        if not ret:
            break
        
        # Append the frame to the list
        result = model(frame)
        # iterate through each box and label in the result tensor
        cropped_img = []
        cropped_animal = []
        for box in result.xyxy[0]:
            # extract the box coordinates and label index
            x1, y1, x2, y2, confidence, label_idx = box.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # get the class label from the model's class list
            class_label = model.names[int(label_idx)]
            
            # draw the box on the image
            if class_label == 'animal':
                print('animal')
                color = (0, 255, 0)  # green
                thickness = 2
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
                # add the class label and confidence score to the box
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)
                cropped_animal.append(frame[y1:y2, x1:x2])
            else:
                # Add Cropped people images
                cropped_img.append(frame[y1:y2, x1:x2])
            
            # print the box coordinates and class label
            print(f"Box: ({x1},{y1}) - ({x2},{y2}), Class: {class_label}, Confidence: {confidence}")
        
        alert_required = False
        for box_img in cropped_img:
            
            results = model_ppe(box_img)
            
            unique_labels = {}

            # iterate through the list of tuples
            
            for box in results[0].boxes:

                cls = int(box.cls[0])
                currentClass = classNames[cls]

                conf = math.ceil((box.conf[0] * 100)) / 100
                label, confidence = currentClass, conf
                if currentClass in [ 'Mask', 'NO-Mask', 'Safety Cone', 'machinery', 'vehicle'] :
                    continue
                # if the label is not already in the dictionary or if the confidence level is higher than the stored confidence level for that label
                if label not in unique_labels:
                    unique_labels[label] = box
                else:
                    conf_dict = math.ceil((unique_labels[label].conf[0] * 100)) / 100
                    if confidence > conf_dict:
                        # add or update the dictionary with the new label and confidence level
                        unique_labels[label] = box


            for box in unique_labels.values():
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = classNames[cls]
                print(currentClass)
                myColor = (127,255,0)
            
                if currentClass =='NO-Hardhat' or currentClass =='NO-Safety Vest':
                    myColor = (0, 0, 255)
                    # Alert
                    print('-----------------------Alert-----------------------')
                    # play the audio file

                    alert_required = True
                    cvzone.putTextRect(box_img, f'{classNames[cls]} {conf}',
                                (max(0, x1), max(35, y1)), scale=1, thickness=1,colorB=myColor,
                                colorT=(255,255,255),colorR=(0,0,255), offset=5)
                    cv2.rectangle(box_img, (x1, y1), (x2, y2), myColor, 3)
                    # playsound(audio_file_path)
        prev = ''
        for box_img in cropped_animal: 
            results = model_ani(box_img)
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])
                currentClass = classAniNames[cls]
                print(currentClass)
                myColor = (127,255,0)
            
                if prev == '':
                    prev = currentClass
                elif prev != currentClass:
                    # Alert
                    print('-----------------------Alert-----------------------')
                    # play the audio file
                    alert_required = True
                    cvzone.putTextRect(box_img, f'{classAniNames[cls]} {conf}',
                                (max(0, x1), max(35, y1)), scale=1, thickness=1,colorB=myColor,
                                colorT=(255,255,255),colorR=(0,0,255), offset=5)
                    cv2.rectangle(box_img, (x1, y1), (x2, y2), myColor, 3)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # # yield the frame bytes to the generator
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        global intial  
        if alert_required and (intial == 0 or (datetime.datetime.now() - intial).total_seconds() > 30) :
            cv2.imwrite("output.jpg", frame)
            # send_alert("output.jpg")  
            intial = datetime.datetime.now()
            
            os.remove('C:/Users/dkb03/Desktop/Wildlife-Conservation/output.jpg')
            # print("------------------------SENT ALERT-----------------------------")
        # convert the frame to bytes
          
        # cv2.imshow("Result", frame)

        # # # wait for a key press and check if the user wants to quit
        # if cv2.waitKey(1) == ord("q"):
        #     break
        
# Release the video capture object and close all windows
# generate_frames(0)
# cap.release()
# cv2.destroyAllWindows()