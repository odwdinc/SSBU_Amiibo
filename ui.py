#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Menu
from amiibo_class import ssbu
from subprocess import call
import subprocess
file = None
ssb = None
def OpenCmd():
	global file, new_item
	if(file):
		file.close()
	file = filedialog.askopenfile(mode='rb+', filetypes = (("Amiibo Decripted","*.bind"),("Amiibo Decripted","*.bind")))
	handaleFile()

def handaleFile():
	global ssb,menu
	if(file):
		new_item.entryconfig(1,state=NORMAL)
		new_item.entryconfig(3,state=NORMAL)
		menu.entryconfig("Data", state="normal")
		ssb = ssbu(file)
		handaleSSB()

def handaleSSB():

	#learn un0 move1 move2 move3 un1 xp un2 atc hp un3 gift
	if(ssb.ds1['learn'] == True):
		chk_state_learn.set(True)
	else:
		chk_state_learn.set(False)

	i = len(ssb.ds1['un0'])
	for i in range(0,i):
		tet_UM0[i].set(hex(ssb.ds1['un0'][i]))
		i =+1

	txt_Move_1.delete('0', 'end')
	txt_Move_2.delete('0', 'end')
	txt_Move_3.delete('0', 'end')

	txt_Move_1.insert('0',ssb.ds1['move1'])
	txt_Move_2.insert('0',ssb.ds1['move2'])
	txt_Move_3.insert('0',ssb.ds1['move3'])

	txt_XP.delete('0', 'end')
	txt_ATC.delete('0', 'end')
	txt_HP.delete('0', 'end')

	txt_XP.insert('0',ssb.ds1['xp'])
	txt_ATC.insert('0',ssb.ds1['atc'])
	txt_HP.insert('0',ssb.ds1['hp'])

	txt_Gift.delete('0', 'end')
	txt_Gift.insert('0',ssb.ds1['gift'])

def SaveCmd():
	global ssb
	ssb.setLearn(chk_state_learn.get())
	ssb.setMove1(int(txt_Move_1.get()))
	ssb.setMove2(int(txt_Move_2.get()))
	ssb.setMove3(int(txt_Move_3.get()))

	ssb.setLevel(int(txt_XP.get()))
	ssb.setAttack(int(txt_ATC.get()))
	ssb.setDefense(int(txt_HP.get()))

	ssb.setGift(int(txt_Gift.get()))

	ssb.sign()

def Encrypt():
	global file
	SaveCmd()
	curentfile = file.name
	file.close()
	fName = filedialog.asksaveasfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	print(call("./amiitool -e -k ./retail.bin -o "+fName +" -i "+curentfile,stderr=subprocess.STDOUT, shell=True))
	file = open(curentfile, "rb+")
	handaleFile()

def Decrypt():
	global file
	fName = filedialog.askopenfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	print(call("./amiitool -d -k ./retail.bin -i "+fName +" -o "+fName+"d",stderr=subprocess.STDOUT, shell=True))
	file = open(fName+"d", "rb+")
	handaleFile()

def QuitCmd():
	if(file):
		file.close()
	quit(0)


def ExportDB():
	DBName = filedialog.asksaveasfilename(filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	ssb.dataBlockToFile(DBName)


def InportDB():
	DBName = filedialog.askopenfilename(filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	ssb.dataBlockFromeFile(DBName)
	ssb.unpackData()
	handaleSSB()

window = Tk()

chk_state_learn = BooleanVar() 
chk_state_learn.set(False)
 
window.title("SSBU Amiibo editor")
window.geometry('840x480')

menu = Menu(window)
 
new_item = Menu(menu, tearoff=0)
 
new_item.add_command(label='Open',command=OpenCmd)
 
sv_cmd = new_item.add_command(label='Save',command=SaveCmd,state='disabled')

new_item.add_separator()

enc_cmd = new_item.add_command(label='Encrypt Amiibo',command=Encrypt,state='disabled')
drc_cmd =new_item.add_command(label='Decrypt amiibo',command=Decrypt)

new_item.add_separator()

new_item.add_command(label='Exit',command=QuitCmd)
 
menu.add_cascade(label='File', menu=new_item)

block_item = Menu(menu, tearoff=0)
block_item.add_command(label='Export DataBlock',command=ExportDB)
block_item.add_command(label='Import DataBlock',command=InportDB)
menu.add_cascade(label='Data', menu=block_item , state='disabled')

window.config(menu=menu)


chk_learn = Checkbutton(window, text='Learning On/Off', var=chk_state_learn)
chk_learn.grid(column=0, row=0)

lbl_Move_1 = Label(window, text="Move 1: ")
lbl_Move_1.grid(column=0, row=1)
txt_Move_1 = Entry(window,width=5)
txt_Move_1.grid(column=1, row=1)

lbl_Move_2 = Label(window, text="Move 2: ")
lbl_Move_2.grid(column=0, row=2)
txt_Move_2 = Entry(window,width=5)
txt_Move_2.grid(column=1, row=2)

lbl_Move_3 = Label(window, text="Move 3: ")
lbl_Move_3.grid(column=0, row=3)
txt_Move_3 = Entry(window,width=5)
txt_Move_3.grid(column=1, row=3)


lbl_XP = Label(window, text="XP: ")
lbl_XP.grid(column=0, row=4)
txt_XP = Entry(window,width=15)
txt_XP.grid(column=1, row=4)

lbl_ATC = Label(window, text="Attack: ")
lbl_ATC.grid(column=0, row=5)
txt_ATC = Entry(window,width=10)
txt_ATC.grid(column=1, row=5)


lbl_HP = Label(window, text="Defense: ")
lbl_HP.grid(column=0, row=6)
txt_HP = Entry(window,width=10)
txt_HP.grid(column=1, row=6)


lbl_Gift = Label(window, text="Gift: ")
lbl_Gift.grid(column=0, row=7)
txt_Gift = Entry(window,width=10)
txt_Gift.grid(column=1, row=7)

tet_UM0 = {}

for pos in range(0,9):
	tet_UM0[pos] = StringVar()
	Temp = Entry(window,width=6,textvariable = tet_UM0[pos])
	Temp.grid(column=3+pos, row=0)

#tet_UM1 = {}
#rowst = 3
#for posr in range(0,91):
#	for pos in range(0,16):
#		tet_UM1[pos] = StringVar()
#		Temp = Entry(window,width=4,textvariable = tet_UM1[pos])
#		Temp.grid(column=3+pos, row=rowst)
#	rowst +=1


 
window.mainloop()