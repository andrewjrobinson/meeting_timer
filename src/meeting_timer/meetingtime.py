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

import sys
import tkinter as tk

from meeting_timer.main_window import MainWindow


'''
Created on 15 Jul 2020

@author: arobinson
'''

def main(argv=sys.argv):
    '''Main entry point'''
    
    filename = None
    if len(argv) > 1:
        filename = argv[1]
    
    root = tk.Tk()
    root.geometry("240x600")
    app = MainWindow(master=root, filename=filename)
    app.mainloop()


if __name__ == '__main__':
    main(sys.argv)
    
