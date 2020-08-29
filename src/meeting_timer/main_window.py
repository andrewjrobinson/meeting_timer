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


import glob
import platform
import time
import tkinter as tk

from meeting_timer.display_window import DisplayWindow
from meeting_timer.settings import Settings

# platform specific imports
WEBCAM_SUPPORT=False
if platform.system().lower() == "linux":
    try:
        import pyfakewebcam
        import numpy as np
        from PIL import Image, ImageFont, ImageDraw
        WEBCAM_SUPPORT=True
    except ImportError:
        pass


class MainWindow(tk.Frame):
    '''
    Control window
    '''
    
    def __init__(self, master, filename, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self._last_colour = ''
        self._last_time = ''
        
        self.master = master
        self.master.title('Meeting Timer - Control')
        
        self._settings = Settings(filename)
        
        self.start_time = None
        self.pause_time = None
        self.duration = self._settings.initial.duration.get()
        self.warning = self._settings.initial.warning.get()
        self.finished_text = self._settings.initial.time.get()
        
        self.create_widgets()
        self.display_window = tk.Toplevel(self.master)
        self.display_window.title('Meeting Timer')
        
        # copy initial values onto display
        self._settings.display.title.set(self._settings.initial.title.get())
        self._settings.display.time.set(self._settings.initial.time.get())
        self._settings.display.speaker.set(self._settings.initial.speaker.get())
        
        self.display_app = DisplayWindow(self.display_window, settings=self._settings)
        
        self.pack()
        
        # open webcam
        self._webcam_img = None
        self._img_width = 1280
        self._img_height = int(self._img_width*9/16)
        # find webcam
        self._camera = None
        if platform.system().lower() == "linux" and WEBCAM_SUPPORT:
            for dev in glob.glob('/dev/video*'):
                try:
                    self._camera = pyfakewebcam.FakeWebcam(dev, self._img_width, self._img_height)
                    break
                except:
                    pass
            if self._camera is None:
                print("No loopback web-cam found")
        
        # trace colour and timer value
        def update_colour(*args):
            colour = self._settings.display.foreground.get()
            background = self._settings.display.background.get()
            time_text = self._settings.display.time.get()
            self.display_app.set_colours(fg=colour, bg=background)
            if self._camera is not None:
                self._update_webcam(time_text, colour)
        self._settings.display.foreground.trace('w', update_colour)
        self._settings.display.background.trace('w', update_colour)
        def update_text(*args):
            colour = self._settings.display.foreground.get()
#             background = self._settings.display.background.get()
            time_text = self._settings.display.time.get()
            if self._camera is not None:
                self._update_webcam(time_text, colour)
        self._settings.display.title.trace('w', update_text)
        self._settings.display.time.trace('w', update_text)
        self._settings.display.speaker.trace('w', update_text)
        
        self.master.after(100, self.update_timer)
        
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
            colour = self._settings.colour.primary.get()
            if remaining <= self.warning:
                colour = self._settings.colour.warning.get()
#             self.display_app.set_colours(fg=colour)
            if colour != self._last_colour:
                self._settings.display.foreground.set(colour)
            self._last_colour = colour
            
            # update display text
            if int(remaining) <= 0:
                self._settings.display.foreground.set(self._settings.colour.finished.get())
                self._settings.display.time.set(self._settings.finished_text.get())
                self.start_time = None
                self.pause_time = None
            else:
                time_text = self._seconds_to_display(remaining)
                if time_text != self._last_time:
                    self._settings.display.time.set(time_text)
        
        # render image
        if self._webcam_img is not None:
            self._camera.schedule_frame(self._webcam_img)
        
        self.master.after(100, self.update_timer)
    
    def _update_webcam(self, time_text, colour):
        '''Updates image to render to webcam'''
        
        
        img = Image.new('RGB', (self._img_width, self._img_height, ))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", int(self._img_height/7))
        fontm = ImageFont.truetype("FreeMonoBold.otf", int(self._img_height/2))
        # font = ImageFont.load_default()
        
        # draw title text
        title_text = self._settings.display.title.get()
        w,_ = font.getsize(title_text)
        draw.text(((self._img_width-w)/2, 5), title_text, font=font, fill=colour)
        
        # draw time text
        w,h = fontm.getsize(time_text)
        draw.text(((self._img_width-w)/2, (self._img_height-h)/2-15), time_text, font=fontm, fill=colour)
        
        # draw speaker text
        title_text = self._settings.display.speaker.get()
        w,_ = font.getsize(title_text)
        draw.text(((self._img_width-w)/2, self._img_height-15-int(self._img_height/7)), title_text, font=font, fill=colour)
        
        # create image
        self._webcam_img = np.array(img)
        
        
    
    def _seconds_to_display(self, duration):
        '''Formats a duration for display'''
        mins = int(duration / 60)
        sec = duration % 60
        return '%02d:%02d' % (mins, sec)

    def create_widgets(self):
        
        ## On-screen area ##
        self.current_frame = tk.LabelFrame(self, text="On-screen")
        
        self.current_title_label = tk.Label(self.current_frame, text="Title:", font="Arial 10 bold", anchor=tk.W)
        self.current_title_label.pack(side="top", expand=True, fill="x")
        self.current_title_entry = tk.Entry(self.current_frame)
        self.current_title_entry["textvariable"] = self._settings.display.title
        self.current_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_time_label = tk.Label(self.current_frame, text="Time:", font="Arial 10 bold", anchor=tk.W)
        self.current_time_label.pack(side="top", expand=True, fill="x")
        self.current_time_entry = tk.Entry(self.current_frame)
        self.current_time_entry["textvariable"] = self._settings.display.time
        self.current_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_speaker_label = tk.Label(self.current_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.current_speaker_label.pack(side="top", expand=True, fill="x")
        self.current_speaker_entry = tk.Entry(self.current_frame)
        self.current_speaker_entry["textvariable"] = self._settings.display.speaker
        self.current_speaker_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)
        
        ## Control area ##
        self.control_frame = tk.LabelFrame(self, text="Controls")
        
        self.next_btn = tk.Button(self.control_frame, text="Next", command=self.next, width=4)
        self.next_btn.grid(column=0, row=0)
        
        self.start_btn = tk.Button(self.control_frame, text="Start", command=self.start, width=4)
        self.start_btn.grid(column=1, row=0)
        
        self.pause_btn = tk.Button(self.control_frame, text="Pause", command=self.pause, width=4)
        self.pause_btn.grid(column=2, row=0)
        
        self.add60_btn = tk.Button(self.control_frame, text="+1m", command=self.add60, width=4)
        self.add60_btn.grid(column=0, row=1)
        
        self.minus60_btn = tk.Button(self.control_frame, text="-1m", command=self.minus60, width=4)
        self.minus60_btn.grid(column=1, row=1)
        
        self.stop_btn = tk.Button(self.control_frame, text="Stop", command=self.stop, fg='red', width=4)
        self.stop_btn.grid(column=2, row=1)
        
        self.control_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)
        
        ## Up next area ##
        self.next_frame = tk.LabelFrame(self, text="Up-next")
        
        self.next_title_label = tk.Label(self.next_frame, text="Title:", font="Arial 10 bold", anchor=tk.W)
        self.next_title_label.pack(side="top", expand=True, fill="x")
        self.next_title_entry = tk.Entry(self.next_frame)
        self.next_title_entry["textvariable"] = self._settings.next.title
        self.next_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_time_label = tk.Label(self.next_frame, text="Speaking time (total sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_time_label.pack(side="top", expand=True, fill="x")
        self.next_time_entry = tk.Entry(self.next_frame)
        self.next_time_entry["textvariable"] = self._settings.next.duration
        self.next_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_warn_label = tk.Label(self.next_frame, text="Warning time (last X sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_warn_label.pack(side="top", expand=True, fill="x")
        self.next_warn_entry = tk.Entry(self.next_frame)
        self.next_warn_entry["textvariable"] = self._settings.next.warning
        self.next_warn_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_speaker_label = tk.Label(self.next_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.next_speaker_label.pack(side="top", expand=True, fill="x")
        self.next_speaker_entry = tk.Entry(self.next_frame)
        self.next_speaker_entry["textvariable"] = self._settings.next.speaker
        self.next_speaker_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="top", expand=True, fill=tk.X)

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
        self.duration = self._settings.next.duration.get()
        self.warning = self._settings.next.warning.get()
        
        # preload next speakers duration
        self._settings.display.foreground.set(self._settings.colour.primary.get())
        self._settings.display.title.set(self._settings.next.title.get())
        self._settings.display.speaker.set(self._settings.next.speaker.get())
        self._settings.display.time.set(self._seconds_to_display(self.duration))
        
    
    def stop(self):
        '''
        Stop timer and reset to 0
        '''
        self.start_time = None
        self.pause_time = None
        self._settings.display.time.set(self.finished_text)
        self._settings.display.foreground.set(self._settings.colour.finished.get())
    
    def add60(self):
        self.add(60)
    def minus60(self):
        self.add(-60)
    
    def add(self, duration):
        self.duration += duration









