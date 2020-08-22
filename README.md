# Meeting Timer

A simple application to allow you to keep your meetings or webinars running on
time.  

It has two modes:

* **Screen-share**: a window that contains the timer that you can screen share 
  on your video conferencing software.  This mode is useful for meetings where
  everyone attending should see the timer.
* **Webcam**: a virtual webcam stream that you can use instead of your real
  webcam to display the timer.  This mode is most-useful for webinars where you
  can share the timer with other presenters via your webcam which can be hidden
  from the regular participants by making it a webinar co-host.
  
**Table operating system (OS) support**:

| Mode         | Windows | MacOS     | Linux |
| ------------ |:-------:|:---------:|:-----:|
| Screen-share | Yes     | Yes       | Yes   |
| Webcam       | No (1)  | Maybe (2) | Yes   |

1) It currently doesn't support windows however If you are a developer and can 
   work out how to connect it I am happy to accept your pull-request to submit
   the code.
2) It is possible the Linux method might work for MacOS however I do not have 
   access to a MacOS computer to test it out.  If you do and successfully get it
   to work, please drop me a message (andrewjrobinson+mt at gmail.com).

## TO-DO list

Some features that I would like to add:

* Save configuration to file (JSON)
* Allow customisation of display (font-size, colours etc.)
* Allow full schedule of events to be specified ahead of time:
  * Manual advance to next speaker
  * Automatic advance
  * Display runtime difference from schedule (i.e. how late/early are you)
    * Display in configuration window (i.e. you only)
    * Progress bar to display meeting progress on timer output
* Import schedule from spreadsheet (CSV) OR pasted from clipboard (TSV)
* Webcam Support:
  * WindowsOS
  * MacOS

To be honest though, I may not get to implementing them since my main 
motiviation for creating this application (hosting a webinar) has passed (and 
this tool performed very well.

  
## Gifts / Motivation

If you like what I'm doing or think it helped you, feel free to gift me some 
motivation:

<style>.bmc-button img{height: 34px !important;width: 35px !important;
margin-bottom: 1px !important;box-shadow: none !important;
border: none !important;vertical-align: middle !important;}
.bmc-button{padding: 7px 15px 7px 10px !important;line-height: 35px !important;
height:51px !important;text-decoration: none !important;
display:inline-flex !important;color:#ffffff !important;
background-color:#FF5F5F !important;border-radius: 8px !important;
border: 1px solid transparent !important;font-size: 24px !important;
letter-spacing:0.6px !important;
box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;
-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;
margin: 0 auto !important;font-family:'Cookie', cursive !important;
-webkit-box-sizing: border-box !important;box-sizing: border-box !important;}
.bmc-button:hover, .bmc-button:active, .bmc-button:focus {
-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;
text-decoration: none !important;
box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;
opacity: 0.85 !important;color:#ffffff !important;}</style><link 
href="https://fonts.googleapis.com/css?family=Cookie" rel="stylesheet"><a 
class="bmc-button" target="_blank" 
href="https://www.buymeacoffee.com/andrewjrobinson"><img 
src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" 
alt="Buy me some motivation"><span 
style="margin-left:5px;font-size:24px !important;">Buy me some motivation</span></a> 

