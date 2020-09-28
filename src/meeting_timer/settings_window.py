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
import tkinter.ttk


class SettingsWindow(tk.Frame):
    '''
    Edit settings window
    '''
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.app = app
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.create_widgets()

    def create_widgets(self):
        
        self.tab_ctl = tk.ttk.Notebook(self)
        
        # display tab #
        self.tab_disp = tk.ttk.Frame(self.tab_ctl)
        
        self.fg_colour_label = tk.Label(self.tab_disp, text="Foreground Colour:", font="Arial 10 bold", anchor=tk.W)
        self.fg_colour_label.pack(side="top", expand=True, fill="x")
        self.fg_colour_entry = tk.Entry(self.tab_disp)
        self.fg_colour_entry["textvariable"] = self.app.settings.colour.primary
        self.fg_colour_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.warn_colour_label = tk.Label(self.tab_disp, text="Warning Colour:", font="Arial 10 bold", anchor=tk.W)
        self.warn_colour_label.pack(side="top", expand=True, fill="x")
        self.warn_colour_entry = tk.Entry(self.tab_disp)
        self.warn_colour_entry["textvariable"] = self.app.settings.colour.warning
        self.warn_colour_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.fin_colour_label = tk.Label(self.tab_disp, text="Finished Colour:", font="Arial 10 bold", anchor=tk.W)
        self.fin_colour_label.pack(side="top", expand=True, fill="x")
        self.fin_colour_entry = tk.Entry(self.tab_disp)
        self.fin_colour_entry["textvariable"] = self.app.settings.colour.finished
        self.fin_colour_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.bg_colour_label = tk.Label(self.tab_disp, text="Background Colour:", font="Arial 10 bold", anchor=tk.W)
        self.bg_colour_label.pack(side="top", expand=True, fill="x")
        self.bg_colour_entry = tk.Entry(self.tab_disp)
        self.bg_colour_entry["textvariable"] = self.app.settings.colour.background
        self.bg_colour_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.fin_text_label = tk.Label(self.tab_disp, text="Finished Text:", font="Arial 10 bold", anchor=tk.W)
        self.fin_text_label.pack(side="top", expand=True, fill="x")
        self.fin_text_entry = tk.Entry(self.tab_disp)
        self.fin_text_entry["textvariable"] = self.app.settings.finished_text
        self.fin_text_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.tab_ctl.add(self.tab_disp, text='Display')
        
        # initial tab #
        self.tab_init = tk.ttk.Frame(self.tab_ctl)
        
        self.init_title_label = tk.Label(self.tab_init, text="Title:", font="Arial 10 bold", anchor=tk.W)
        self.init_title_label.pack(side="top", expand=True, fill="x")
        self.init_title_entry = tk.Entry(self.tab_init)
        self.init_title_entry["textvariable"] = self.app.settings.initial.title
        self.init_title_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.init_time_label = tk.Label(self.tab_init, text="Time:", font="Arial 10 bold", anchor=tk.W)
        self.init_time_label.pack(side="top", expand=True, fill="x")
        self.init_time_entry = tk.Entry(self.tab_init)
        self.init_time_entry["textvariable"] = self.app.settings.initial.time
        self.init_time_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.init_speaker_label = tk.Label(self.tab_init, text="Speaker:", font="Arial 10 bold", anchor=tk.W)
        self.init_speaker_label.pack(side="top", expand=True, fill="x")
        self.init_speaker_entry = tk.Entry(self.tab_init)
        self.init_speaker_entry["textvariable"] = self.app.settings.initial.speaker
        self.init_speaker_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.init_width_label = tk.Label(self.tab_init, text="Width:", font="Arial 10 bold", anchor=tk.W)
        self.init_width_label.pack(side="top", expand=True, fill="x")
        self.init_width_entry = tk.Entry(self.tab_init)
        self.init_width_entry["textvariable"] = self.app.settings.initial.width
        self.init_width_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.init_height_label = tk.Label(self.tab_init, text="Height:", font="Arial 10 bold", anchor=tk.W)
        self.init_height_label.pack(side="top", expand=True, fill="x")
        self.init_height_entry = tk.Entry(self.tab_init)
        self.init_height_entry["textvariable"] = self.app.settings.initial.height
        self.init_height_entry.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        
        self.tab_ctl.add(self.tab_init, text='Initial')
        
        # pack tab ctrl
        self.tab_ctl.pack(side="top", expand = 1, fill ="both")
        
        # buttons
        self.update_btn = tk.Button(self, text="Update Background", command=self.app.update_bg_colour)
        self.update_btn.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        self.close_btn = tk.Button(self, text="Close", command=self.master.destroy)
        self.close_btn.pack(side="top", expand=True, fill="x", padx=1, pady=(0,1))
        







