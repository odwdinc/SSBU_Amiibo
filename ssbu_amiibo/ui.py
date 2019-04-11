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

from tkinter import messagebox

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

class MoveData:
	def __init__(self):
		self.MoveNames = list(MoveCodeList.keys())
		self.MoveList =[k for k in MoveCodeList if not k.isdigit() and MoveCodeList[k] > 0]

	def itemClicked(self, event, _tree):
		ID = self.TreeList[_tree]['Treeview'].focus()
		if  "I" not in ID:
			parent_iid = self.TreeList[_tree]['Treeview'].parent(ID)
			ParentName = self.TreeList[_tree]['Treeview'].item(parent_iid)['text']
			Name =  self.TreeList[_tree]['Treeview'].item(ID)['text']
			Values = self.TreeList[_tree]['Treeview'].item(ID)['values']
			self.TreeList[_tree]['EntryText'].set(ID)

			print (ID,ParentName ,Name ,Values)

	def itemChange(self, _tree):
		testText = self.TreeList[_tree]['EntryText'].get()
		if(testText and testText.isdigit()):
			if len(self.MoveNames) < int(testText):
				name = self.MoveNames[int(testText)]
				if not name.isdigit():
					self.setItem(_tree, int(testText))
		return True
		
	def buildTrees(self, window, Height = 4):
		self.TreeList = {'tree':{'Treeview':None,'EntryText':StringVar(window),'idlist':[]},\
						'tree2':{'Treeview':None,'EntryText':StringVar(window),'idlist':[]},\
						'tree3':{'Treeview':None,'EntryText':StringVar(window),'idlist':[]}}

		sf = Frame(window)
		cpol = [200,40,450]
		cpoT = ["Skill List","Slots","Decription"]
		pos  = 0
		

		for tree in self.TreeList:
			self.TreeList[tree]['Treeview'] = ttk.Treeview(sf, columns=('slotCt','dec',),height=Height) 
	
			self.TreeList[tree]['Treeview'].column("#0", width=cpol[0])
			self.TreeList[tree]['Treeview'].heading('#0', text=cpoT[0])
			self.TreeList[tree]['Treeview'].column("#1", width=cpol[1])
			self.TreeList[tree]['Treeview'].heading('#1', text=cpoT[1])
			self.TreeList[tree]['Treeview'].column("#2",width=cpol[2])
			self.TreeList[tree]['Treeview'].heading('#2', text=cpoT[2])
			self.TreeList[tree]['Treeview'].grid( row=pos, column=1, sticky=(W, W, E, S))

			ysb = ttk.Scrollbar(sf, orient='vertical', command=self.TreeList[tree]['Treeview'].yview)
			ysb.grid(row=pos, column=0, sticky='ns')
			pos+=1

		return sf

	def addSkilsToTree(self, tree, maxslot = 3):
		SkillList = []
		for s_type in Skill_Set:
			id = self.TreeList[tree]['Treeview'].insert('', 'end', text=s_type,open=False)
			self.TreeList[tree]['idlist'].append(id)
			temp  = list(Skill_Set[s_type].keys())
			for s_name in sorted(temp):
				if s_name in self.MoveList and MoveCodeList[s_name] <= maxslot:	
					ids = self.TreeList[tree]['Treeview'].insert(id, 'end',  self.MoveNames.index(s_name), text=s_name, values=(MoveCodeList[s_name], Skill_Set[s_type][s_name][0]))
					SkillList.append(s_name)

		id = self.TreeList[tree]['Treeview'].insert('', 'end', text="Unknown Skills",open=False)
		for move in self.MoveList:
			if move not in SkillList and MoveCodeList[move] <= maxslot:
				self.TreeList[tree]['Treeview'].insert(id, 'end', self.MoveNames.index(move), text=move,  values=(MoveCodeList[move], ""))

		self.TreeList[tree]['Treeview'].bind('<<TreeviewSelect>>', lambda e: self.itemClicked(e,tree))


	def setItem(self, _tree, id):
		if(id > 0):
			parent_iid = self.TreeList[_tree]['Treeview'].parent(id)
			self.TreeList[_tree]['Treeview'].item(parent_iid, open=True)
			self.TreeList[_tree]['Treeview'].focus(id)
			self.TreeList[_tree]['Treeview'].selection_set(id)
			self.TreeList[_tree]['Treeview'].see(id)
		else:
			for node in self.TreeList[_tree]['idlist']:
				self.TreeList[_tree]['Treeview'].item(node, open = False)


	def getID(self,_tree):
		if  "I" not in self.TreeList[_tree]['Treeview'].focus():
			return self.TreeList[_tree]['Treeview'].focus()
		else:
			return 0

	def canUse(self, moveindex, creddits):
		if moveindex is '':
			return (0, creddits)
		caust = MoveCodeList[self.MoveNames[int(moveindex)]]
		if creddits >= caust:
			return (int(moveindex), creddits-caust)
		return(0,creddits)
