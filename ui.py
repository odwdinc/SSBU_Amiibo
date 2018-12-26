#!/usr/bin/env python3

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Menu
from amiibo_class import ssbu
from subprocess import call
import subprocess
from pathlib import Path

file = None
ssb = None
MoveCodeList = {
'No_Move':0,
'Move Speed ↑':1,
'Hyper Smash Attacks':1,
'3':1,
'Jump ↑':1,
'Additional Midair Jump':2,
'Lifesteal':2,
'Defense ↑':1,
'Easier Dodging':1,
'Easier Perfect Shield	':1,
'Super Armor':3,
#10
'Slow Super Armor':2,
'Trade-Off Attacks ↑':1,
'Trade-Off Defense ↑':1,
'Trade-Off Speed ↑':1,
'Trade-Off Ability ↑':1,
'Critical-Health Attack ↑':1,
'Critical-Health Defense ↑':1,
'Critical-Health Stats ↑':1,
'Critical Immunity':2,
'Autoheal':2,
#20
'Poison Immunity':2,
'Poison Damage Reduced':1,
'Poison Heals':3,
'Lava-Floor Immunity':2,
'Sticky-Floor Immunity':2,
'Beam Sword Equipped':1,
'Lip\'s Stick Equipped':1,
'Star Rod Equipped':1,
'Ore Club Equipped':3,
'Home-Run Bat Equipped':1,
#30
'Ray Gun Equipped':2,
'Super Scope Equipped':2,
'Gust Bellows Equipped':1,
'Drill Equipped':1,
'Green Shell Equipped':1,
'Poke Ball Equipped':1,
'37':1,
'Black Shell Equipped':1,
'Bunny Hood Equipped':1,
'Made of Metal':1,
#40
'Mouthful of Curry':2,
'Franklin Badge Equipped':2,
'Hammer Equipped':3,
'Fairy Bottle Equipped':1,
'Fire Flower Equipped':1,
'Freezie Equipped':1,
'Ramblin\' Evil Mushroom Equipped':1,
'Killing Edge Equipped':1,
'49':1,
'Physical Attack ↑':1,
#50
'Weapon Attack ↑':1,
'Fist Attack ↑':1,
'Foot Attack ↑':1,
'Aura Attack ↑':1,
'Magic Attack ↑':1,
'PSI Attack ↑':1,
'57.':1,
'Fire & Explosion Attack ↑':1,
'59':1,
'Electric Attack ↑':1,
#60
'Energy-Shot Attack ↑':1,
'Water & Ice Attack ↑':1,
'Magic Resist ↑':1,
'PSI Resist ↑':1,
'65':1,
'Fire/Explosion Resist ↑':1,
'67':1,
'68':1,
'Electric Resist ↑':1,
'Energy-Shot Resist ↑':1,
#70
'71':1,
'Water/Freezing Resist ↑':1,
'Aura Resist ↑':1,
'74':1,
'Slumber Immunity':1,
'Ice-Floor Immunity':2,
'Falling Immunity':1,
'Bury Immunity':1,
'Braking Ability ↑':1,
'Mobility.':1,
#80
'Landing Lag ↓':1,
'Lightweight':1,
'Shield Damage ↑':1,
'Air Attack ↑':1,
'Air Defense ↑':1,
'Neutral Special ↑':1,
'Side Special ↑':1,
'Up Special ↑':1,
'Down Special ↑':1,
'Strong Throw':1,
#90
'Unflinching Charged Smashes':2,
'Toss & Meteor':1,
'93':1,
'Critical Hit ↑':1,
'Swimmer':1,
'Shield Durability ↑':1,
'Improved Escape':1,
'98':1,
'99':2,
'100':1,
#100
'Battering Items ↑':1,
'Shooting Items ↑':1,
'Thrown Items ↑':1,
'KOs Heal Damage':1,
'Invincibility after Eating':2,
'Stats ↑ after Eating':1,
'107':1,
'First-Strike Advantage':2,
'109':1,
'Running Start':2,
#110
'111':1,
'Fast Final Smash Meter':2,
'Instadrop':2,
'Healing Shield':2,
'115':1,
'116':1,
'Floaty Jumps':1,
'118':1,
'Irreversible Controls':2,
'Recovery Items ↑':1,
#120
'ransformation Duration ↑':1,
'Undamaged Attack ↑':1,
'Undamaged Speed ↑':1,
'Undamaged Attack & Speed ↑':1,
'125':1,
'126':1,
'Edge Grab ↑':1,
'Impact Run':1,
'129':1,
'Lava-Floor Resist':1,
#130
'Item Gravitation':1,
'132':1,
'Chance of Double Final Smash':2,
'Double Final Smash':3,
'135':2,
'136':2,
'Metal and Giant':3,
'Giant':2,
'Dash Attack ↑':1,
'Armor Knight':2,
#140
'141':1,
'Energy Shot Attack/Resistance ↑':2,
'Hammer Duration ↑':1,
'Boomerang Equipped':1,
'Item Attack ↑':1,
'146':1,
'147':1,
'148':2,
'149':2,
'150':1,
#150
'Perfect-Shield Reflect':1,
'Weapon Attack & Move Speed ↑':2,
'Shooting Attack ↑':1,
'Charge Speed & Power ↑':3,
'155':1,
'Screen-Flip Immunity':2,
'Fog Immunity':2,
'Gravity-Change Immunity':2,
'Stamina ↑':1,
'Strong-Wind Resist':1,
#160
'Strong-Wind Immunity':2,
'Critical-Health Healing':2,
'Special-Move Power ↑':1,
'164':2,
'Bob-omb Equipped':1,
'Hothead Equipped':2,
'Super Leaf Equipped':1,
'Super Launch Star Equipped':1,
'Super Launch Star Equipped?':1,
'Death\'s Scythe Equipped':1,
#170
'Mr. Saturn Equipped':1,
'Unira Equipped':1,
'Rocket Belt Equipped':1,
'Black Hole Equipped':2,
'175':1,
'Stats ↑↑ after Eating':2,
'177':2,
'Critical-Health Stats ↑↑':2,
'Critical-Health Stats ↑↑?':1,
'Great Autoheal':3,
#180
'Steel Diver Equipped':2,
'Banana Gun Equipped':1,
'Rage Blaster Equipped':1,
'Staff Equipped':1,
'Fire Bar Equipped':1,
'Screw Attack Equipped':2,
'Bomber Equipped':1,
'Cucco Equipped':1,
'Neutral Attack ↑':1,
'Neutral Attack ↑↑':1,
#190
'Tilt Attack ↑':1,
'Tilt Attack ↑↑':1,
'Air Attack ↑↑':1,
'Mighiy Throw':1,
'Special-Move Power ↑↑':1,
'Super Easy Dodging':1,
'197':1,
'Landing Lag ↓↓':1,
'Become Heavy':1,
'Meteor Smashes ↑':1,
#200
'Poisoned Smash':1,
'No Penalty for Continuous Dodging':1,
'Airborne Endurance':1,
'Sprinting Endurance':1,
'Perfect-Shield Recovery':1,
'Masterful Fall Brak':1,
'207':1,
'Attack ↑ When Healthy':1,
'Defense ↑ When Healthy':1,
'Endless Smash Holding':1,
#210
'Heal with Smash Attacks':1,
'Activities ↑':1,
'Giant Killer':1,
'Metal Killer':1,
'Assist Killer':1,
'Jam FS Charge':2,
'Weapon Resist ↑':2,
'Hyper Smash Attacks?':1,
'Neutral Attack ↑?':1,
'Tilt Attack ↑?':1,
#220
'Special-Move Power ↑?':1,
'Air Attack ↑?':1,
'223':0,
'224':0,
'225':0,
'226':0,
'227':0,
'228':0,
'229':0,
'230':0,
#230
'231':0,
'232':0,
'233':0,
'234':0,
'235':0,
'236':0,
'237':0,
'238':0,
'239':0,
'240':0,
#2400
'241':0,
'242':0,
'243':0,
'244':0,
'245':0,
'246':0,
'247':0,
'248':0,
'249':0,
'250':0,
#250
'251':0,
'252':0,
'253':0,
'254':0
			}
