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
from meeting_timer import support


class DisplayWindow(tk.Frame):
    '''
    Share-screen window
    '''
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, bg="black", *args, **kwargs)
        self.master = master
        self.app = app
        self.pack(fill=tk.BOTH, expand=tk.YES)
        self.create_widgets()
#         master.attributes('-zoomed', True)

        # watch for colour updates
        def update_colour(*args):
            colour = self.app.settings.display.foreground.get()
            background = self.app.settings.display.background.get()
            self.set_colours(fg=colour, bg=background)
        self.app.settings.display.foreground.trace('w', update_colour)
        self.app.settings.display.background.trace('w', update_colour)

    def create_widgets(self):
        self.title_label = tk.Label(self, fg="green", bg="black")
        self.title_label["textvariable"] = self.app.settings.display.title
        self.title_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.title_label.config(font=("Arial", 64))
        
        self.timer_label = tk.Label(self, fg="green", bg="black")
        self.timer_label["textvariable"] = self.app.settings.display.time
        self.timer_label.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.timer_label.config(font=("Courier Bold", 256))
        
        self.speaker_label = tk.Label(self, fg="green", bg="black")
        self.speaker_label["textvariable"] = self.app.settings.display.speaker
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
            bg = support.colour_to_html(bg)
            self.title_label.config(bg=bg)
            self.timer_label.config(bg=bg)
            self.speaker_label.config(bg=bg)