mv = MoveData()
#mv.setItem(mv.TreeList['tree'],102)



def OpenCmd():
	global file, new_item
	if(file):
		file.close()
	file = filedialog.askopenfile(mode='rb+', filetypes = (("Amiibo Decripted","*.bind"),("Amiibo Decripted","*.bind")))
	handaleFile()

def handaleFile():
	global ssb, menu, background_label, trainData , window ,traningMenu
	if(file):
		new_item.entryconfig(1,state=NORMAL)
		new_item.entryconfig(2,state=NORMAL)
		new_item.entryconfig(4,state=NORMAL)
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
	if(ssb.ds1['learn'] == True):
		chk_state_learn.set(True)
	else:
		chk_state_learn.set(False)

	txt_XP.delete('0', 'end')
	txt_ATC.delete('0', 'end')
	txt_HP.delete('0', 'end')

	txt_XP.insert('0',ssb.ds1['xp'])
	txt_ATC.insert('0',ssb.ds1['atc'])
	txt_HP.insert('0',ssb.ds1['hp'])

	txt_Gift.delete('0', 'end')
	txt_Gift.insert('0',ssb.ds1['gift'])

	txt_CL.delete('0', 'end')
	txt_CL.insert('0',ssb.ds1['color'])

	mv.setItem('tree',ssb.ds1['move1'])
	mv.setItem('tree2',ssb.ds1['move2'])
	mv.setItem('tree3',ssb.ds1['move3'])



def SaveCmd():
	global ssb
	ssb.setLearn(chk_state_learn.get())
	slot = 3
	move1 , slot =  mv.canUse(mv.getID('tree'),slot)
	move2 , slot =  mv.canUse(mv.getID('tree2'),slot)
	move3 , slot =  mv.canUse(mv.getID('tree3'),slot)

	ssb.setMove1(move1)
	ssb.setMove2(move2)
	ssb.setMove3(move3)

	ssb.setLevel(int(txt_XP.get()))
	ssb.setAttack(int(txt_ATC.get()))
	ssb.setDefense(int(txt_HP.get()))

	ssb.setGift(int(txt_Gift.get()))

	ssb.setColor(int(txt_CL.get()))

	ssb.sign()
	handaleFile()

def SaveASCmd():
	global file,ssb
	fName = filedialog.asksaveasfilename(defaultextension=".bind", filetypes = (("Amiibo Decripted","*.bind"),("Amiibo Decripted","*.bind")))
	if fName :
		curentfile = file.name
		file.close()
		with open(curentfile, 'rb') as fp:
			data = fp.read()

			with open(fName, 'wb') as fp:
				fp.write(data)
		file = open(fName, "rb+")
		ssb = ssbu(file)
		SaveCmd()
		handaleFile()

