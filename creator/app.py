# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
views = None

menus = [
    { 'text': 'Creator',
      'menus': ['file_new', 'file_open', 'separator', 'file_exit']    
    },
    { 'text': 'Editor',
      'menus': []    
    },
    { 'text': 'Source',
      'menus': []    
    },
    { 'text': 'Help',
      'menus': []    
    },
]

actions = {
    'file_open':{
        'icon': '',
        'text': u'Open Source File',
        'shortcut': Qt.CTRL | Qt.Key_O,
        'tip': u'',
    },
    'file_new':{
        'icon': '',
        'text': u'New Source File',
        'shortcut': Qt.CTRL | Qt.Key_N,
        'tip': u'',
    },
    'file_exit':{
        'icon': '',
        'text': u'Exit',
        'shortcut': Qt.CTRL | Qt.Key_Q,
        'tip': u'',
    }
}


class Consts:
    icon_run = ':/creator/images/run.png'
    icon_run_small = ':/creator/images/run_small.png'
    icon_run_section = ':/creator/images/run.png'
    icon_run_section_small = ':/creator/images/run_small.png'
    icon_debug = ':/creator/images/debugger_start.png'
    icon_debug_small = ':/creator/images/debugger_start_small.png'
