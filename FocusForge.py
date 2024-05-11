# imports
import tkinter as tk
import tkinter.messagebox as mb
import time as t

class FocusForge(tk.Tk):
  # create an instance of this class with a open window
  def __init__(self):
    tk.Tk.__init__(self)
    
    # create timer frame and place widgets in it
    self.focus_frame = tk.Frame(self)
    self.title("Focus Forge")
    self.focus_frame.grid(row=0, column=0, sticky="news")

    # show this authorization frame
    self.focus_frame.tkraise()
  
  def work_timer(num_mins):
    pass
  
  def break_timer():
    '''you guys code the timer and stuff'''
    tk.Tk.attributes('-fullscreen',True)
    '''timer end variable you guys need to create and stuff'''
    timer_end = True
    if timer_end:
      tk.Tk.attributes('-fullscreen', False)
