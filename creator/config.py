# -*- coding: utf-8 -*-
import os, sys
import os.path as osp
from PyQt4.QtGui import QLabel, QIcon, QPixmap, QFont, QFontDatabase
# Local import
from utils.userconfig import UserConfig, get_home_dir

DATA_DEV_PATH = osp.dirname(__file__)
DATA_PATH = DATA_DEV_PATH

SANS_SERIF = ['Sans Serif', 'DejaVu Sans', 'Bitstream Vera Sans',
              'Bitstream Charter', 'Lucida Grande', 'Verdana', 'Geneva',
              'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
SANS_SERIF.insert(0, unicode(QFont().family()))

MONOSPACE = ['Monospace', 'DejaVu Sans Mono', 'Courier New',
             'Bitstream Vera Sans Mono', 'Andale Mono', 'Liberation Mono',
             'Monaco', 'Courier', 'monospace', 'Fixed', 'Terminal']
MEDIUM = 11
SMALL = 9

App_Name = 'Creator'

DEFAULTS = [
            ('main',
             {
              'translation': True,
              'window/size' : (800, 600),
              'window/is_maximized' : False,
              'window/is_fullscreen' : False,
              'window/position' : (10, 10),
              'lightwindow/size' : (650, 400),
              'lightwindow/position' : (30, 30),
              }),
            ('editor',
             {
              'margins/backgroundcolor' : 'white',
              'margins/foregroundcolor' : 'darkGray',
              'foldmarginpattern/backgroundcolor' : 0xEEEEEE,
              'foldmarginpattern/foregroundcolor' : 0xEEEEEE,
              'printer_header/font/family': SANS_SERIF,
              'printer_header/font/size': MEDIUM,
              'printer_header/font/italic': False,
              'printer_header/font/bold': False,
              'shortcut': "Ctrl+Shift+E",
              'font/family' : MONOSPACE,
              'font/size' : MEDIUM,
              'font/italic' : False,
              'font/bold' : False,
              'wrap' : False,
              'wrapflag' : True,
              'code_analysis' : True,
              'class_browser' : True,
              'toolbox_panel' : True,
              'code_folding' : True,
              'check_eol_chars': True,
              'show_eol_chars' : False,
              'show_whitespace' : False,
              'tab_always_indent' : True,
              'api' : osp.join(DATA_PATH, 'python.api'),
              'max_recent_files' : 20,
              }),
            ('explorer',
             {
              'shortcut': "Ctrl+Shift+F",
              'enable': True,
              'wrap': True,
              'name_filters': ['*.py', '*.pyw', '*.pth',
                               '*.npy', '*.mat', '*.spydata'],
              'valid_filetypes': ['', '.py', '.pyw', '.spydata', '.npy', '.pth',
                                  '.txt', '.csv', '.mat', '.h5'],
              'show_hidden': True,
              'show_all': False,
              'show_toolbar': True,
              'show_icontext': True,
              }),
            ]
DEV = False
CONF = UserConfig('creator', defaults=DEFAULTS, load=(not DEV),
                  version='0.0.1',
                  subfolder='.config/creator' if os.name == 'posix' else '.creator')

def font_is_installed(font):
    """Check if font is installed"""
    return [fam for fam in QFontDatabase().families() if unicode(fam)==font]
    
def get_family(families):
    """Return the first installed font family in family list"""
    if not isinstance(families, list):
        families = [ families ]
    for family in families:
        if font_is_installed(family):
            return family
    else:
        print "Warning: None of the following fonts is installed: %r" % families
        return QFont().family()
        
FONT_CACHE = {}
def get_font(section, option=None):
    """Get console font properties depending on OS and user options"""
    font = FONT_CACHE.get((section, option))
    if font is None:
        if option is None:
            option = 'font'
        else:
            option += '/font'
        families = CONF.get(section, option+"/family", None)
        if families is None:
            return QFont()
        family = get_family( families )
        weight = QFont.Normal
        italic = CONF.get(section, option+'/italic', False)
        if CONF.get(section, option+'/bold', False):
            weight = QFont.Bold
        size = CONF.get(section, option+'/size', 9)
        font = QFont(family, size, weight)
        font.setItalic(italic)
        FONT_CACHE[(section, option)] = font
    return font

def set_font(font, section, option=None):
    """Set font"""
    if option is None:
        option = 'font'
    else:
        option += '/font'
    CONF.set(section, option+'/family', unicode(font.family()))
    CONF.set(section, option+'/size', float(font.pointSize()))
    CONF.set(section, option+'/italic', int(font.italic()))
    CONF.set(section, option+'/bold', int(font.bold()))
    FONT_CACHE[(section, option)] = font
    
SUPPORTED_EXT = ['.py', '.pyw', '.txt', '.xml', '.htm', '.html', '.js',
                 '.diff', '.patch', '.rej', '.css', '.h', '.c', '.cpp', '.hpp',
                 '.cxx', '.hxx', '.bat', '.cmd', '.properties', '.ini', '.java',
                 '.lua', '.yaml', '.sql', '.js']
def support_file(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext.lower() in SUPPORTED_EXT:
        return True
    return False
