#!/usr/bin/env python3
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
import sys
import time
import tkinter as tk

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
    

'''
Created on 15 Jul 2020

@author: arobinson
'''

def main(argv=sys.argv):
    '''Main entry point'''
    
    root = tk.Tk()
    root.geometry("240x600")
    app = Application(master=root)
    app.mainloop()


class Application(tk.Frame):
    '''
    Control application window
    '''
    
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self._last_colour = ''
        self._last_time = ''
        
        self.master = master
        self.master.title('Meeting Timer - Control')
        
        self.display_variables = {
            'title': tk.StringVar(value="My Webinar"),
            'time': tk.StringVar(value=""),
            'fgcolour': tk.StringVar(value="green"),
#             'bgcolour': tk.StringVar(value="black"),
            'speaker': tk.StringVar(value="Welcome"),
        }
        
        self.application_variables = {
            'title': tk.StringVar(value="My Webinar"),
            'duration': tk.IntVar(value=540),
            'warning': tk.IntVar(value=60),
            'speaker': tk.StringVar(value="John Smith"),
        }
        
        self.start_time = None
        self.pause_time = None
        self.duration = 540 # seconds (5m = 300)
        self.warning = 60 # seconds
        self.finished_text = "00:00"
        self.colours = {
            'primary': 'green',
            'warning': 'orange',
            'finished': 'red',
            'background':  'black',
        }
        
        self.create_widgets()
        self.display_window = tk.Toplevel(self.master)
        self.display_window.title('Meeting Timer')
        
        self.display_app = DisplayWindow(self.display_window, variables=self.display_variables)
        
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
            colour = self.display_variables['fgcolour'].get()
            time_text = self.display_variables['time'].get()
            self.display_app.set_colours(fg=colour)
            if self._camera is not None:
                self._update_webcam(time_text, colour)
        self.display_variables['fgcolour'].trace('w', update_colour)
        def update_text(*args):
            colour = self.display_variables['fgcolour'].get()
            time_text = self.display_variables['time'].get()
            if self._camera is not None:
                self._update_webcam(time_text, colour)
        self.display_variables['title'].trace('w', update_text)
        self.display_variables['time'].trace('w', update_text)
        self.display_variables['speaker'].trace('w', update_text)
        
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
            colour = self.colours['primary']
            if remaining <= self.warning:
                colour = self.colours['warning']
#             self.display_app.set_colours(fg=colour)
            if colour != self._last_colour:
                self.display_variables['fgcolour'].set(colour)
            self._last_colour = colour
            
            # update display text
            if int(remaining) <= 0:
#                 self.display_app.set_colours(fg=self.colours['finished'])
                self.display_variables['fgcolour'].set(self.colours['finished'])
                self.display_variables['time'].set(self.finished_text)
#                 self._update_webcam(self.finished_text, colour)
                self.start_time = None
                self.pause_time = None
            else:
                time_text = self._seconds_to_display(remaining)
                if time_text != self._last_time:
                    self.display_variables['time'].set(time_text)
