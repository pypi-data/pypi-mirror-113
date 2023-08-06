# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 14:38:43 2020

@author: LIM YUAN QING
"""

import sys

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk


import dd8
import dd8.utility.utils as utils

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)

def create_frame(master, *args, **kwargs):
    return tk.Frame(master, *args, **kwargs)

class App(tk.Tk):
    def __init__(self, str_name, str_title = '',  *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.name = str_name
        self.title(str_title)
        self.__dic_frames = dict()
        self.__main_frame = None   

    @property
    def name(self):
        return self.__str_name
    
    @name.setter
    def name(self, str_name):
        if isinstance(str_name, str):
            self.__str_name = str_name
        else:
            self.__str_name = str(str_name)

    @property
    def frames(self):
        return self.__dic_frames

    @property
    def main_frame(self):
        return self.__main_frame
    
    @main_frame.setter
    def main_frame(self, frame):
        if isinstance(frame, tk.Frame):
            self.__main_frame = frame
        else:
            logger.error('`main_frame` must be a `tk.Frame` object.')

    def add_frame(self, frame):
        if isinstance(frame, tk.Frame):
            self.__dic_frames[type(frame)] = frame
        else:
            logger.error(str(type(frame)) + ' is not a `tk.Frame object.')

    def add_icon(self, str_full_file_path):
        self.iconbitmap(str_full_file_path)

    def show_frame(self, frame):
        if type(frame) == type:
            frame = self.frames[frame]
        else:
            frame = self.frames[type(frame)]
        frame.tkraise()
        
class GenericWindowTemplate(tk.Frame):
    def __init__(self, app, master):
        super().__init__(master)        
    
    @property
    def children(self):
        return self.winfo_children()
    
    def add_label(self, *args, **kwargs):
        ttk.Label(self, *args, **kwargs)
    
    def add_button(self, *args, **kwargs):
        ttk.Button(self, *args, **kwargs)