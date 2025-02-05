# AFK Scroller

Tired of getting your keyboard or mouse all oily when you're trying to eat and read something at the same time?

Using the computer's webcam to view the user's hand, AFK Scroller allows you to read any page with hand gestures!

- Swipe up with Index Finger: Scrolls down to next page
- Swipe up with Middle Finger: Scrolls up to previous page

Technologies: Python, Numpy (Image Generation), Open CV2 API (camera control), Mediapipe API (hand tracking), Pynput (automate keyboard)

#### Show/Hide Camera

It starts up with camera on. To toggle between showing and hiding camera, press 1 and 2 on your keyboard, relatively.

#### Quit Program

While on the program's window, you can press 'q' to quit.

#### For Silicon Users

- Uncomment the mediapipe-silicon package in requirements.txt
- Follow these [instructions](https://pynput.readthedocs.io/en/latest/limitations.html) to allow pynput access to your keyboard on your mac

#### Python Version

Pleaseee switch to python 3.11 or lower, unfortunately mediapipe does not fully support python 3.12 and 3.13 yet 😔