#                 self._update_webcam(time_text, colour)
        
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
        title_text = self.display_variables['title'].get()
        w,_ = font.getsize(title_text)
        draw.text(((self._img_width-w)/2, 5), title_text, font=font, fill=colour)
        
        # draw time text
        w,h = fontm.getsize(time_text)
        draw.text(((self._img_width-w)/2, (self._img_height-h)/2-15), time_text, font=fontm, fill=colour)
        
        # draw speaker text
        title_text = self.display_variables['speaker'].get()
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
        self.current_title_entry["textvariable"] = self.display_variables['title']
        self.current_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_time_label = tk.Label(self.current_frame, text="Time:", font="Arial 10 bold", anchor=tk.W)
        self.current_time_label.pack(side="top", expand=True, fill="x")
        self.current_time_entry = tk.Entry(self.current_frame)
        self.current_time_entry["textvariable"] = self.display_variables['time']
        self.current_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_speaker_label = tk.Label(self.current_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.current_speaker_label.pack(side="top", expand=True, fill="x")
        self.current_speaker_entry = tk.Entry(self.current_frame)
        self.current_speaker_entry["textvariable"] = self.display_variables['speaker']
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
        self.next_title_entry["textvariable"] = self.application_variables['title']
        self.next_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_time_label = tk.Label(self.next_frame, text="Speaking time (total sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_time_label.pack(side="top", expand=True, fill="x")
        self.next_time_entry = tk.Entry(self.next_frame)
        self.next_time_entry["textvariable"] = self.application_variables['duration']
        self.next_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_warn_label = tk.Label(self.next_frame, text="Warning time (last X sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_warn_label.pack(side="top", expand=True, fill="x")
        self.next_warn_entry = tk.Entry(self.next_frame)
        self.next_warn_entry["textvariable"] = self.application_variables['warning']
        self.next_warn_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_speaker_label = tk.Label(self.next_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.next_speaker_label.pack(side="top", expand=True, fill="x")
        self.next_speaker_entry = tk.Entry(self.next_frame)
        self.next_speaker_entry["textvariable"] = self.application_variables['speaker']
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
        self.duration = self.application_variables['duration'].get()
        self.warning = self.application_variables['warning'].get()
        
        # preload next speakers duration
#         self.display_app.set_colours(self.colours['primary'], self.colours['background'])
        self.display_variables['fgcolour'].set(self.colours['primary'])
        self.display_variables['title'].set(self.application_variables['title'].get())
        self.display_variables['speaker'].set(self.application_variables['speaker'].get())
        self.display_variables['time'].set(self._seconds_to_display(self.duration))
#         self._update_webcam(self._seconds_to_display(self.duration), self.colours['primary'])
        
    
    def stop(self):
        '''
        Stop timer and reset to 0
        '''
        self.start_time = None
        self.pause_time = None
        self.display_variables['time'].set(self.finished_text)
#         self._update_webcam(self.finished_text, self.colours['finished'])
#         self.display_app.set_colours(self.colours['finished'], self.colours['background'])
        self.display_variables['fgcolour'].set(self.colours['finished'])
    
    def add60(self):
        self.add(60)
    def minus60(self):
        self.add(-60)
    
    def add(self, duration):
        self.duration += duration

class DisplayWindow(tk.Frame):
    '''
    Share-screen window
    '''
    def __init__(self, master=None, variables={}, *args, **kwargs):
        super().__init__(master, bg="black", *args, **kwargs)
        self.master = master
        self.variables = variables
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.create_widgets()
#         master.attributes('-zoomed', True)

    def create_widgets(self):
        self.title_label = tk.Label(self, fg="green", bg="black")
        if 'title' in self.variables:
            self.title_label["textvariable"] = self.variables['title']
        self.title_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.title_label.config(font=("Arial", 64))
        
        self.timer_label = tk.Label(self, fg="green", bg="black")
        if 'time' in self.variables:
            self.timer_label["textvariable"] = self.variables['time']
        self.timer_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.timer_label.config(font=("Courier Bold", 256))
        
        self.speaker_label = tk.Label(self, fg="green", bg="black")
        if 'speaker' in self.variables:
            self.speaker_label["textvariable"] = self.variables['speaker']
        self.speaker_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.speaker_label.config(font=("Arial", 64))

    def set_colours(self, fg=None, bg=None):
        '''
        Set the display colours
        '''
        if fg is not None:
            self.title_label.config(fg=fg)
            self.timer_label.config(fg=fg)
            self.speaker_label.config(fg=fg)
        if bg is not None:
            self.title_label.config(bg=bg)
            self.timer_label.config(bg=bg)
            self.speaker_label.config(bg=bg)
            


if __name__ == '__main__':
    main(sys.argv)
    
