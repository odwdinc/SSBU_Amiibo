#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import ttk

from amiibo_class import ssbu
from amiibo_class import MoveCodeList
from amiibo_class import Skill_Set

from subprocess import call
import subprocess
from pathlib import Path

file = None
ssb = None


MoveNames = list(MoveCodeList.keys())

MoveList =[k for k in MoveCodeList if not k.isdigit() and MoveCodeList[k] > 0]

Skills = {}
unknown_Skills = []

for s_type in Skill_Set:
	for s_name in Skill_Set[s_type]:
		if s_name in MoveList:
			Skill_Set[s_type][s_name].append(s_type)
			Skills[s_name] = Skill_Set[s_type][s_name]
		else:
			unknown_Skills.append('['+s_name+'] '+s_name)

No_Skills_dec = []

for k_name in MoveList:
	if not k_name in Skills:
		No_Skills_dec.append(k_name)


if(len(unknown_Skills)> 0):
	print("\n\nunknown_Skills",unknown_Skills)
	print("\n\n")

if(len(No_Skills_dec)>0):
	print("\n\nNo_Skills_dec",No_Skills_dec)
	print("\n\n")


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
		
		if(key_file):
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

	Moves['Move 1']['Entry'].set(ssb.ds1['move1'])
	Moves['Move 2']['Entry'].set(ssb.ds1['move2'])
	Moves['Move 3']['Entry'].set(ssb.ds1['move3'])

	Moves['Move 1']['Combobox'].set(MoveNames[int(ssb.ds1['move1'])])

	if MoveCodeList[MoveNames[int(ssb.ds1['move1'])]] == 2:
		Moves['Move 2']['Combobox'].set('')
		Moves['Move 3']['Combobox'].set(MoveNames[int(ssb.ds1['move3'])])

	elif MoveCodeList[MoveNames[int(ssb.ds1['move1'])]] == 3:
		Moves['Move 2']['Combobox'].set('')
		Moves['Move 3']['Combobox'].set('')
	else:
		Moves['Move 2']['Combobox'].set(MoveNames[int(ssb.ds1['move2'])])
		if MoveCodeList[MoveNames[int(ssb.ds1['move2'])]] == 2:
			Moves['Move 3']['Combobox'].set('')
		else:
			Moves['Move 3']['Combobox'].set(MoveNames[int(ssb.ds1['move3'])])

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

	ssb.setMove1(MoveNames.index(Moves['Move 1']['Combobox'].get()))
	if MoveCodeList[Moves['Move 1']['Combobox'].get()] == 2:
		ssb.setMove2(0)
		ssb.setMove3(MoveNames.index(Moves['Move 3']['Combobox'].get()))
	elif MoveCodeList[Moves['Move 1']['Combobox'].get()] == 3:
		ssb.setMove2(0)
		ssb.setMove3(0)
	else:
		ssb.setMove2(MoveNames.index(Moves['Move 2']['Combobox'].get()))
		if MoveCodeList[Moves['Move 1']['Combobox'].get()] == 2:
			ssb.setMove3(0)
		else:
			ssb.setMove3(MoveNames.index(Moves['Move 3']['Combobox'].get()))

	ssb.setLevel(int(txt_XP.get()))
	ssb.setAttack(int(txt_ATC.get()))
	ssb.setDefense(int(txt_HP.get()))

	ssb.setGift(int(txt_Gift.get()))

	ssb.sign()

def Encrypt():
	global file

	fName = filedialog.asksaveasfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	if fName :
		SaveCmd()
		curentfile = file.name
		file.close()
		print(call("amiitool -e -k ./retail.key -o "+fName +" -i "+curentfile,stderr=subprocess.STDOUT, shell=True))
		file = open(curentfile, "rb+")
		handaleFile()

def Decrypt():
	global file
	fName = filedialog.askopenfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	if fName:
		print(call("amiitool -d -k ./retail.key -i "+fName +" -o "+fName+"d",stderr=subprocess.STDOUT, shell=True))
		file = open(fName+"d", "rb+")
		handaleFile()

def QuitCmd():
	if(file):
		file.close()
	quit(0)


