#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import ttk

from ssbu_amiibo.amiibo_class import ssbu
from ssbu_amiibo.amiibo_class import MoveCodeList
from ssbu_amiibo.amiibo_class import Skill_Set


from amiibo import AmiiboDump, AmiiboMasterKey
from pathlib import Path

from ssbu_amiibo.hex import HexWindow
from ssbu_amiibo.trainingData import training, knowLocations
from PIL import ImageTk


file = None
ssb = None
traningMenu=None

def amiitools_to_dump(internal):
    """Convert a 3DS/amiitools internal dump to the standard Amiibo/NTAG215
    dump format."""
    dump = bytearray(internal)
    dump[0x008:0x010] = internal[0x000:0x008]
    dump[0x080:0x0A0] = internal[0x008:0x028]
    dump[0x010:0x034] = internal[0x028:0x04C]
    dump[0x0A0:0x208] = internal[0x04C:0x1B4]
    dump[0x034:0x054] = internal[0x1B4:0x1D4]
    dump[0x000:0x008] = internal[0x1D4:0x1DC]
    dump[0x054:0x080] = internal[0x1DC:0x208]
    return dump

def dump_to_amiitools(dump):
    """Convert a standard Amiibo/NTAG215 dump to the 3DS/amiitools internal
    format.
    """
    internal = bytearray(dump)
    internal[0x000:0x008] = dump[0x008:0x010]
    internal[0x008:0x028] = dump[0x080:0x0A0]
    internal[0x028:0x04C] = dump[0x010:0x034]
    internal[0x04C:0x1B4] = dump[0x0A0:0x208]
    internal[0x1B4:0x1D4] = dump[0x034:0x054]
    internal[0x1D4:0x1DC] = dump[0x000:0x008]
    internal[0x1DC:0x208] = dump[0x054:0x080]
    return internal

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


#if(len(unknown_Skills)> 0):
#	print("\n\nunknown_Skills",unknown_Skills)
#	print("\n\n")

#if(len(No_Skills_dec)>0):
#	print("\n\nNo_Skills_dec",No_Skills_dec)
#	print("\n\n")

def OpenCmd():
	global file, new_item
	if(file):
		file.close()
	file = filedialog.askopenfile(mode='rb+', filetypes = (("Amiibo Decripted","*.bind"),("Amiibo Decripted","*.bind")))
	handaleFile()
from tkinter import messagebox
def handaleFile():
	global ssb, menu, background_label, trainData , window ,traningMenu
	if(file):
		new_item.entryconfig(1,state=NORMAL)
		
		if(key_file):
			new_item.entryconfig(3,state=NORMAL)
			menu.entryconfig("Data", state="normal")
		ssb = ssbu(file)

		img2 = ImageTk.PhotoImage(ssb.img)
		background_label.configure(image=img2)
		background_label.image = img2
		window.title("SSBU Amiibo editor " + ssb.webdata['amiibo']['name'])
		menu.delete(3)
		for train in training:
			if training[train]['head'] == ssb.webdata['amiibo']['head']:
				print(train)
				trainData = training[train]
				items = Menu(menu, tearoff=0)
				for move in trainData['data']:
					print("	"+move[0])
					items.add_command(label=move[0], command=(lambda move: lambda: traningFunc(move))(move))
				menu.add_cascade(label='Traning', menu= items)
		handaleSSB()

def traningFunc(var):
	 messagebox.showinfo(var[0],var[1])

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
	move1 = Moves['Move 1']['Combobox'].get()
	if move1 is '':
		move1 = 'No_Move'
	ssb.setMove1(MoveNames.index(move1))
	if MoveCodeList[Moves['Move 1']['Combobox'].get()] == 2:
		ssb.setMove2(0)
		move3 = Moves['Move 3']['Combobox'].get()
		if move3 is '':
			move3 = 'No_Move'
		ssb.setMove3(MoveNames.index(move3))
	elif MoveCodeList[Moves['Move 1']['Combobox'].get()] == 3:
		ssb.setMove2(0)
		ssb.setMove3(0)
	else:
		move2 = Moves['Move 2']['Combobox'].get()
		if move2 is '':
			move2 = 'No_Move'
		ssb.setMove2(MoveNames.index(move2))
		if MoveCodeList[Moves['Move 1']['Combobox'].get()] == 2:
			ssb.setMove3(0)
		else:
			move3 = Moves['Move 3']['Combobox'].get()
			if move3 is '':
				move3 = 'No_Move' 
			ssb.setMove3(MoveNames.index(move3))

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

		with open(curentfile, 'rb') as fp:
			data = fp.read()
		data = amiitools_to_dump(data)
		dump = AmiiboDump(master_keys, data, is_locked=False)
		dump.lock()
		dump.unset_lock_bytes()
		with open(fName, 'wb') as fp:
			fp.write(dump.data)

		file = open(curentfile, "rb+")
		handaleFile()

