# User Guide

## Control Window

Allows you to control the count-down timer

![Control Window](./user-guide/control-window.png)

**Figure**: The control window is divided up into 3 sections: 1) On-screen, 2) Controls and 3) Up-next.

The on-screen section controls the values that are displayed on screen at the time.  You can edit these 
values and they will update as you type.  Note: if the timer is running the time field will get overridden.

The Controls section allows you to control the action of the timer:

* **Next**: button will take the values from the up-next section and load them into the on-screen section and
  preset the time to the speeking time value.  Note: the timer will not start until you click *Start*
* **Start**: begins the count down process.
* **Pause**: pauses the count down process.  Click the *Start* button to resume.
* **+1m**: adds 1 minute to the count down time.
* **-1m**: removes 1 minute from the count down time.
* **Stop**: ends the count down process and sets time to 0

The up-next section is used to set the timer configuration when the next speaker is up.  The Title and Speaker fields update the 
corresponding value in the on-screen section when you press *Next* button.  The speaking time is converted from seconds to MM:SS
format and put into the Time field.  Warning time is used to switch the colour of the timer to Orange when timer reaches this number 
of seconds remaining.

The Quit button is used to exit the application and will close all other windows (and stop publishing to virtual webcam)

## Screen-share window

The screen-share window shows the count down timer and is the window that you share with your participants to show them the timer.

![Share-screen Window](./user-guide/share-screen.png)

**Figure**: The share-screen window is divided up into 3 sections 1) title, 2) time, and 3) speaker; their current value is set 
by the corresponding textboxes on the Control window's *on-screen* section.

![Share-screen Window - Warning mode](./user-guide/share-screen-warning.png)

**Figure**: when the timer reaches the *warning* threshold (default 60 seconds) it switches colour to orange

![Share-screen Window](./user-guide/share-screen-finished.png)

**Figure**: when the timer reaches the end, it switches colour to red.

## Webcam output

When you use a supported Operating System (currently Linux) and have the required dependencies installed and configured, *meeting-timer* 
will output video frames to the first available virtual webcam device.  You can then configure your video-conference application (such as 
Zoom (R)) to use the virtual webcam to display the timer instead of your regular webcam.  This mode is useful when you need to share to
only presenters in a webminar or need to also share a different screen in a regular meeting.

![Webcam mode](./user-guide/webcam-mode.png)

**Figure**: the webcam output showing up in the Zoom (R) video conferencing application over the top of the share-screen and control
windows