MoveNames = list(MoveCodeList.keys())

MoveList =[k for k in MoveCodeList if not k.isdigit() and MoveCodeList[k] > 0]




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

	i = len(ssb.ds1['un0'])
	for i in range(0,i):
		tet_UM0[i].set(hex(ssb.ds1['un0'][i]))
		i =+1
	txt_Move_num_1.set(ssb.ds1['move1'])
	txt_Move_num_2.set(ssb.ds1['move2'])
	txt_Move_num_3.set(ssb.ds1['move3'])

	txt_Move_1.set(MoveNames[int(ssb.ds1['move1'])])
	if MoveCodeList[MoveNames[int(ssb.ds1['move1'])]] == 2:
		txt_Move_2.set('')
		txt_Move_3.set(MoveNames[int(ssb.ds1['move3'])])

	elif MoveCodeList[MoveNames[int(ssb.ds1['move1'])]] == 3:
		txt_Move_2.set('')
		txt_Move_3.set('')
	else:
		txt_Move_2.set(MoveNames[int(ssb.ds1['move2'])])
		if MoveCodeList[MoveNames[int(ssb.ds1['move2'])]] == 2:
			txt_Move_3.set('')
		else:
			txt_Move_3.set(MoveNames[int(ssb.ds1['move3'])])

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
	ssb.setMove1(MoveNames.index(txt_Move_1.get()))
	if MoveCodeList[txt_Move_1.get()] == 2:
		ssb.setMove2(0)
		ssb.setMove3(MoveNames.index(txt_Move_3.get()))
	elif MoveCodeList[txt_Move_1.get()] == 3:
		ssb.setMove2(0)
		ssb.setMove3(0)
	else:
		ssb.setMove2(MoveNames.index(txt_Move_2.get()))
		if MoveCodeList[txt_Move_2.get()] == 2:
			ssb.setMove3(0)
		else:
			ssb.setMove3(MoveNames.index(txt_Move_3.get()))

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
		print(call("./amiitool -e -k ./retail.key -o "+fName +" -i "+curentfile,stderr=subprocess.STDOUT, shell=True))
		file = open(curentfile, "rb+")
		handaleFile()