def Decrypt():
	global file
	fName = filedialog.askopenfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	if fName:
		with open(fName, 'rb') as fp:
			dump = AmiiboDump(master_keys, fp.read(), is_locked=True)
		dump.unlock()
		data = dump.data
		data = dump_to_amiitools(data)
		with open(fName+"d", 'wb') as fp:
			fp.write(data)
		file = open(fName+"d", "rb+")
		handaleFile()

def QuitCmd():
	if(file):
		file.close()
	quit(0)



def Edit(var):
	top = Toplevel(window)
	top.title("Hex View")

	if var == 'DB':
		HexWin = HexWindow(top,ssb.data,(None,ExitHex))
	else:
		HexWin = HexWindow(top,ssb.ds1[var],(var,ExitHex))

	

def Export(var):
	DBName = filedialog.asksaveasfilename(defaultextension="."+var+"_db",filetypes = (("Smash "+var+"_Block","*."+var+"_db"),("Smash "+var+"_Block","*."+var+"_db")))
	if DBName:
		with open(DBName, "wb") as fdb:
			print(len(ssb.ds1[var]))
			fdb.write(ssb.ds1[var])

def Inport(var):
	DBName = filedialog.askopenfilename(filetypes = (("Smash "+var+"_Block","*."+var+"_db"),("Smash "+var+"_Block","*."+var+"_db")))
	if DBName:
		with open(DBName, "rb") as fdb:
			ssb.ds1[var] = bytearray(fdb.read())

def ExportDB():
	DBName = filedialog.asksaveasfilename(defaultextension=".bind_db",filetypes = (("Smash DataBlock","*.bind_db"),("Smash DataBlock","*.bind_db")))
	if DBName:
		ssb.dataBlockToFile(DBName)

def ExitHex(DBName,VarName):
	if VarName is None:
		ssb.data = DBName
		ssb.unpackData()
		handaleSSB()
	else:
		ssb.ds1[VarName] = DBName


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
def maine():
	global master_keys, window, new_item, sv_cmd, menu, chk_state_learn, chk_learn, Moves, txt_XP, txt_ATC, txt_HP, txt_Gift, key_file, background_label, menu
	window = Tk()

	key_file = Path("./key_retail.bin").is_file()



	chk_state_learn = BooleanVar() 
	chk_state_learn.set(False)
	 
	window.title("SSBU Amiibo editor")
	window.geometry('1040x400')

	menu = Menu(window)
	 
	new_item = Menu(menu, tearoff=0)
	 
	new_item.add_command(label='Open',command=OpenCmd)
	 
	sv_cmd = new_item.add_command(label='Save',command=SaveCmd,state='disabled')

	if (key_file):
		with open('./key_retail.bin', 'rb') as fp_d:
			master_keys = AmiiboMasterKey.from_combined_bin(fp_d.read())

	if(key_file):
		new_item.add_separator()
		enc_cmd = new_item.add_command(label='Encrypt Amiibo',command=Encrypt,state='disabled')
		drc_cmd =new_item.add_command(label='Decrypt amiibo',command=Decrypt)
		block_item = Menu(menu, tearoff=0)
		block_item.add_command(label='Export Full DataBlock',command=ExportDB)
		for un in range(0,5):
			block_item.add_command(label='Export Un'+str(un)+'_Block',command=(lambda un: lambda: Export('un'+un))(str(un)))
		block_item.add_separator()
		block_item.add_command(label='Import Full DataBlock',command=InportDB)
		for un in range(0,5):
			block_item.add_command(label='Import Un'+str(un)+'_Block',command=(lambda un: lambda: Inport('un'+un))(str(un)))
		block_item.add_separator()
		
		block_item.add_command(label='Edit Full DataBlock',command=(lambda: Edit('DB')))
		for un in range(0,5):
			block_item.add_command(label='Edit Un'+str(un)+'_Block',command=(lambda un: lambda: Edit('un'+un))(str(un)))
		

	new_item.add_separator()	
	new_item.add_command(label='Exit',command=QuitCmd)


	menu.add_cascade(label='File', menu=new_item)
	if(key_file):
		menu.add_cascade(label='Data', menu=block_item , state='disabled')
	window.config(menu=menu)
	window.bind("<Key>", key)

	background_label = Label(window)
	background_label.place(x=0, y=0, relwidth=1, relheight=1)


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
	
if __name__ == '__main__':
    maine()
