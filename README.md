# Home Security System
## A project by Ved Roychowdhury

This program uses dlib face/age/gender recognition to create a home security system.

###Features

This program features facial recognition, age detection, and gender detection. Please note the system is not always 100% accurate :).
This also features an email system. More information is next.

###The Email System

The program will send an email when an Unknown person has been detected. If that person stays there for more than 20 minutes, it will send another one. Every 20 minutes the program will send one, if the person is still there. One problem is that if the unknown exits the frame, then comes back in, it will not send an email. Working on that in the next commit!

###How to use

I've put together all of the sensitive information in the config.ini file. Please change the data in there, like the email, password, and path to folders. The age and gender models are all ok if you download or clone this project in the same structure. I originally had Twilio SMS on this, which I excluded. You are free to add it: (https://www.twilio.com). If you already have a Twilio account with a phone number and sms, you can add it to your Unknown notification script using this line of code:

```python
client.messages.create(to=smsto, from_=smsfrom, body="An unknown person has entered the room. This person is {}. Check your gmail for more info.").format(mygenage)
```

##Requirements
Ok, you need a lot of libraries for this project. The libraries are also listed in the detectface.py project, but I'll also list them here:
  * face_recognition
  * cv2
  * numpy
  * os
  * datetime (timedelta)
  * datetime
  * time
  * smtplib
  * configparser
  * mime
  * email
  * os.path
  * math

###License
MIT License. Do whatever you want with it!

###


