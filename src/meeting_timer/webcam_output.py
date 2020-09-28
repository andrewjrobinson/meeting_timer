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

import platform
import glob
from meeting_timer import support

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

class WebcamOutput(object):
    '''
    Writes frames to loopback webcam
    '''
    
    def __init__(self, app):
        '''
        Constructor
        '''
        self.app = app
        self._camera = None
        self._running = True
        
        
        # trace colour and text value changes
        def update(*_):
            if self._camera is not None:
                self._update_webcam()
        self.app.settings.display.foreground.trace('w', update)
        self.app.settings.display.background.trace('w', update)
        self.app.settings.display.title.trace('w', update)
        self.app.settings.display.time.trace('w', update)
        self.app.settings.display.speaker.trace('w', update)
    
        # open webcam
        self._webcam_img = None
        self._img_width = 1280
        self._img_height = int(self._img_width*9/16)
        # find webcam
        if platform.system().lower() == "linux" and WEBCAM_SUPPORT:
            for dev in glob.glob('/dev/video*'):
                try:
                    self._camera = pyfakewebcam.FakeWebcam(dev, self._img_width, self._img_height)
                    break
                except:
                    pass
            if self._camera is None:
                print("No loopback web-cam found")
    
    def schedule_frame(self):
        '''
        Send current frame to webcam
        '''
        if self._webcam_img is not None and self._running:
            self._camera.schedule_frame(self._webcam_img)

    def _update_webcam(self):
        '''Updates image to render to webcam'''
        
        colour = self.app.settings.display.foreground.get()
        background = support.colour_to_tuple(self.app.settings.display.background.get())
        
        img = Image.new('RGB', (self._img_width, self._img_height, ), background)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", int(self._img_height/7))
        fontm = ImageFont.truetype("FreeMonoBold.otf", int(self._img_height/2))
        # font = ImageFont.load_default()
        
        # draw title text
        title_text = self.app.settings.display.title.get()
        w,_ = font.getsize(title_text)
        draw.text(((self._img_width-w)/2, 5), title_text, font=font, fill=colour)
        
        # draw time text
        time_text = self.app.settings.display.time.get()
        w,h = fontm.getsize(time_text)
        draw.text(((self._img_width-w)/2, (self._img_height-h)/2-15), time_text, font=fontm, fill=colour)
        
        # draw speaker text
        title_text = self.app.settings.display.speaker.get()
        w,_ = font.getsize(title_text)
        draw.text(((self._img_width-w)/2, self._img_height-15-int(self._img_height/7)), title_text, font=font, fill=colour)
        
        # create image
        self._webcam_img = np.array(img)
    
    
        