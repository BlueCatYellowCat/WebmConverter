import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.input_b = tk.Button(self)
		self.input_b["text"] = "Input file..."
		self.input_b["command"] = self.openfile
		self.input_b.grid(row=0, column = 0, padx=5, pady=2)
		self.input_t = tk.Entry(self, width = 80)
		self.input_t.grid(row=0, column = 1, columnspan=4, sticky=W)
		self.output_l = tk.Label(self, text="Output file:")
		self.output_l.grid(row=1, column = 0, sticky=W, padx=5)
		self.output_t = tk.Entry(self, width = 80)
		self.output_t.grid(row=1, column = 1, columnspan=4, sticky=W)
		self.padlowright = tk.Label(self, text=" ", width = 1)
		self.padlowright.grid(row=4, column = 5)
		self.convert = tk.Button(self, width = 10, height = 2)
		self.convert["text"] = "Convert file"
		self.convert["command"] = self.convertfile
		self.convert.grid(row=4, column = 4, columnspan=2, sticky=E, padx=5, pady=5)
		self.au = IntVar()
		self.au_c = Checkbutton(self, text="Audio", variable=self.au)
		self.au_c.grid(row=2, column = 1, sticky=W, pady=2)
		self.vp = IntVar()
		self.vp_c = Checkbutton(self, text="VP9   ", variable=self.vp)
		self.vp_c.grid(row=2, column = 2, sticky=W, pady=2)
		self.start_l = tk.Label(self, text="Start from:")
		self.start_l.grid(row=3, column = 0, sticky=E, padx=5)
		self.start_t = tk.Entry(self, width = 10)
		self.start_t.grid(row=3, column = 1, sticky=W)
		self.duration_l = tk.Label(self, text="  Duration: ")
		self.duration_l.grid(row=3, column = 1, sticky=E)
		self.duration_t = tk.Entry(self, width = 10)
		self.duration_t.grid(row=3, column = 2, sticky=W)
		self.bitrate_l = tk.Label(self, text="  Bitrate: (MB/s) ")
		self.bitrate_l.grid(row=3, column = 2, sticky=E)
		self.bitrate_t = tk.Entry(self, width = 4)
		self.bitrate_t.grid(row=3, column = 3, sticky=W)
		self.bitrate_t.insert(0, "1")
		self.scale_l = tk.Label(self, text="Scale: (enter width) ")
		self.scale_l.grid(row=3, column = 3, sticky=E)
		self.scale_t = tk.Entry(self, width = 5)
		self.scale_t.grid(row=3, column = 4, sticky=W)


	def openfile(self):
		filename = filedialog.askopenfilename()
		self.input_t.delete(0, len(self.input_t.get()))
		self.input_t.insert(0, filename)
		self.output_t.delete(0, len(self.output_t.get()))
		if ".webm" == os.path.splitext(filename)[1]:
			self.output_t.insert(0, os.path.splitext(filename)[0]+"1.webm")
		else:
			self.output_t.insert(0, os.path.splitext(filename)[0]+".webm")


	def convertfile(self):
		time_option = ""
		if self.start_t.get() != "":
			time_option = " -ss "+self.start_t.get()
		if self.duration_t.get() != "":
			time_option = time_option +" -t "+self.duration_t.get()
		audio_option = ""
		if self.au.get() == 0:
			audio_option = "-an" 
		vp_option = ""
		if self.vp.get() == 1:
			vp_option = "-vp9"
		scale_option = ""
		if self.scale_t.get() != "":
			scale_option = " -vf scale="+self.scale_t.get()+":-2" 
		infile = self.input_t.get().replace('\\','/')
		outfile = self.output_t.get().replace('\\','/')
		os.system('ffmpeg -i "'+infile+'" -c:v libvpx'+vp_option+' -b:v '+self.bitrate_t.get()+'M -c:a libvorbis '+audio_option+time_option+scale_option+' "'+outfile+'"')
		
root = tk.Tk()
root.wm_title("Webm Converter")
app = Application(master=root)
app.mainloop()