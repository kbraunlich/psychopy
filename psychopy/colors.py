#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from past.builtins import basestring
from psychopy.visual import basevisual as vis


def hex2rgb255(hexColor):
    """Convert a hex color string (e.g. "#05ff66") into an rgb triplet
    ranging from 0:255
    """
    col = vis.Color(hexColor)
    if len(hexColor.strip('#')) == 6:
        return col.rgb255
    elif len(hexColor.strip('#')) == 8:
        return col.rgba255


def isValidColor(color):
    """check color validity (equivalent to existing checks in _setColor)
    """
    col = vis.Color(color)
    if col.rgb:
        return True
    else:
        return False


"""140 colors defined by most modern browsers (originally the standard colors
of X11). Google for 140 web colors for further info"""
colors = {
    "aliceblue": (0.882352941176471, 0.945098039215686, 1),
    "antiquewhite": (0.96078431372549, 0.843137254901961, 0.686274509803922),
    "aqua": (-1, 1, 1),
    "aquamarine": (-0.00392156862745097, 1, 0.662745098039216),
    "azure": (0.882352941176471, 1, 1),
    "beige": (0.92156862745098, 0.92156862745098, 0.725490196078431),
    "bisque": (1, 0.788235294117647, 0.537254901960784),
    "black": (-1, -1, -1),
    "blanchedalmond": (1, 0.843137254901961, 0.607843137254902),
    "blue": (-1, -1, 1),
    "blueviolet": (0.0823529411764705, -0.662745098039216, 0.772549019607843),
    "brown": (0.294117647058824, -0.670588235294118, -0.670588235294118),
    "burlywood": (0.741176470588235, 0.443137254901961, 0.0588235294117647),
    "cadetblue": (-0.254901960784314, 0.23921568627451, 0.254901960784314),
    "chartreuse": (-0.00392156862745097, 1, -1),
    "chocolate": (0.647058823529412, -0.176470588235294, -0.764705882352941),
    "coral": (1, -0.00392156862745097, -0.372549019607843),
    "cornflowerblue": (-0.215686274509804, 0.168627450980392, 0.858823529411765),
    "cornsilk": (1, 0.945098039215686, 0.725490196078431),
    "crimson": (0.725490196078431, -0.843137254901961, -0.529411764705882),
    "cyan": (-1, 1, 1),
    "darkblue": (-1, -1, 0.0901960784313725),
    "darkcyan": (-1, 0.0901960784313725, 0.0901960784313725),
    "darkgoldenrod": (0.443137254901961, 0.0509803921568628, -0.913725490196078),
    "darkgray": (0.325490196078431, 0.325490196078431, 0.325490196078431),
    "darkgreen": (-1, -0.215686274509804, -1),
    "darkgrey": (0.325490196078431, 0.325490196078431, 0.325490196078431),
    "darkkhaki": (0.482352941176471, 0.435294117647059, -0.16078431372549),
    "darkmagenta": (0.0901960784313725, -1, 0.0901960784313725),
    "darkolivegreen": (-0.333333333333333, -0.16078431372549, -0.631372549019608),
    "darkorange": (1, 0.0980392156862746, -1),
    "darkorchid": (0.2, -0.607843137254902, 0.6),
    "darkred": (0.0901960784313725, -1, -1),
    "darksalmon": (0.827450980392157, 0.176470588235294, -0.0431372549019607),
    "darkseagreen": (0.12156862745098, 0.474509803921569, 0.12156862745098),
    "darkslateblue": (-0.435294117647059, -0.52156862745098, 0.0901960784313725),
    "darkslategray": (-0.631372549019608, -0.380392156862745, -0.380392156862745),
    "darkslategrey": (-0.631372549019608, -0.380392156862745, -0.380392156862745),
    "darkturquoise": (-1, 0.615686274509804, 0.63921568627451),
    "darkviolet": (0.16078431372549, -1, 0.654901960784314),
    "deeppink": (1, -0.843137254901961, 0.152941176470588),
    "deepskyblue": (-1, 0.498039215686275, 1),
    "dimgray": (-0.176470588235294, -0.176470588235294, -0.176470588235294),
    "dimgrey": (-0.176470588235294, -0.176470588235294, -0.176470588235294),
    "dodgerblue": (-0.764705882352941, 0.129411764705882, 1),
    "firebrick": (0.396078431372549, -0.733333333333333, -0.733333333333333),
    "floralwhite": (1, 0.96078431372549, 0.882352941176471),
    "forestgreen": (-0.733333333333333, 0.0901960784313725, -0.733333333333333),
    "fuchsia": (1, -1, 1),
    "gainsboro": (0.725490196078431, 0.725490196078431, 0.725490196078431),
    "ghostwhite": (0.945098039215686, 0.945098039215686, 1),
    "gold": (1, 0.686274509803922, -1),
    "goldenrod": (0.709803921568627, 0.294117647058824, -0.749019607843137),
    "gray": (0.00392156862745097, 0.00392156862745097, 0.00392156862745097),
    "grey": (0.00392156862745097, 0.00392156862745097, 0.00392156862745097),
    "green": (-1, 0.00392156862745097, -1),
    "greenyellow": (0.356862745098039, 1, -0.631372549019608),
    "honeydew": (0.882352941176471, 1, 0.882352941176471),
    "hotpink": (1, -0.176470588235294, 0.411764705882353),
    "indianred": (0.607843137254902, -0.27843137254902, -0.27843137254902),
    "indigo": (-0.411764705882353, -1, 0.0196078431372548),
    "ivory": (1, 1, 0.882352941176471),
    "khaki": (0.882352941176471, 0.803921568627451, 0.0980392156862746),
    "lavender": (0.803921568627451, 0.803921568627451, 0.96078431372549),
    "lavenderblush": (1, 0.882352941176471, 0.92156862745098),
    "lawngreen": (-0.0274509803921569, 0.976470588235294, -1),
    "lemonchiffon": (1, 0.96078431372549, 0.607843137254902),
    "lightblue": (0.356862745098039, 0.694117647058824, 0.803921568627451),
    "lightcoral": (0.882352941176471, 0.00392156862745097, 0.00392156862745097),
    "lightcyan": (0.756862745098039, 1, 1),
    "lightgoldenrodyellow": (0.96078431372549, 0.96078431372549, 0.647058823529412),
    "lightgray": (0.654901960784314, 0.654901960784314, 0.654901960784314),
    "lightgreen": (0.129411764705882, 0.866666666666667, 0.129411764705882),
    "lightgrey": (0.654901960784314, 0.654901960784314, 0.654901960784314),
    "lightpink": (1, 0.427450980392157, 0.513725490196078),
    "lightsalmon": (1, 0.254901960784314, -0.0431372549019607),
    "lightseagreen": (-0.749019607843137, 0.396078431372549, 0.333333333333333),
    "lightskyblue": (0.0588235294117647, 0.615686274509804, 0.96078431372549),
    "lightslategray": (-0.0666666666666667, 0.0666666666666667, 0.2),
    "lightslategrey": (-0.0666666666666667, 0.0666666666666667, 0.2),
    "lightsteelblue": (0.380392156862745, 0.537254901960784, 0.741176470588235),
    "lightyellow": (1, 1, 0.756862745098039),
    "lime": (-1, 1, -1),
    "limegreen": (-0.607843137254902, 0.607843137254902, -0.607843137254902),
    "linen": (0.96078431372549, 0.882352941176471, 0.803921568627451),
    "magenta": (1, -1, 1),
    "maroon": (0.00392156862745097, -1, -1),
    "mediumaquamarine": (-0.2, 0.607843137254902, 0.333333333333333),
    "mediumblue": (-1, -1, 0.607843137254902),
    "mediumorchid": (0.458823529411765, -0.333333333333333, 0.654901960784314),
    "mediumpurple": (0.152941176470588, -0.12156862745098, 0.717647058823529),
    "mediumseagreen": (-0.529411764705882, 0.403921568627451, -0.113725490196078),
    "mediumslateblue": (-0.0352941176470588, -0.184313725490196, 0.866666666666667),
    "mediumspringgreen": (-1, 0.96078431372549, 0.207843137254902),
    "mediumturquoise": (-0.435294117647059, 0.63921568627451, 0.6),
    "mediumvioletred": (0.56078431372549, -0.835294117647059, 0.0431372549019609),
    "midnightblue": (-0.803921568627451, -0.803921568627451, -0.12156862745098),
    "mintcream": (0.92156862745098, 1, 0.96078431372549),
    "mistyrose": (1, 0.788235294117647, 0.764705882352941),
    "moccasin": (1, 0.788235294117647, 0.419607843137255),
    "navajowhite": (1, 0.741176470588235, 0.356862745098039),
    "navy": (-1, -1, 0.00392156862745097),
    "oldlace": (0.984313725490196, 0.92156862745098, 0.803921568627451),
    "olive": (0.00392156862745097, 0.00392156862745097, -1),
    "olivedrab": (-0.16078431372549, 0.113725490196078, -0.725490196078431),
    "orange": (1, 0.294117647058824, -1),
    "orangered": (1, -0.458823529411765, -1),
    "orchid": (0.709803921568627, -0.12156862745098, 0.67843137254902),
    "palegoldenrod": (0.866666666666667, 0.819607843137255, 0.333333333333333),
    "palegreen": (0.192156862745098, 0.968627450980392, 0.192156862745098),
    "paleturquoise": (0.372549019607843, 0.866666666666667, 0.866666666666667),
    "palevioletred": (0.717647058823529, -0.12156862745098, 0.152941176470588),
    "papayawhip": (1, 0.874509803921569, 0.670588235294118),
    "peachpuff": (1, 0.709803921568627, 0.450980392156863),
    "peru": (0.607843137254902, 0.0431372549019609, -0.505882352941176),
    "pink": (1, 0.505882352941176, 0.592156862745098),
    "plum": (0.733333333333333, 0.254901960784314, 0.733333333333333),
    "powderblue": (0.380392156862745, 0.756862745098039, 0.803921568627451),
    "purple": (0.00392156862745097, -1, 0.00392156862745097),
    "red": (1, -1, -1),
    "rosybrown": (0.474509803921569, 0.12156862745098, 0.12156862745098),
    "royalblue": (-0.490196078431373, -0.176470588235294, 0.764705882352941),
    "saddlebrown": (0.0901960784313725, -0.458823529411765, -0.850980392156863),
    "salmon": (0.96078431372549, 0.00392156862745097, -0.105882352941176),
    "sandybrown": (0.913725490196079, 0.286274509803922, -0.247058823529412),
    "seagreen": (-0.63921568627451, 0.0901960784313725, -0.317647058823529),
    "seashell": (1, 0.92156862745098, 0.866666666666667),
    "sienna": (0.254901960784314, -0.356862745098039, -0.647058823529412),
    "silver": (0.505882352941176, 0.505882352941176, 0.505882352941176),
    "skyblue": (0.0588235294117647, 0.615686274509804, 0.843137254901961),
    "slateblue": (-0.168627450980392, -0.294117647058823, 0.607843137254902),
    "slategray": (-0.12156862745098, 0.00392156862745097, 0.129411764705882),
    "slategrey": (-0.12156862745098, 0.00392156862745097, 0.129411764705882),
    "snow": (1, 0.96078431372549, 0.96078431372549),
    "springgreen": (-1, 1, -0.00392156862745097),
    "steelblue": (-0.450980392156863, 0.0196078431372548, 0.411764705882353),
    "tan": (0.647058823529412, 0.411764705882353, 0.0980392156862746),
    "teal": (-1, 0.00392156862745097, 0.00392156862745097),
    "thistle": (0.694117647058824, 0.498039215686275, 0.694117647058824),
    "tomato": (1, -0.223529411764706, -0.443137254901961),
    "turquoise": (-0.498039215686275, 0.756862745098039, 0.631372549019608),
    "violet": (0.866666666666667, 0.0196078431372548, 0.866666666666667),
    "wheat": (0.92156862745098, 0.741176470588235, 0.403921568627451),
    "white": (1, 1, 1),
    "whitesmoke": (0.92156862745098, 0.92156862745098, 0.92156862745098),
    "yellow": (1, 1, -1),
    "yellowgreen": (0.207843137254902, 0.607843137254902, -0.607843137254902),
}
colorsHex = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9EA0',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8B',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred': '#CD5C5C',
    'indigo': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray': '#D3D3D3',
    'lightgreen': '#90EE90',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#F4A460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32'
}
colors255 = {
    "aliceblue": (240, 248, 255),
    "antiquewhite": (250, 235, 215),
    "aqua": (0, 255, 255),
    "aquamarine": (127, 255, 212),
    "azure": (240, 255, 255),
    "beige": (245, 245, 220),
    "bisque": (255, 228, 196),
    "black": (0, 0, 0),
    "blanchedalmond": (255, 235, 205),
    "blue": (0, 0, 255),
    "blueviolet": (138, 43, 226),
    "brown": (165, 42, 42),
    "burlywood": (222, 184, 135),
    "cadetblue": (95, 158, 160),
    "chartreuse": (127, 255, 0),
    "chocolate": (210, 105, 30),
    "coral": (255, 127, 80),
    "cornflowerblue": (100, 149, 237),
    "cornsilk": (255, 248, 220),
    "crimson": (220, 20, 60),
    "cyan": (0, 255, 255),
    "darkblue": (0, 0, 139),
    "darkcyan": (0, 139, 139),
    "darkgoldenrod": (184, 134, 11),
    "darkgray": (169, 169, 169),
    "darkgreen": (0, 100, 0),
    "darkgrey": (169, 169, 169),
    "darkkhaki": (189, 183, 107),
    "darkmagenta": (139, 0, 139),
    "darkolivegreen": (85, 107, 47),
    "darkorange": (255, 140, 0),
    "darkorchid": (153, 50, 204),
    "darkred": (139, 0, 0),
    "darksalmon": (233, 150, 122),
    "darkseagreen": (143, 188, 143),
    "darkslateblue": (72, 61, 139),
    "darkslategray": (47, 79, 79),
    "darkslategrey": (47, 79, 79),
    "darkturquoise": (0, 206, 209),
    "darkviolet": (148, 0, 211),
    "deeppink": (255, 20, 147),
    "deepskyblue": (0, 191, 255),
    "dimgray": (105, 105, 105),
    "dimgrey": (105, 105, 105),
    "dodgerblue": (30, 144, 255),
    "firebrick": (178, 34, 34),
    "floralwhite": (255, 250, 240),
    "forestgreen": (34, 139, 34),
    "fuchsia": (255, 0, 255),
    "gainsboro": (220, 220, 220),
    "ghostwhite": (248, 248, 255),
    "gold": (255, 215, 0),
    "goldenrod": (218, 165, 32),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
    "green": (0, 128, 0),
    "greenyellow": (173, 255, 47),
    "honeydew": (240, 255, 240),
    "hotpink": (255, 105, 180),
    "indianred": (205, 92, 92),
    "indigo": (75, 0, 130),
    "ivory": (255, 255, 240),
    "khaki": (240, 230, 140),
    "lavender": (230, 230, 250),
    "lavenderblush": (255, 240, 245),
    "lawngreen": (124, 252, 0),
    "lemonchiffon": (255, 250, 205),
    "lightblue": (173, 216, 230),
    "lightcoral": (240, 128, 128),
    "lightcyan": (224, 255, 255),
    "lightgoldenrodyellow": (250, 250, 210),
    "lightgray": (211, 211, 211),
    "lightgreen": (144, 238, 144),
    "lightgrey": (211, 211, 211),
    "lightpink": (255, 182, 193),
    "lightsalmon": (255, 160, 122),
    "lightseagreen": (32, 178, 170),
    "lightskyblue": (135, 206, 250),
    "lightslategray": (119, 136, 153),
    "lightslategrey": (119, 136, 153),
    "lightsteelblue": (176, 196, 222),
    "lightyellow": (255, 255, 224),
    "lime": (0, 255, 0),
    "limegreen": (50, 205, 50),
    "linen": (250, 240, 230),
    "magenta": (255, 0, 255),
    "maroon": (128, 0, 0),
    "mediumaquamarine": (102, 205, 170),
    "mediumblue": (0, 0, 205),
    "mediumorchid": (186, 85, 211),
    "mediumpurple": (147, 112, 219),
    "mediumseagreen": (60, 179, 113),
    "mediumslateblue": (123, 104, 238),
    "mediumspringgreen": (0, 250, 154),
    "mediumturquoise": (72, 209, 204),
    "mediumvioletred": (199, 21, 133),
    "midnightblue": (25, 25, 112),
    "mintcream": (245, 255, 250),
    "mistyrose": (255, 228, 225),
    "moccasin": (255, 228, 181),
    "navajowhite": (255, 222, 173),
    "navy": (0, 0, 128),
    "oldlace": (253, 245, 230),
    "olive": (128, 128, 0),
    "olivedrab": (107, 142, 35),
    "orange": (255, 165, 0),
    "orangered": (255, 69, 0),
    "orchid": (218, 112, 214),
    "palegoldenrod": (238, 232, 170),
    "palegreen": (152, 251, 152),
    "paleturquoise": (175, 238, 238),
    "palevioletred": (219, 112, 147),
    "papayawhip": (255, 239, 213),
    "peachpuff": (255, 218, 185),
    "peru": (205, 133, 63),
    "pink": (255, 192, 203),
    "plum": (221, 160, 221),
    "powderblue": (176, 224, 230),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "rosybrown": (188, 143, 143),
    "royalblue": (65, 105, 225),
    "saddlebrown": (139, 69, 19),
    "salmon": (250, 128, 114),
    "sandybrown": (244, 164, 96),
    "seagreen": (46, 139, 87),
    "seashell": (255, 245, 238),
    "sienna": (160, 82, 45),
    "silver": (192, 192, 192),
    "skyblue": (135, 206, 235),
    "slateblue": (106, 90, 205),
    "slategray": (112, 128, 144),
    "slategrey": (112, 128, 144),
    "snow": (255, 250, 250),
    "springgreen": (0, 255, 127),
    "steelblue": (70, 130, 180),
    "tan": (210, 180, 140),
    "teal": (0, 128, 128),
    "thistle": (216, 191, 216),
    "tomato": (255, 99, 71),
    "turquoise": (64, 224, 208),
    "violet": (238, 130, 238),
    "wheat": (245, 222, 179),
    "white": (255, 255, 255),
    "whitesmoke": (245, 245, 245),
    "yellow": (255, 255, 0),
    "yellowgreen": (154, 205, 50),
}
