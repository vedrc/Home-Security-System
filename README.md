# Home Security System
## A project by Ved Roychowdhury

This program uses dlib face/age/gender recognition to create a home security system. I am a student at [Urbana Middle School](https://education.fcps.org/ums/home) and this is my first project in learning how to use machine learning for something useful. I plan to eventually port this code into a Raspberry Pi 4 with a pi cam and stick it close to our front door :-)

### Features

This program features facial recognition, age detection, and gender detection. Please note the system is not always 100% accurate :).
This also features an email system. More information is next.

### The Email System

The program will send an email when an Unknown person has been detected. If that person stays there for more than 20 minutes, it will send another one. Every 20 minutes the program will send one, if the person is still there. One problem is that if the unknown exits the frame, then comes back in, it will not send an email. Working on that in the next commit!

### How to use

I've put together all of the sensitive information in the `config.ini.sample` file. Please change the data in there, like the email,password, and path to folders. The age and gender models are all ok if you download or clone this project in the same structure. I originally had [Twilio](https://www.twilio.com) SMS on this, which I have made optional. It is on line 203 in detectface.py. If you
lost the line, here it is:

```python
client.messages.create(to=smsto, from_=smsfrom, body="An unknown person has entered the room. This person is {}. Check your gmail for more info.").format(mygenage)
```

## Requirements

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

## Downloading models
  You also need to download 2 large models into the `models` directory. I've removed them to save bandwidth.
  You can get them by doing:

  ```bash
    cd models
    wget https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/age_net.caffemodel 
    wget https://github.com/GilLevi/AgeGenderDeepLearning/raw/master/models/gender_net.caffemodel
  ```

 Each of them is pretty large, around 45M each.



### License
MIT License. Do whatever you want with it!

###


