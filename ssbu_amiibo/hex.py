#!/usr/bin/env python3
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

		self.top = Toplevel(parent)
		self.top.title(APPNAME)
		self.parent = self.top
		self.create_variables()
		self.create_widgets()
		self.create_layout()
		self.create_bindings()
		print(filename)
		self._open(filename)

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
		self.quitButton = ttk.Button(frame, text="Quit", underline=0,
									 command=self.quit)
		self.create_view()

	def create_view(self):
		self.viewText = tk.Text(self.frame, height=BLOCK_HEIGHT,
								width=2 + (BLOCK_WIDTH * 3))
		self.viewText.tag_configure("ascii", foreground="green")
		self.viewText.tag_configure("error", foreground="red")
		self.viewText.tag_configure("hexspace", foreground="navy")
		self.viewText.tag_configure("graybg", background="lightgray")
		self.viewText.bind('<Key>', self.viewTextCallback)

		self.viewText_enc = tk.Text(self.frame, height=BLOCK_HEIGHT,
								width=2 + (BLOCK_WIDTH * 4))
		self.viewText_enc.tag_configure("ascii", foreground="green")
		self.viewText_enc.tag_configure("error", foreground="red")
		self.viewText_enc.tag_configure("hexspace", foreground="navy")
		self.viewText_enc.tag_configure("graybg", background="lightgray")

	def create_layout(self):
		for column, widget in enumerate((
				self.encodingLabel, self.encodingCombobox,
				self.quitButton)):
			widget.grid(row=0, column=column, sticky=tk.W)
		self.viewText.grid(row=1, column=0, columnspan=6, sticky=tk.NSEW)
		self.viewText_enc.grid(row=1, column=7, columnspan=6, sticky=tk.NSEW)
		self.frame.grid(row=0, column=0, sticky=tk.NSEW)

	def create_bindings(self):
		for keypress in ("<Control-q>", "<Alt-q>", "<Escape>"):
			self.parent.bind(keypress, self.quit)

	def updateBlock(self, block):
		self.viewText.delete("1.0", "end")
		self.viewText_enc.delete("1.0", "end")
		rows = [block[i:i + BLOCK_WIDTH]
				for i in range(0, len(block), BLOCK_WIDTH)]
		for row in rows:
			self.show_bytes(row)
			self.show_line(row)
		self.viewText.insert("end", "\n")
		self.viewText_enc.insert("end", "\n")

	def show_block(self, *args):
		
		if not self.filename:
			return
		with open(self.filename, "rb") as file:
			try:
				file.seek(0, os.SEEK_SET)
				block = file.read(BLOCK_SIZE)
			except ValueError: # Empty offsetSpinbox
				return
			self.updateBlock(block)

	def viewTextCallback(self, event):
		CharList = ('1','2','3','4','5','6','7','8','9','0','A','B','C','D','E','F')
		pos =  self.viewText.index(tk.INSERT)
		x,y = pos.split('.',1)
		x =  int(x)
		y = int(y)

		if(event.keysym == 'Right'):
			y = y+(2-y%3)
			outstr =  "{}.{}".format(x,y).strip()
			#print(pos,outstr)
			self.viewText.mark_set("insert",outstr)
		elif(event.keysym == 'Left'):
			y = y-(y-1)%3
			outstr =  "{}.{}".format(x,y).strip()
			#print(pos,outstr)
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
			#print(pos,event.char)
			self.resetLines()
			self.viewText.mark_set("insert",endPos)
			return "break"
		elif (event.keysym == 'Up') or (event.keysym == 'Down'):
			pass
		else:
			print(event)
			#outstr =  "{}.{}".format(x,y+1).strip()
			#self.viewText.delete(outstr)
			return "break"
		

	def resetLines(self):
		HexText = self.viewText.get("1.0","end").replace('\n', '').replace(' ', '')
		self.updateBlock(bytes.fromhex(HexText))


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
			self.filename = filename
			self.show_block()

	def quit(self, event=None):
		HexText = self.viewText.get("1.0","end").replace('\n', '').replace(' ', '')

		with open(self.filename, "wb") as file:
			file.write(bytes.fromhex(HexText))

		self.parent.destroy()
		self.exitFunc(self.filename)
		

def ExitHex(file):
	print(file)

def maine():
	app = tk.Tk()
	app.title(APPNAME)
	DBName = filedialog.askopenfilename(filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	if DBName:
		HexWin = HexWindow(app,DBName,ExitHex)
	app.protocol("WM_DELETE_WINDOW", app.quit)
	app.resizable(width=False, height=False)
	app.mainloop()

if __name__ == '__main__':
    maine()