def Encrypt():
	global file

	fName = filedialog.asksaveasfilename(defaultextension=".bin",filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
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


def maine():
	global master_keys, window,txt_CL, new_item, sv_cmd,sva_cmd, menu, chk_state_learn, chk_learn, Moves, txt_XP, txt_ATC, txt_HP, txt_Gift, key_file, background_label, menu
	window = Tk()

	key_file = Path("./key_retail.bin").is_file()



	chk_state_learn = BooleanVar() 
	chk_state_learn.set(False)
	 
	window.title("SSBU Amiibo editor")
	window.geometry('1080x400')

	menu = Menu(window)
	 
	new_item = Menu(menu, tearoff=0)
	 
	new_item.add_command(label='Open',command=OpenCmd)
	 
	sv_cmd = new_item.add_command(label='Save',command=SaveCmd,state='disabled')
	sva_cmd = new_item.add_command(label='Save As...',command=SaveASCmd,state='disabled')
	

	if (key_file):
		with open('./key_retail.bin', 'rb') as fp_d:
			master_keys = AmiiboMasterKey.from_combined_bin(fp_d.read())

	if(key_file):
		new_item.add_separator()
		enc_cmd = new_item.add_command(label='Encrypt Amiibo',command=Encrypt,state='disabled')
		drc_cmd =new_item.add_command(label='Decrypt amiibo',command=Decrypt)
	
	new_item.add_separator()	
	new_item.add_command(label='Exit',command=QuitCmd)
	menu.add_cascade(label='File', menu=new_item)

	unMenuCount = 6
	block_item = Menu(menu, tearoff=0)
	sub_item = Menu(block_item, tearoff=0)

	sub_item.add_command(label='Export Full DataBlock',command=ExportDB)
	sub_item.add_command(label='Export Traning DataBlock',command=lambda: Export('train'))
	sub_item.add_command(label='Export Color DataBlock',command=lambda: Export('color'))

	
	for un in range(0,unMenuCount):
		sub_item.add_command(label='Export Un'+str(un)+'_Block',command=(lambda un: lambda: Export('un'+un))(str(un)))
	block_item.add_cascade(label='Export', menu=sub_item)

	sub_item = Menu(block_item, tearoff=0)
	sub_item.add_command(label='Import Full DataBlock',command=InportDB)
	sub_item.add_command(label='Import Traning DataBlock',command=lambda: Inport('train'))
	sub_item.add_command(label='Import Color DataBlock',command=lambda: Inport('color'))

	for un in range(0,unMenuCount):
		sub_item.add_command(label='Import Un'+str(un)+'_Block',command=(lambda un: lambda: Inport('un'+un))(str(un)))
	block_item.add_cascade(label='Import', menu=sub_item)

	sub_item = Menu(block_item, tearoff=0)
	sub_item.add_command(label='Edit Full DataBlock',command=(lambda: Edit('train')))
	sub_item.add_command(label='Edit Traning DataBlock',command=lambda: Edit('train'))
	sub_item.add_command(label='Edit Color DataBlock',command=lambda: Edit('color'))

	for un in range(0,unMenuCount):
		sub_item.add_command(label='Edit Un'+str(un)+'_Block',command=(lambda un: lambda: Edit('un'+un))(str(un)))
	block_item.add_cascade(label='Edit', menu=sub_item)
		
	menu.add_cascade(label='Data', menu=block_item , state='disabled')

	window.config(menu=menu)
	window.bind("<Key>", key)

	background_label = Label(window)
	background_label.grid(column=0, row=5,columnspan = 4)

	chk_learn = Checkbutton(window, text='Learning On/Off', var=chk_state_learn)
	chk_learn.grid(column=0, row=0)


	moveFrame = mv.buildTrees(window)
	moveFrame.grid(column=4, row=1, rowspan = 5)

	for tree in mv.TreeList:
		mv.addSkilsToTree(tree)

	lbl_XP = Label(window, text="XP: ")
	lbl_XP.grid(column=0, row=1)
	txt_XP = Entry(window)
	txt_XP.grid(column=1, row=1)

	lbl_ATC = Label(window, text="Attack: ")
	lbl_ATC.grid(column=2, row=1)
	txt_ATC = Entry(window)
	txt_ATC.grid(column=3, row=1)

	lbl_HP = Label(window, text="Defense: ")
	lbl_HP.grid(column=0, row=2)
	txt_HP = Entry(window)
	txt_HP.grid(column=1, row=2)

	lbl_Gift = Label(window, text="Gift: ")
	lbl_Gift.grid(column=2, row=2)
	txt_Gift = Entry(window)
	txt_Gift.grid(column=3, row=2)

	lbl_CL = Label(window, text="Color: ")
	lbl_CL.grid(column=0, row=3)
	txt_CL = Entry(window)
	txt_CL.grid(column=1, row=3)

	window.mainloop()
	
if __name__ == '__main__':
    maine()
