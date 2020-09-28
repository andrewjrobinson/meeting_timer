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

import tkinter as tk


class MainWindow(tk.Frame):
    '''
    Control window
    '''
    
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.app = app
#         self.settings = self.app.settings
        
        self.create_widgets()
        self.pack()
        
    

    def create_widgets(self):
        
        ## On-screen area ##
        self.current_frame = tk.LabelFrame(self, text="On-screen")
        
        self.current_title_label = tk.Label(self.current_frame, text="Title:", font="Arial 10 bold", anchor=tk.W)
        self.current_title_label.pack(side="top", expand=True, fill="x")
        self.current_title_entry = tk.Entry(self.current_frame)
        self.current_title_entry["textvariable"] = self.app.settings.display.title
        self.current_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_time_label = tk.Label(self.current_frame, text="Time:", font="Arial 10 bold", anchor=tk.W)
        self.current_time_label.pack(side="top", expand=True, fill="x")
        self.current_time_entry = tk.Entry(self.current_frame)
        self.current_time_entry["textvariable"] = self.app.settings.display.time
        self.current_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_speaker_label = tk.Label(self.current_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.current_speaker_label.pack(side="top", expand=True, fill="x")
        self.current_speaker_entry = tk.Entry(self.current_frame)
        self.current_speaker_entry["textvariable"] = self.app.settings.display.speaker
        self.current_speaker_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.current_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)
        
        ## Control area ##
        self.control_frame = tk.LabelFrame(self, text="Controls")
        
        self.next_btn = tk.Button(self.control_frame, text="Next", command=self.app.next, width=4)
        self.next_btn.grid(column=0, row=0)
        
        self.start_btn = tk.Button(self.control_frame, text="Start", command=self.app.start, width=4)
        self.start_btn.grid(column=1, row=0)
        
        self.pause_btn = tk.Button(self.control_frame, text="Pause", command=self.app.pause, width=4)
        self.pause_btn.grid(column=2, row=0)
        
        self.add60_btn = tk.Button(self.control_frame, text="+1m", command=self.app.add60, width=4)
        self.add60_btn.grid(column=0, row=1)
        
        self.minus60_btn = tk.Button(self.control_frame, text="-1m", command=self.app.minus60, width=4)
        self.minus60_btn.grid(column=1, row=1)
        
        self.stop_btn = tk.Button(self.control_frame, text="Stop", command=self.app.stop, fg='red', width=4)
        self.stop_btn.grid(column=2, row=1)
        
        self.open_btn = tk.Button(self.control_frame, text="Open", command=self.app.open, width=4)
        self.open_btn.grid(column=0, row=2)
        
        self.save_btn = tk.Button(self.control_frame, text="Save", command=self.app.save, width=4)
        self.save_btn.grid(column=1, row=2)
        
        self.saveas_btn = tk.Button(self.control_frame, text="Save as", command=self.app.saveas, width=4)
        self.saveas_btn.grid(column=2, row=2)
        
        self.control_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)
        
        ## Up next area ##
        self.next_frame = tk.LabelFrame(self, text="Up-next")
        
        self.next_title_label = tk.Label(self.next_frame, text="Title:", font="Arial 10 bold", anchor=tk.W)
        self.next_title_label.pack(side="top", expand=True, fill="x")
        self.next_title_entry = tk.Entry(self.next_frame)
        self.next_title_entry["textvariable"] = self.app.settings.next.title
        self.next_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_time_label = tk.Label(self.next_frame, text="Speaking time (total sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_time_label.pack(side="top", expand=True, fill="x")
        self.next_time_entry = tk.Entry(self.next_frame)
        self.next_time_entry["textvariable"] = self.app.settings.next.duration
        self.next_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_warn_label = tk.Label(self.next_frame, text="Warning time (last X sec):", font="Arial 10 bold", anchor=tk.W)
        self.next_warn_label.pack(side="top", expand=True, fill="x")
        self.next_warn_entry = tk.Entry(self.next_frame)
        self.next_warn_entry["textvariable"] = self.app.settings.next.warning
        self.next_warn_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_speaker_label = tk.Label(self.next_frame, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.next_speaker_label.pack(side="top", expand=True, fill="x")
        self.next_speaker_entry = tk.Entry(self.next_frame)
        self.next_speaker_entry["textvariable"] = self.app.settings.next.speaker
        self.next_speaker_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.next_frame.pack(padx=2, pady=2, expand=True, fill=tk.X)

        self.settings_btn = tk.Button(self, text="Settings...", command=self.app.show_settings)
        self.settings_btn.pack(side="top", expand=True, fill=tk.X)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.app.quit)
        self.quit.pack(side="top", expand=True, fill=tk.X)









