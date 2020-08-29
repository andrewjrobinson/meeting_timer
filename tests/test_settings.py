'''
Unit testing for Settings and SettingsWrapper classes
'''

import json
import os
import tempfile
import tkinter as tk
import unittest

from meeting_timer import settings


class TestSettingsWrapper(unittest.TestCase):
    '''Tests the SettingsWrapper class'''

    ## TESTS ##

    def test_getattr(self):
        s = settings.SettingsWrapper(None, {"test": "world"})
        self.assertEqual(s.test, "world", "s.test == 'world'")
        with self.assertRaises(KeyError):
            s.not_such_key
        
    def test_getitem(self):
        s = settings.SettingsWrapper(None, {"test": "world"})
        self.assertEqual(s['test'], "world", "s['test'] == 'world'")
        with self.assertRaises(KeyError):
            s['not_such_key']
        
    def test_get(self):
        s = settings.SettingsWrapper(None, {"test": "world"})
        self.assertEqual(s.get('test'), "world", "s.get('test') == 'world'")
        self.assertEqual(s.get('no_such_key', 'hello'), "hello", "s.get('no_such_key', 'hello') == 'hello'")
        
    def test_subitem(self):
        s = settings.SettingsWrapper(None, {"test": {"this": "that"}})
        self.assertEqual(s.test.this, 'that', "s.test.this == 'that'")
        with self.assertRaises(KeyError):
            self.assertEqual(s.test.not_such_key, 'that', "s.test.this == 'that'")

    def test_settings_root(self):
        s = settings.SettingsWrapper(None, {"test": {"this": "that"}})
        self.assertEqual(s.settings_root(), s, "s.settings_root == s")
        self.assertEqual(s.test.settings_root(), s, "s.settings_root == s")


class TestSettings(unittest.TestCase):
    '''Tests the Settings class'''

    ## TESTS ##

    def test_read(self):
        root = tk.Tk()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', prefix='meeting_', delete=False) as tmpfile:
            json.dump({"next": {"speaker": "Tom Thumb"}, "display": {"title": "NOT SET"}, "finished_text": "STOP!!!"}, tmpfile)
        s = settings.Settings(tmpfile.name)
        
        self.assertEqual(s.finished_text.get(), "STOP!!!", "s.finished_text.get() == 'STOP!!!'")
        self.assertEqual(s.display.title.get(), "", "s.display.title.get() == ''")
        
        if os.path.exists(tmpfile.name):
            os.unlink(tmpfile.name)
    
    def test_read_no_file(self):
        root = tk.Tk()
        s = settings.Settings()
        
        self.assertEqual(s.finished_text.get(), "STOP", "s.finished_text.get() == 'STOP'")
        with self.assertRaises(FileNotFoundError):
            s.read()
    
    def test_read_no_file2(self):
        root = tk.Tk()
        s = settings.Settings('no_such_file.json')
        
        with self.assertRaises(FileNotFoundError):
            s.read()
            
    def test_read_empty_file(self):
        root = tk.Tk()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', prefix='meeting_', delete=False) as tmpfile:
            pass
        s = settings.Settings(tmpfile.name)
        
        self.assertEqual(s.finished_text.get(), "STOP", "s.finished_text.get() == 'STOP'")
        
        if os.path.exists(tmpfile.name):
            os.unlink(tmpfile.name)
        
    def test_write_empty_file(self):
        root = tk.Tk()
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, 'meeting.json')
            s = settings.Settings()
            s.colour.primary.set("purple")
            s.write(filename)
            content = get_json_file(filename)
            self.assertEqual(content['colour']['primary'], "purple", "content['colour']['primary'] == 'purple'")
        
    def test_write_no_filename(self):
        root = tk.Tk()
        with tempfile.TemporaryDirectory() as tmpdir:
            s = settings.Settings()
            with self.assertRaises(FileNotFoundError):
                s.write()

def get_json_file(filename):
    '''
    '''
    with open(filename) as f:
        return json.load(f)


if __name__ == '__main__':
    unittest.main()



