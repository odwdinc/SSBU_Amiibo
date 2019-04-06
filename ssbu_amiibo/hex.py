#!/usr/bin/env python3
## Addapted form http://www.qtrac.eu/pyhexviewer.html
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import ttk

from tkinter import *
try:
	Spinbox = ttk.Spinbox
except AttributeError:
	Spinbox = tk.Spinbox
APPNAME = "Hex View"
BLOCK_WIDTH = 16
BLOCK_HEIGHT = 32
BLOCK_SIZE = BLOCK_WIDTH * BLOCK_HEIGHT
ENCODINGS = ("ASCII", "CP037", "CP850", "CP1140", "CP1252",
			 "Latin1", "ISO8859_15", "Mac_Roman", "UTF-8",
			 "UTF-8-sig", "UTF-16", "UTF-32")
class HexWindow:

	def __init__(self, parent, filename,exitFunc):
		self.exitFunc  = exitFunc
		self.parent = parent
		self.create_variables()
		self.create_widgets()
		self.create_layout()
		self.create_bindings()
		self.isFile = False
		self.filename = filename

		self.reset()


	def create_variables(self):
		self.filename = None
		self.encoding = tk.StringVar()
		self.encoding.set(ENCODINGS[0])

	def create_widgets(self):
		frame = self.frame = ttk.Frame(self.parent)
		self.encodingLabel = ttk.Label(frame, text="Encoding", underline=0)
		self.encodingCombobox = ttk.Combobox(
			frame, values=ENCODINGS, textvariable=self.encoding,
			state="readonly")
		self.saveButton = ttk.Button(frame, text="Save", underline=0,
									 command=self.save)
		self.resetButton = ttk.Button(frame, text="Reset", underline=0,
									 command=self.reset)
		self.quitButton = ttk.Button(frame, text="Quit", underline=0,
									 command=self.quit)
		self.create_view()

	def create_view(self):
		self.offsethorz = tk.Text(self.frame, height=BLOCK_HEIGHT,
								width=1)
		self.offsetvert = tk.Text(self.frame, height=1,
								width=BLOCK_WIDTH)

		self.viewText = tk.Text(self.frame, height=BLOCK_HEIGHT,
								width=2 + (BLOCK_WIDTH * 3))
		self.viewText.tag_configure("ascii", foreground="green")
		self.viewText.tag_configure("error", foreground="red")
		self.viewText.tag_configure("hexspace", foreground="navy")
		self.viewText.tag_configure("graybg", background="lightgray")
		self.viewText.bind('<Key>', self.viewTextCallback)

		self.viewText_enc = tk.Text(self.frame, height=BLOCK_HEIGHT,
								width=20)
		self.viewText_enc.tag_configure("ascii", foreground="green")
		self.viewText_enc.tag_configure("error", foreground="red")
		self.viewText_enc.tag_configure("hexspace", foreground="navy")
		self.viewText_enc.tag_configure("graybg", background="lightgray")

	def create_layout(self):
		for column, widget in enumerate((
				self.encodingLabel, self.encodingCombobox, self.saveButton,self.resetButton,
				self.quitButton)):
			widget.grid(row=0, column=column, sticky=tk.W)
		self.offsetvert.grid(row=1, column=1, columnspan=6, sticky=tk.NSEW)
		self.offsethorz.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW)
		self.viewText.grid(row=2, column=1, columnspan=6, sticky=tk.NSEW)
		self.viewText_enc.grid(row=2, column=7, columnspan=6, sticky=tk.NSEW)
		self.frame.grid(row=0, column=0, sticky=tk.NSEW)

		self.offsetvert.insert("end", "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F")
		for x in range(0,BLOCK_SIZE,16):
			x = "{0:0{1}x}".format(x,6)
			self.offsethorz.insert("end", ""+str(x)+"\n")#0010\n  0020\n0030\n0040\n0050\n0060\n0070\n0080\n0090\n00A0\n00B0\n00C0\n00D0\n00E0\n00F0\n")

	def create_bindings(self):
		self.offsethorz.bind("<MouseWheel>", self.scrolloed)
		self.viewText.bind("<MouseWheel>", self.scrolloed)
		self.viewText_enc.bind("<MouseWheel>", self.scrolloed)

		self.encodingCombobox.bind("<<ComboboxSelected>>", self.encodingChanged)

	def updateBlock(self):
		block = self.dataByts
		self.viewText.delete("1.0", "end")
		self.viewText_enc.delete("1.0", "end")
		rows = [block[i:i + BLOCK_WIDTH]
				for i in range(0, len(block), BLOCK_WIDTH)]
		for row in rows:
			self.show_bytes(row)
			self.show_line(row)
		self.viewText.insert("end", "\n")
		self.viewText_enc.insert("end", "\n")

	def open_block(self, *args):
		
		if not self.filename:
			return
		with open(self.filename, "rb") as file:
			try:
				file.seek(0, os.SEEK_SET)
				block = file.read(BLOCK_SIZE)
			except ValueError: # Empty offsetSpinbox
				return
			self.dataByts = block
			self.updateBlock()

	def viewTextCallback(self, event):
		CharList = ('1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F')
		pos =  self.viewText.index(tk.INSERT)
		x,y = pos.split('.',1)
		x =  int(x)
		y = int(y)

		if(event.keysym == 'Right'):
			y = y+(2-y%3)
			outstr =  "{}.{}".format(x,y).strip()
			self.viewText.mark_set("insert",outstr)
		elif(event.keysym == 'Left'):
			y = y-(y-1)%3
			outstr =  "{}.{}".format(x,y).strip()
			self.viewText.mark_set("insert",outstr)
		elif event.char in CharList:
			
			if self.viewText.get(pos) == ' ':
				pos =  "{}.{}".format(x,y+1).strip()
				endPos = "{}.{}".format(x,y+2).strip()
				self.viewText.mark_set("insert",pos)	
			else:
				endPos = "{}.{}".format(x,y+1).strip()

			self.viewText.delete(pos)
			self.viewText.insert(pos, event.char)
			self.viewText.mark_set("insert",endPos)
			self.resetLines()
			return "break"
		elif (event.keysym == 'Up') or (event.keysym == 'Down'):
			pass
		else:
			return "break"
	def reset(self):
		try:
			data = self.filename.decode()
			self.dataByts = self.filename
			self.updateBlock()
		except AttributeError:
			if self.filename and os.path.exists(self.filename):
				self.isFile = True
				self._open(self.filename)
		except UnicodeDecodeError:
			self.dataByts = self.filename
			self.updateBlock()
			

	def resetLines(self):
		pos =  self.viewText.index(tk.INSERT)
		HexText = self.viewText.get("1.0","end").replace('\n', '').replace(' ', '')
		self.dataByts = bytes.fromhex(HexText)
		self.updateBlock()
		self.viewText.mark_set("insert",pos)

	def show_bytes(self, row):
		for byte in row:
			tags = ()
			if byte in b"\t\n\r\v\f":
				tags = ("hexspace", "graybg")
			elif 0x20 < byte < 0x7F:
				tags = ("ascii",)
			self.viewText.insert("end", "{:02X} ".format(byte), tags)
		self.viewText.insert("end", "\n")

	def show_line(self, row):
		for char in row.decode(self.encoding.get(), errors="replace"):
			tags = ()
			if char in "\u2028\u2029\t\n\r\v\f\uFFFD":
				char = "."
				tags = ("graybg" if char == "\uFFFD" else "error",)
			elif 0x20 < ord(char) < 0x7F:
				tags = ("ascii",)
			elif not 0x20 <= ord(char) <= 0xFFFF: # Tcl/Tk limit
				char = "?"
				tags = ("error",)
			self.viewText_enc.insert("end", char, tags)
		self.viewText_enc.insert("end", "\n")

	def _open(self, filename):
		if filename and os.path.exists(filename):
			self.parent.title("{} — {}".format(filename, APPNAME))
			size = os.path.getsize(filename)
			size = (size - BLOCK_SIZE if size > BLOCK_SIZE else
					size - BLOCK_WIDTH)
			
			self.open_block()


	def scrolloed(self, event=None):
		pos = int(-1*(event.delta/120))
		#print(pos)
		self.offsethorz.yview_scroll(pos, "units")
		self.viewText.yview_scroll(pos, "units")
		self.viewText_enc.yview_scroll(pos, "units")

	def encodingChanged(self, event=None):

		self.resetLines()

	def save(self, event=None):
		HexText = self.viewText.get("1.0","end").replace('\n', '').replace(' ', '')
		if self.isFile:
			with open(self.filename, "wb") as file:
				file.write(bytes.fromhex(HexText))
		else:
			self.filename = bytes.fromhex(HexText)

	def quit(self, event=None):
		self.parent.destroy()
		
		self.exitFunc[1](self.filename,self.exitFunc[0])
		

def ExitHex(file,var):
	print(file,var)

def maine():
	app = tk.Tk()
	app.title(APPNAME)
	DBName = filedialog.askopenfilename(filetypes = (("All Files","*.*"),("","")))
	if DBName:
		HexWin = HexWindow(app,DBName,('test',ExitHex))
	app.protocol("WM_DELETE_WINDOW", app.quit)
	app.resizable(width=False, height=False)
	app.mainloop()

if __name__ == '__main__':
    maine()
