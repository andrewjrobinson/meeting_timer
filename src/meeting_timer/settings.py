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

import collections.abc
import json
import os
import tkinter as tk


class SettingsWrapper(object):
    '''
    Wraps settings sub-sections with standard interface
    '''
    
    def __init__(self, root=None, settings={}):
        '''
        Constructor
        '''
        if root is None:
            self._root = self
        else:
            self._root = root
        self.settings = settings
    
    def settings_root(self):
        '''
        Get the top level settings object
        '''
        return self._root
    
    def __getattr__(self, key):
        '''Attribute mapper (i.e. Object.key)'''
        return self.get(key)
    
    def __getitem__(self, key):
        '''Index mapper (i.e. Object['key'])'''
        return self.get(key)
    
    def get(self, key, default=None):
        '''
        Get the specified key
        '''
        if default is not None:
            result = self.settings.get(key, default)
        else:
            result = self.settings[key]
        if isinstance(result, collections.abc.Mapping):
            result = SettingsWrapper(self._root, result)
        return result

## end class SettingsWrapper() ##


class Settings(SettingsWrapper):
    '''
    Object for storing settings including writing-to/reading-from file
    '''
    
    def __init__(self, filename=None):
        '''
        Constructor
        
        @param filename: string, name of file to read-from/write-to
        '''
        SettingsWrapper.__init__(self, self, {
            "colour": {
                "background": tk.StringVar(value="black"),
                "finished": tk.StringVar(value="red"),
                "primary": tk.StringVar(value="green"),
                "warning": tk.StringVar(value="orange"),
            },
            "display": {
                "background": tk.StringVar(value="black"),
                "foreground": tk.StringVar(value="green"),
                "title": tk.StringVar(value=""),
                "time": tk.StringVar(value=""),
                "speaker": tk.StringVar(value=""),
            },
            "initial": {
                "duration": tk.IntVar(value=540),
                "title": tk.StringVar(value="My Webinar"),
                "time": tk.StringVar(value=""),
                "speaker": tk.StringVar(value="Welcome"),
                "warning": tk.IntVar(value=60),
                "width": tk.IntVar(value=1280),
                "height": tk.IntVar(value=720),
            },
            "next": {
                "duration": tk.IntVar(value=540),
                "speaker": tk.StringVar(value="John Smith"),
                "title": tk.StringVar(value="My Webinar"),
                "warning": tk.IntVar(value=60),
            },
            "finished_text": tk.StringVar(value="STOP")
        })
        self._filename = filename
        self._settings_loaded = False
    
    def get(self, key, default=None):
        '''
        Get a specific setting
        '''
        if not self._settings_loaded and self._filename is not None:
            self._settings_loaded = True
            self.read()
        return SettingsWrapper.get(self, key, default=default)
    
    def read(self, from_filename=None):
        '''
        Read settings from file
        '''
        # change filename if required
        if from_filename is not None:
            self._filename = from_filename
            
        # check filename is ok
        if self._filename is None:
            raise FileNotFoundError(f"Settings filename not provided")
        if not os.path.exists(self._filename):
            raise FileNotFoundError(f"Settings file does not exist ({self._filename})")
        
        # open file to read
        if os.path.getsize(self._filename) > 0:
            with open(self._filename, 'r') as f:
                content = json.load(f)
                self._read_setting_values(self.settings, content, ('display',))


    def write(self, as_filename=None):
        '''
        Writes settings to file, optionally as an alternate filename
        '''
        # change filename if required
        if as_filename is not None:
            self._filename = as_filename
        
        # check filename is ok
        if self._filename is None:
            raise FileNotFoundError(f"Settings filename not provided")
        
        # open file to write
        with open(self._filename, 'w+') as f:
            # convert to basic python types
            content = self._dump_setting_values(self.settings, ('display',))
            
            # write to file in json format
            json.dump(content, f, indent=2, sort_keys=True)


    def _read_setting_values(self, settings, values, ignore_keys=()):
        '''
        Tree-recursively load setting values
        '''
        for key,var in settings.items():
            if key not in ignore_keys:
                if isinstance(var, collections.abc.Mapping):
                    self._read_setting_values(var, values.get(key))
                elif values is not None:
                    var.set(values.get(key))


    def _dump_setting_values(self, settings, ignore_keys=()):
        '''
        Tree-recursively dump settings into regular python types 
        '''
        result = {}
        for key,var in settings.items():
            if key not in ignore_keys:
                if isinstance(var, collections.abc.Mapping):
                    result[key] = self._dump_setting_values(var)
                else:
                    result[key] = var.get()
        return result

## end class Settings() ##









