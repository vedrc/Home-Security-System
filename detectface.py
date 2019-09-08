import face_recognition
import cv2
import numpy as np
import os
from twilio.rest import Client
from datetime import timedelta
from datetime import datetime
import time
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import math


now = datetime.now()
future_time = now + timedelta (minutes=20)
sent = False

debug_on = True


config = configparser.ConfigParser()
config.read('config.ini')
known_dir = config['dir']['known_faces_dir']
screenshot_dir = config['dir']['screenshot_dir']
from_phone = config['sms']['from_phone']
to_phone = config['sms']['to_phone']

    
def debug(message):
    global debug_on
    if (debug_on):
        print ('DEBUG: {}'.format(message))
    
def genderage():

    def getFaceBox(net, frame, conf_threshold=0.7):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
        return frameOpencvDnn, bboxes

    faceProto = config['models']['faceProto']
    faceModel = config['models']['faceModel']
    ageProto = config['models']['ageProto']
    ageModel = config['models']['ageModel']
    genderProto = config['models']['genderProto']
    genderModel = config['models']['genderModel']

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['0-2', '4-6', '8-12', '15-20', '25-32', '38-43', '48-53', '60-100']
    genderList = ['Male', 'Female']

    # Load network
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)
    faceNet = cv2.dnn.readNet(faceModel, faceProto)

    # Open a video file or an image file or a camera stream
    cap = cv2.VideoCapture(0)
    padding = 20
    # Read frame
    t = time.time()
    hasFrame, frame1 = cap.read()
    frameFace, bboxes = getFaceBox(faceNet, frame1)
        

    for bbox in bboxes:
        # print(bbox)
        face = frame1[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]
        genage = (gender+", "+age)         
        return (genage)
        


       
        #cv2.imwrite("age-gender-out-{}".format(args.input),frameFace)
def send_email(file_to_send):
    email = config['gmail']['from_email']
    password = config['gmail']['password']
    send_to_email = config['gmail']['send_to']
    subject = 'Unknown Person'
    message = 'An unknown person has entered the room. This person is {}.'.format(mygenage)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Setup the attachment
    filename = os.path.basename(file_to_send)
    attachment = open(file_to_send, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()


known_face_encodings = [] # will hold details of each face
known_face_names = [] # will hold names of each face

encoding_for_file = [] # Create an empty list for saving encoded files
known_dir = config['dir']['known_faces_dir']
for i in os.listdir(known_dir): # Loop over the folder to list individual files
    if i == '.DS_Store':
        continue
    filename = 0
    image = known_dir + i
    debug ('Reading {}'.format(image))
    image = face_recognition.load_image_file(image) # Run your load command
    image_encoding = face_recognition.face_encodings(image) # Run your encoding command
    known_face_encodings.append(image_encoding[0]) # Append the results to encoding_for_file list
    face_name, file_extension = os.path.splitext(i)
    known_face_names.append(face_name) # append name to known_faces

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

debug ('Starting video capture...')

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
       
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        #print (face_encodings)
        # Loop through the results 
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ("Unknown")
  
            # For each matched face, compute if it maps to a known face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]: # if its close to a known face
                name = known_face_names[best_match_index]
            face_names.append(name)
            now = datetime.now()
            mygenage = genderage()
            if (now >= future_time and "Unknown" in face_names) or (sent == False and "Unknown" in face_names):
                debug ('Unknown face found, now ({}) > future_time ({}) so sending out email and sms'.format(now, future_time))
                client.messages.create(to=to_phone, from_=from_phone, body="An unknown person has entered the room. This person is {}. Check your gmail for more info.").format(mygenage)
                cv2.imwrite(screenshot_dir,frame)
                send_email(file_to_send=screenshot_dir)
                sent = True
                future_time = now + timedelta (minutes=20)

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right + 140, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            if face_names:
                if mygenage == None:
                    mygenage = 'No face'
                print (name)
                print (mygenage)
                name = str(name+", "+mygenage)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            face_names = []
            face_locations = []



            

        # Display the resulting image
        cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # we are alternating process_this frame in each while iteration
    # what that means is every 2nd frame will be used
    #process_this_frame = not process_this_frame


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

