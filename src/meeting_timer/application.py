#
# MIT License
# 
# Copyright (c) 2020 Andrew Robinson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import time
import tkinter as tk
import tkinter.filedialog

from meeting_timer.display_window import DisplayWindow
from meeting_timer.settings import Settings
from meeting_timer.main_window import MainWindow
from meeting_timer.webcam_output import WebcamOutput
import os


class Application(object):
    '''
    Main state management for the application
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        # setup tkinter
        self.master = tk.Tk()
    
    def main(self, argv):
        '''
        Main entry point into application
        '''
        
        # parse cli arguments
        filename = None
        if len(argv) > 1:
            filename = argv[1]
        
        # construct state
        self.settings = Settings(filename)
        
        # internal variables
        self.start_time = None
        self.pause_time = None
        self.duration = self.settings.initial.duration.get()
        self.warning = self.settings.initial.warning.get()
        self._last_colour = ''
        self._last_time = ''
        
        # copy initial values onto display
        self.settings.display.title.set(self.settings.initial.title.get())
        self.settings.display.time.set(self.settings.initial.time.get())
        self.settings.display.speaker.set(self.settings.initial.speaker.get())
        
        ## create output devices ##
        # display window
        self.display_window = tk.Toplevel(self.master)
        self.display_window.title('Meeting Timer')
        self.display_app = DisplayWindow(self.display_window, app=self)
        # webcam
        self.camera = WebcamOutput(self)
        
        # schedule display update
        self.master.after(100, self.update_timer)
        
        # create main window
        self.master.title('Meeting Timer - Control')
        self.master.geometry("240x600")
        app = MainWindow(master=self.master, app=self)
        
        # start event loop
        app.mainloop()
    
    
    def update_timer(self):
        '''
        Timer function that updates display at ~10fps
        '''
        
        if self.start_time is not None:
            
            # calculate time remaining
            if self.pause_time is not None:
                elapsed = self.pause_time - self.start_time
            else:
                elapsed = time.time() - self.start_time
            remaining = int(self.duration - elapsed)
            
            # update display colour
            colour = self.settings.colour.primary.get()
            if remaining <= self.warning:
                colour = self.settings.colour.warning.get()
            if colour != self._last_colour:
                self.settings.display.foreground.set(colour)
            self._last_colour = colour
            
            # update display text
            if int(remaining) <= 0:
                self.settings.display.foreground.set(self.settings.colour.finished.get())
                self.settings.display.time.set(self.settings.finished_text.get())
                self.start_time = None
                self.pause_time = None
            else:
                time_text = self._seconds_to_display(remaining)
                if time_text != self._last_time:
                    self.settings.display.time.set(time_text)
        
        # render image
        self.camera.schedule_frame()
        
        # schedule next display update
        self.master.after(100, self.update_timer)

    def open(self):
        '''
        Choose a file to open
        '''
        initial_dir = "~"
        filename = tk.filedialog.askopenfilename(initialdir=initial_dir,
                                                 title="Select file",
                                                 filetypes=(("meeting timer files","*.mt"),
                                                            ("all files","*.*")))
        self.settings.read(filename)

    def save(self):
        '''Save to file'''
        if self.settings._filename is None or not os.path.isfile(self.settings._filename):
            self.saveas()
        else:
            self.settings.write()
    
    def saveas(self):
        '''Save as new file'''
        initial_dir = "~"
        filename = tk.filedialog.asksaveasfilename(initialdir=initial_dir,
                                                   title="Select file",
                                                   filetypes=(("meeting timer files","*.mt"),
                                                              ("all files","*.*")))
        if filename is not None:
            self.settings.write(filename)

    
    def new(self):
        '''Clear '''
        raise NotImplementedError

    def start(self):
        if self.pause_time is not None:
            self.start_time += time.time() - self.pause_time
        else:
            self.start_time = time.time()
        self.pause_time = None
    
    def pause(self):
        if self.pause_time is None and self.start_time is not None:
            self.pause_time = time.time()
    
    def next(self):
        '''
        Move to next speaker
        '''
        self.stop()
        
        # update configuration
        self.duration = self.settings.next.duration.get()
        self.warning = self.settings.next.warning.get()
        
        # preload next speakers duration
        self.settings.display.foreground.set(self.settings.colour.primary.get())
        self.settings.display.title.set(self.settings.next.title.get())
        self.settings.display.speaker.set(self.settings.next.speaker.get())
        self.settings.display.time.set(self._seconds_to_display(self.duration))
        
    
    def stop(self):
        '''
        Stop timer and reset to 0
        '''
        self.start_time = None
        self.pause_time = None
        self.settings.display.time.set(self.settings.finished_text.get())
        self.settings.display.foreground.set(self.settings.colour.finished.get())
    
    def quit(self):
        '''
        Stop the application
        '''
        self.master.destroy()
    
    def add60(self):
        self.add(60)
    def minus60(self):
        self.add(-60)
    
    def add(self, duration):
        self.duration += duration
        
        
    
    def _seconds_to_display(self, duration):
        '''Formats a duration for display'''
        mins = int(duration / 60)
        sec = duration % 60
        return '%02d:%02d' % (mins, sec)
