import tkinter;from tkinter import ttk,messagebox,filedialog
from tkinter import *
class Window(tkinter.Tk):
    def top(self):
        self.wm_attributes('-topmost', 1)
    def canceltop(self):
        self.wm_attributes('-topmost',False)
    def always_focus_force(self,trueorfalse):
        if trueorfalse:
            self.Always_focus_value=self.after(1000,func=(lambda:self.focus_force()))
        else:
            self.after_cancel(self.Always_focus_value)
import inspect, re
class getinfo(object):
    def __init__(self,window):
        self.window=window
        self.name=self.getname()
        self.type=type(window)
    def getname(self):
        p=self.window
        self.getpname(p)
    def getpname(self,p):
        for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
            m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