def ExportDB():
	DBName = filedialog.asksaveasfilename(filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	if DBName:
		ssb.dataBlockToFile(DBName)


def InportDB():
	DBName = filedialog.askopenfilename(filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	if DBName:
		ssb.dataBlockFromeFile(DBName)
		ssb.unpackData()
		handaleSSB()

def key(event):
	if(event.char):
		#print ("pressed", hex(ord(event.char)))
		if(file):
			if ord(event.char) == 0x05:
				print ("Encrypt")
				Encrypt()
			if ord(event.char) == 0x13:
				print ("Saved")
				SaveCmd()
		if ord(event.char) == 0xf:
			OpenCmd()


def Combobox_Change_1(event):
	this_move= Moves['Move 1']
	Combobox_Change(this_move)

def Combobox_Change_2(event):
	this_move= Moves['Move 2']
	Combobox_Change(this_move)

def Combobox_Change_3(event):
	this_move= Moves['Move 3']
	Combobox_Change(this_move)

def Combobox_Change(this_move):
	name = this_move['Combobox'].get()
	if name:
		this_move['Entry'].set(str(MoveNames.index(name)))

def Entry_Change_1():
	this_move= Moves['Move 1']
	Entry_Change(this_move)
	return True

def Entry_Change_2():
	this_move= Moves['Move 2']
	Entry_Change(this_move)
	return True

def Entry_Change_3():
	this_move= Moves['Move 3']
	Entry_Change(this_move)
	return True

def Entry_Change(this_move):
	if(this_move['Entry'].get()):
		e_move = this_move['Entry'].get()
		print("Entry ",e_move)
		name = MoveNames[int(e_move)]
		if name in Skills:
			this_move['Dec_Label'].set("[ "+Skills[name][3]+" Rank "+str(Skills[name][1])+" ] "+Skills[name][0])
		else:
			this_move['Dec_Label'].set('???')
		this_move['Combobox'].set(name)
	return True

window = Tk()
key_file = Path("./retail.key").is_file()
needed_tool = Path("/usr/local/bin/amiitool").is_file()
chk_state_learn = BooleanVar() 
chk_state_learn.set(False)
 
window.title("SSBU Amiibo editor")
window.geometry('1040x280')

menu = Menu(window)
 
new_item = Menu(menu, tearoff=0)
 
new_item.add_command(label='Open',command=OpenCmd)
 
sv_cmd = new_item.add_command(label='Save',command=SaveCmd,state='disabled')


if(key_file and needed_tool):

	new_item.add_separator()
	enc_cmd = new_item.add_command(label='Encrypt Amiibo',command=Encrypt,state='disabled')
	drc_cmd =new_item.add_command(label='Decrypt amiibo',command=Decrypt)
	block_item = Menu(menu, tearoff=0)
	block_item.add_command(label='Export DataBlock',command=ExportDB)
	block_item.add_command(label='Import DataBlock',command=InportDB)
	

new_item.add_separator()	
new_item.add_command(label='Exit',command=QuitCmd)


menu.add_cascade(label='File', menu=new_item)
if(key_file):
	menu.add_cascade(label='Data', menu=block_item , state='disabled')
window.config(menu=menu)
window.bind("<Key>", key)

chk_learn = Checkbutton(window, text='Learning On/Off', var=chk_state_learn)
chk_learn.grid(column=0, row=0)

Moves={'Move 1':{'Combobox':StringVar(menu),
				'Entry':StringVar(menu),
				'Dec_Label':StringVar(menu),
				'Combobox_Change': Combobox_Change_1,
				'Entry_Change': Entry_Change_1
				},
		'Move 2':{'Combobox':StringVar(menu),
				'Entry':StringVar(menu),
				'Dec_Label':StringVar(menu),
				'Combobox_Change': Combobox_Change_2,
				'Entry_Change': Entry_Change_2
				},
		'Move 3':{'Combobox':StringVar(menu),
				'Entry':StringVar(menu),
				'Dec_Label':StringVar(menu),
				'Combobox_Change': Combobox_Change_3,
				'Entry_Change': Entry_Change_3
				},
}
move_row = 1
for move in Moves:
	lbl = Label(window, text=move+": ")
	lbl.grid(row=move_row, column=0)

	popup = ttk.Combobox(window, textvariable=Moves[move]['Combobox'], values=MoveList)
	popup.grid(row = move_row, column =1)
	popup.bind("<<ComboboxSelected>>", Moves[move]['Combobox_Change'])

	ent = Entry(window,width=10, textvariable=Moves[move]['Entry'], validate="focusout", validatecommand=Moves[move]['Entry_Change'])
	ent.grid(row=move_row,column=2)
	
	lbl_dec = Label(window,  textvariable=Moves[move]['Dec_Label'])
	lbl_dec.grid(row=move_row,column=3)
	move_row +=1

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
 
window.mainloop()