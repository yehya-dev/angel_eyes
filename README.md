# Angel Eyes
*MVP - Prototype*
## An App To Assist The Blind
### Tools
Web : Flask (Python 3.8)<br>
Database : MySQL<br>
Web UI : HTML, CSS, JS (duh!)<br>
Mobile : Android

### Abstract

**Angel Eyes** is a mobile application for the visually impaired and blind. This
application can be used by these people in delicate and confusing situations
such as finding the right path in the street or looking for an object in the house etc.

This can also provide blind people the ability to have a artificial intelligence
as a guide, that is, by filming their surroundings constantly to recognise objects around them and communicate the information to them via voice, a human volunteer can also help them if needed.

## Features
1. Caretaker To Manage The Blind
2. Face Recognition Of Known People
3. Blind's Live Location Always Available
4. Blind Can Contact Volunteer (Video Call) 
5. Emergency Help Via Phone Shake
6. Navigation Via Google Maps
7. Object Recogntion (COCO_DATASET)
8. Read Text (OCR)

## Note
Download the [yolo3.weights](https://pjreddie.com/media/files/yolov3.weights) file to the  `src/static/yolo` directory.

- run `python src/webservice.py` to start the apis.
- run `python src/app.py` to start the web interface. 

## Dependencies 
**Python**
- requests==2.22.0
- face_recognition==1.3.0
- opencv_python==4.5.2.54
- Flask==1.1.2
- numpy==1.19.5
- PyMySQL==1.0.2

**Android**
- junit:4.12
- runner:1.0.2
- espresso-core:3.0.2
- volley:1.1.0