def Decrypt():
	global file
	fName = filedialog.askopenfilename(filetypes = (("Amiibo","*.bin"),("Amiibo","*.bin")))
	if fName:
		print(call("./amiitool -d -k ./retail.key -i "+fName +" -o "+fName+"d",stderr=subprocess.STDOUT, shell=True))
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
def Move_1_change(event):
	print(event)
	txt_Move_num_1.set(str(MoveNames.index(event)))

def Move_2_change(event):
	print(event)
	txt_Move_num_2.set(str(MoveNames.index(event)))

def Move_3_change(event):
	print(event)
	txt_Move_num_3.set(str(MoveNames.index(event)))


def Move_1_Update():
	if(txt_Move_num_1.get()):
		name = MoveNames[int(txt_Move_num_1.get())]
		print(name)
		txt_Move_1.set(name)
	return True

def Move_2_Update():
	if(txt_Move_num_2.get()):
		name = MoveNames[int(txt_Move_num_2.get())]
		print(name)
		txt_Move_2.set(name)
	return True

def Move_3_Update():
	if(txt_Move_num_3.get()):
		name = MoveNames[int(txt_Move_num_3.get())]
		print(name)
		txt_Move_3.set(name)
	return True

window = Tk()
key_file = Path("./retail.key").is_file()

chk_state_learn = BooleanVar() 
chk_state_learn.set(False)
 
window.title("SSBU Amiibo editor")
window.geometry('840x480')

menu = Menu(window)
 
new_item = Menu(menu, tearoff=0)
 
new_item.add_command(label='Open',command=OpenCmd)
 
sv_cmd = new_item.add_command(label='Save',command=SaveCmd,state='disabled')


if(key_file):
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

txt_Move_1 = StringVar(menu)
txt_Move_2 = StringVar(menu)
txt_Move_3 = StringVar(menu)

txt_Move_num_1 = StringVar(menu)
txt_Move_num_2 = StringVar(menu)
txt_Move_num_3 = StringVar(menu)


lbl_Move_1 = Label(window, text="Move 1: ")
lbl_Move_1.grid(column=0, row=1)
popup_Move_1 = OptionMenu(window, txt_Move_1, *MoveList ,command = Move_1_change )
popup_Move_1.grid(row = 1, column =1)
ent_Move_num_1 = Entry(window,width=10,textvariable= txt_Move_num_1, validate="focusout", validatecommand=Move_1_Update)
ent_Move_num_1.grid(column=2, row=1)

lbl_Move_2 = Label(window, text="Move 2: ")
lbl_Move_2.grid(column=0, row=2)
popup_Move_2 = OptionMenu(window, txt_Move_2, *MoveList, command = Move_2_change )
popup_Move_2.grid(row =2, column =1)
ent_Move_num_2 = Entry(window,width=10,textvariable= txt_Move_num_2, validate="focusout", validatecommand=Move_2_Update)
ent_Move_num_2.grid(column=2, row=2)

lbl_Move_3 = Label(window, text="Move 3: ")
lbl_Move_3.grid(column=0, row=3)
popup_Move_3 = OptionMenu(window, txt_Move_3, *MoveList, command = Move_3_change )
popup_Move_3.grid(row = 3, column =1)
ent_Move_num_3 = Entry(window,width=10,textvariable= txt_Move_num_3, validate="focusout", validatecommand=Move_3_Update)
ent_Move_num_3.grid(column=2, row=3)

Scrollbar(popup_Move_1, orient="vertical")
Scrollbar(popup_Move_2, orient="vertical")
Scrollbar(popup_Move_3, orient="vertical")


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