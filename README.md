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
  
**Table**: operating system (OS) support:

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

## Documentation

* [Install Guide](docs/README.md)
* [User Guide](docs/user-guide/README.md)

## TO-DO list

Some features that I would like to add:

* Allow customisation of display (font-size, ~~colours~~ [done] etc.)
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
* ~~Save configuration to file (JSON)~~ [done]
* ~~Settings dialog~~ [done]

To be honest though, I may not get to implementing these since my main 
motiviation for creating this application (hosting a webinar) has passed (and 
this tool performed very well).

If you have other ideas please contact me so I can add them to the list and 
hopefully get time to implement them at some point.

If you have the skills/time to implement the Windows/Mac version of webcam 
mode please get in contact so we can work together to get it implemented.
  
## Gifts / Motivation

If you like what I'm doing or think it helped you, feel free to gift me some 
motivation:

<a href="https://www.buymeacoffee.com/andrewjrobinson" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 51px !important;width: 217px !important;" ></a>

