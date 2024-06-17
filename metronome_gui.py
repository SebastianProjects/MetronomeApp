import math
import tkinter
import customtkinter as ctk
import time
from tkinter import messagebox as msgbox
from metronome import Metronome

ctk.set_default_color_theme("blue") 

class MetronomeGUI():
    
    def __init__(self):
        
        self.__win = ctk.CTk()
        self.__win.geometry("1040x280")
        self.__win.minsize(1040, 280)
        self.__win.maxsize(1040, 280)
        self.__win.title("Metronome")
        
        self.__win.grid_columnconfigure(0, weight=1)
        self.__win.grid_columnconfigure(1, weight=0)
        
        self.__win.grid_rowconfigure(0, weight=1)
        
        
        self.__frame_left = ctk.CTkFrame(self.__win)
        self.__frame_left.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew")
        
        self.__frame_right = ctk.CTkFrame(self.__win)
        self.__frame_right.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "nsew")
        
        
        # LEFT FRAME
        
        self.__frame_left.grid_columnconfigure(0, weight=1)
        self.__frame_left.grid_rowconfigure(0, weight=0)
        self.__frame_left.grid_rowconfigure(1, weight=0)
        self.__frame_left.grid_rowconfigure(2, weight=1)
        
        # TODO: Bindnut sipky pre posuvanie slidera
        self.__slider = ctk.CTkSlider(self.__frame_left, from_= 50, to = 300, number_of_steps = 250)
        self.__slider.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "we")
        
        self.__slider.bind("<ButtonPress-1>", self.on_slider_hold)
        self.__slider.bind("<ButtonRelease-1>", self.on_slider_release)
        
        self.__canvas = ctk.CTkCanvas(self.__frame_left, width = 20, height = 20, highlightthickness = 0, bg = "gray17")
        self.__canvas.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "nw")
        
        self.dot = self.__canvas.create_oval(0, 0, 20, 20, fill='red')
        self.__canvas.itemconfig(self.dot, state='hidden')
        
        self.__label_val = ctk.CTkLabel(self.__frame_left, font=("Helvetica", 80))
        self.__label_val.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "nsew")
        
        # RIGHT FRAME
        
        self.__frame_right.grid_columnconfigure(0, weight= 1)
        self.__frame_right.grid_rowconfigure(0, weight=1)
        
        
        self.__button_start = ctk.CTkButton(self.__frame_right, text = "Start", command = self.start_metronome, font=("Helvetica", 50))
        self.__button_start.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "nsew", )
        
        # METRONOME
        
        self.__metronome = Metronome(bpm=120, beats_per_measure=4, sound_file="metronome.wav", command = self.blink)  # Example with 120 BPM and 4 beats per measure
        self.__is_running = False
        self.__was_running = False
            
        # WIN
        self.__win.protocol("WM_DELETE_WINDOW", self.on_closing)
               
        self.__win.bind("<space>", lambda event: self.start_metronome())
        self.__win.bind("<Right>", lambda event: self.increment_slider())
        self.__win.bind("<Left>", lambda event: self.decrement_slider())
        self.is_visible = True              
        self.__win.after(10, self.change_val)
        self.__win.mainloop()

    def on_slider_hold(self, event):
        if self.__is_running:
            self.__was_running = True
            self.stop_metronome()
        self.change_val()
        
    # TODO: Po pusteni slidera sa nespusti    
    def on_slider_release(self, event):
        if self.__was_running:
            self.start_metronome()
            self.__was_running = False
    
    def increment_slider(self):
        self.__slider.set(self.__slider.get() + 1)
        
    def decrement_slider(self): 
        self.__slider.set(self.__slider.get() - 1)

    def change_val(self):
        self.__label_val.configure(text=f"{int(self.__slider.get())}")
        self.__win.after(10, self.change_val)
            
    def start_metronome(self):
        self.__is_running = True
        self.__button_start.configure(text = "Stop", command = self.stop_metronome)
        self.__win.bind("<space>", lambda event: self.stop_metronome())
        self.__metronome.set_bpm(self.__slider.get())
        self.__metronome.start()
    
    def stop_metronome(self):
        self.__is_running = False
        self.__button_start.configure(text = "Start", command = self.start_metronome)
        self.__win.bind("<space>", lambda event: self.start_metronome())
        self.__canvas.itemconfig(self.dot, state='hidden')
        self.__metronome.stop()
        
    def blink(self):
        if self.is_visible:
            self.__canvas.itemconfig(self.dot, state='hidden')
        else:
            self.__canvas.itemconfig(self.dot, state='normal')
        self.is_visible = not self.is_visible
        
    def on_closing(self):
        self.__metronome.stop()
        self.__win.destroy()

MetronomeGUI()