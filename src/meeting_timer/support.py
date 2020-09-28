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


import re

HTML_CODE_RE3 = r'^#?([a-f0-9])([a-f0-9])([a-f0-9])$'
HTML_CODE_RE6 = r'^#?([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})$'

def colour_to_html(colour, default="#ffffff"):
    '''Force a colour into HTML hash notation'''
    
    # strip formatting
    colour = str(colour).lower().replace(' ', '').replace('-', '').strip()
    
    # replace named colour codes
    if colour in _named_html_colours:
        colour = _named_html_colours[colour]
    
    # check value matches html notation
    if not re.match(HTML_CODE_RE3, colour) and not re.match(HTML_CODE_RE6, colour):
        colour = default

    # check value starts with #
    elif not colour.startswith('#'):
        colour = f'#{colour}'
    
    return colour
    

def colour_to_tuple(colour, default="#ffffff"):
    '''Force a colour into RGB tuple'''
    
    # convert to html format
    colour = str(colour_to_html(colour, default)).lower()
    
    # try 6-diget html code
    match =  re.match(HTML_CODE_RE6, colour)
    if match:
        match = match.groups()
    else:
        # try 3-digit html code
        match = re.match(HTML_CODE_RE3, colour)
        if match:
            match = map(lambda h: f'{h}{h}', match.groups())
        else:
            # give up
            raise RuntimeError(f'Invalid colour: "{colour}"')
    
    # convert to decimal tuple
    return tuple(map(lambda h: int(h, 16), match))
        
    


_named_html_colours = {
    "mediumvioletred": "#c71585",
    "deeppink": "#ff1493",
    "palevioletred": "#db7093",
    "hotpink": "#ff69b4",
    "lightpink": "#ffb6c1",
    "pink": "#ffc0cb",
    "darkred": "#8b0000",
    "red": "#ff0000",
    "firebrick": "#b22222",
    "crimson": "#dc143c",
    "indianred": "#cd5c5c",
    "lightcoral": "#f08080",
    "salmon": "#fa8072",
    "darksalmon": "#e9967a",
    "lightsalmon": "#ffa07a",
    "orangered": "#ff4500",
    "tomato": "#ff6347",
    "darkorange": "#ff8c00",
    "coral": "#ff7f50",
    "orange": "#ffa500",
    "darkkhaki": "#bdb76b",
    "gold": "#ffd700",
    "khaki": "#f0e68c",
    "peachpuff": "#ffdab9",
    "yellow": "#ffff00",
    "palegoldenrod": "#eee8aa",
    "moccasin": "#ffe4b5",
    "papayawhip": "#ffefd5",
    "lightgoldenrodyellow": "#fafad2",
    "lemonchiffon": "#fffacd",
    "lightyellow": "#ffffe0",
    "maroon": "#800000",
    "brown": "#a52a2a",
    "saddlebrown": "#8b4513",
    "sienna": "#a0522d",
    "chocolate": "#d2691e",
    "darkgoldenrod": "#b8860b",
    "peru": "#cd853f",
    "rosybrown": "#bc8f8f",
    "goldenrod": "#daa520",
    "sandybrown": "#f4a460",
    "tan": "#d2b48c",
    "burlywood": "#deb887",
    "wheat": "#f5deb3",
    "navajowhite": "#ffdead",
    "bisque": "#ffe4c4",
    "blanchedalmond": "#ffebcd",
    "cornsilk": "#fff8dc",
    "darkgreen": "#006400",
    "green": "#008000",
    "darkolivegreen": "#556b2f",
    "forestgreen": "#228b22",
    "seagreen": "#2e8b57",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "mediumseagreen": "#3cb371",
    "limegreen": "#32cd32",
    "lime": "#00ff00",
    "springgreen": "#00ff7f",
    "mediumspringgreen": "#00fa9a",
    "darkseagreen": "#8fbc8f",
    "mediumaquamarine": "#66cdaa",
    "yellowgreen": "#9acd32",
    "lawngreen": "#7cfc00",
    "chartreuse": "#7fff00",
    "lightgreen": "#90ee90",
    "greenyellow": "#adff2f",
    "palegreen": "#98fb98",
    "teal": "#008080",
    "darkcyan": "#008b8b",
    "lightseagreen": "#20b2aa",
    "cadetblue": "#5f9ea0",
    "darkturquoise": "#00ced1",
    "mediumturquoise": "#48d1cc",
    "turquoise": "#40e0d0",
    "aqua": "#00ffff",
    "cyan": "#00ffff",
    "aquamarine": "#7fffd4",
    "paleturquoise": "#afeeee",
    "lightcyan": "#e0ffff",
    "navy": "#000080",
    "darkblue": "#00008b",
    "mediumblue": "#0000cd",
    "blue": "#0000ff",
    "midnightblue": "#191970",
    "royalblue": "#4169e1",
    "steelblue": "#4682b4",
    "dodgerblue": "#1e90ff",
    "deepskyblue": "#00bfff",
    "cornflowerblue": "#6495ed",
    "skyblue": "#87ceeb",
    "lightskyblue": "#87cefa",
    "lightsteelblue": "#b0c4de",
    "lightblue": "#add8e6",
    "powderblue": "#b0e0e6",
    "indigo": "#4b0082",
    "purple": "#800080",
    "darkmagenta": "#8b008b",
    "darkviolet": "#9400d3",
    "darkslateblue": "#483d8b",
    "blueviolet": "#8a2be2",
    "darkorchid": "#9932cc",
    "fuchsia": "#ff00ff",
    "magenta": "#ff00ff",
    "slateblue": "#6a5acd",
    "mediumslateblue": "#7b68ee",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "orchid": "#da70d6",
    "violet": "#ee82ee",
    "plum": "#dda0dd",
    "thistle": "#d8bfd8",
    "lavender": "#e6e6fa",
    "mistyrose": "#ffe4e1",
    "antiquewhite": "#faebd7",
    "linen": "#faf0e6",
    "beige": "#f5f5dc",
    "whitesmoke": "#f5f5f5",
    "lavenderblush": "#fff0f5",
    "oldlace": "#fdf5e6",
    "aliceblue": "#f0f8ff",
    "seashell": "#fff5ee",
    "ghostwhite": "#f8f8ff",
    "honeydew": "#f0fff0",
    "floralwhite": "#fffaf0",
    "azure": "#f0ffff",
    "mintcream": "#f5fffa",
    "snow": "#fffafa",
    "ivory": "#fffff0",
    "white": "#ffffff",
    "black": "#000000",
    "darkslategray": "#2f4f4f",
    "dimgray": "#696969",
    "slategray": "#708090",
    "gray": "#808080",
    "lightslategray": "#778899",
    "darkgray": "#a9a9a9",
    "silver": "#c0c0c0",
    "lightgray": "#d3d3d3",
    "gainsboro": "#dcdcdc",
}
