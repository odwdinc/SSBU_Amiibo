#!/usr/bin/env python3
import sys, struct
from pathlib import Path
from collections import namedtuple

import json
import urllib.request
import requests
from io import BytesIO
from PIL import Image

class crc32r:
	def __init__(self, p0 = 0xEDB88320):
		p0 |= 0x80000000
		u0 = [0x0] * 0x100
		i = 0x1
		while i & 0xFF:
			t0 = i
			for j in range(0x8):
				b = bool(t0 & 0x1)
				t0 >>= 0x1
				if b : t0 ^= p0
			u0[i] = t0
			i += 0x1
		self.u0 = tuple(u0)
		u0.clear()

	def calc0(self, s, inXOR = 0xFFFFFFFF, outXOR = 0xFFFFFFFF):
		u = self.u0
		t = inXOR
		for k in s : t = (t >> 0x8) ^ u[(k ^ t) & 0xFF]
		return t ^ outXOR

class ssbu:
	def __init__(self,fName):
		self.f = fName
		self.crc32 = crc32r()
		self.f.seek(0xE0, 0x0)
		self.data = bytearray(self.f.read(0xD4))
		self.f.seek(0x1DC, 0x0)
		self.ID = bytearray(self.f.read(8))
		self.ds1 =0
		self.ds = namedtuple('ds', 'learn un0 move1 move2 move3 un1 xp un2 atc hp un3 gift un4 train color un5')
		self.DataPatern = "<?9sBBB93sh2shh1sH17s59sB16s"
		self.DataOffset = 0x02
		self.unpackData()
		self.GetWebData()

	def xpToLev(self,xp):
		for i in levMap:
			if i+1 <= len(levMap):
				if xp >= levMap[i]  and xp < levMap[i+1]:
					levSpacing = levMap[i+1] - levMap[i]
					pos = xp - levMap[i]
					if pos > 0:
						lev = i + (pos/levSpacing)
					else:
						lev = i
					return (lev)
		return(50.0)

	def LevToXp(self,lev):
		if lev > 50:
			return levMap[50]
		else:
			i = int(lev)
			pos = lev - i 
			levSpacing = levMap[i+1] - levMap[i]
			if pos > 0:
				pos  = levMap[i] + int( (levSpacing * pos) + (levSpacing % pos > 0))
			else:
				pos  = levMap[i]
			return pos

	def setLearn(self,learn):
		self.ds1['learn'] = learn

	def setMove1(self,move):
		self.ds1['move1'] = move

	def setMove2(self,move):
		self.ds1['move2'] = move

	def setMove3(self,move):
		self.ds1['move3'] = move

	def setLevel(self,xp):
		self.ds1['xp'] = xp

	def getLevel(self):
		return self.ds1['xp']	

	def setAttack(self,Attack):
		self.ds1['atc'] = Attack

	def getAttack(self):
		return self.ds1['atc']

	def setDefense(self,Defense):
		self.ds1['hp'] = Defense

	def getDefense(self):
		return self.ds1['hp']

	def setGift(self,Gift):
		self.ds1['gift'] = Gift

	def setColor(self,Color):
		self.ds1['color'] = Color
	
	def GetWebData(self):
		self.webdata =  None
		self.img = None
		self.ID = ''.join(format(x, '02x') for x in self.ID)
		req = urllib.request.Request('https://www.amiiboapi.com/api/amiibo/?id='+self.ID)
		try:
			with urllib.request.urlopen(req) as response:
				result = json.loads(response.read().decode("utf-8"))
				self.webdata = result
		except urllib.error.HTTPError as e:
			print("Not Found : https://www.amiiboapi.com/api/amiibo/?id="+ self.ID)
		
		if self.webdata and 'amiibo' in self.webdata:
			response = requests.get(self.webdata['amiibo']['image'])
			self.img = Image.open(BytesIO(response.content))


	def unpackData(self):
		print(len(self.data))
		self.ds1 = self.ds._asdict(self.ds._make(struct.unpack_from(self.DataPatern, self.data, self.DataOffset)))
	
	def packData(self):
		struct.pack_into(self.DataPatern, self.data, self.DataOffset, *list(self.ds1.values()))

	def printData(self):
		s = ""
		c = 0
		for b in self.data:
			s += " 0x{:02x}".format(b)
			#s += " "
			if c > 14:
				s += "\n"
				c = 0
			else:
				c +=1
		print(s)

	def dataBlockToFile(self,fName):
		with open(fName, "wb") as fdb:
			fdb.write(self.data)

	def dataBlockFromeFile(self,fName):
		with open(fName, "rb") as fdb:
			self.data = bytearray(fdb.read(0xD4))

	def sign(self):
		self.packData()
		t = self.crc32.calc0(self.data, 0x0)
		self.f.seek(0xDC, 0x0)
		self.f.write(struct.pack("<I", t))
		self.f.write(self.data)



def sign(fName):
	with open(fName, "rb+") as f:
		ssb = ssbu(f)
		DBName = fName+"_db"
		my_file = Path(DBName)
		if my_file.is_file():
			print("updateing DataBlock")
			ssb.dataBlockFromeFile(DBName)
			ssb.unpackData()
		else:
			ssb.dataBlockToFile(DBName)

		for cc in ssb.ds1:
			if not "un" in cc:
				print(cc, ssb.ds1[cc])
				
		ssb.sign()

 
if __name__ == "__main__":
	if sys.stdin.isatty():
		argv = sys.argv
		if 0x2 <= len(argv) <= 0x3:
			sign(argv[-0x1])
		else:
			print("Usage : fp_resign.py file")
	else:
		pass


levMap = {1:0,
2:8,
3:22,
4:41,
5:63,
6:90,
7:120,
8:155,
9:195,
10:238,
11:284,
12:330,
13:376,
14:426,
15:476,
16:528,
17:580,
18:632,
19:684,
20:737,
21:790,
22:843,
23:896,
24:950,
25:1004,
26:1058,
27:1112,
28:1167,
29:1222,
30:1277,
31:1339,
32:1406,
33:1478,
34:1555,
35:1637,
36:1724,
37:1816,
38:1910,
39:2012,
40:2115,
41:2220,
42:2329,
43:2459,
44:2619,
45:2799,
46:2999,
47:3209,
48:3429,
49:3669,
50:3912
} 

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
'Easier Perfect Shield':1,
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
'57':1,
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
'KOs Heal Damage':2,
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

#@https://www.ssbwiki.com/spirit
Attack_Skills = {
	"Fist Attack ↑":["Slightly increases the power of punches and elbow strikes.",1,1],
	"Foot Attack ↑":["Slightly increases the power of kicks and knee strikes.",1,1],
	"Physical Attack ↑":["Slightly increases the power of punches, kicks, and bites.",2,1],
	"Air Attack ↑":["Slightly increases the power of items and attacks used in the air.",2,1],
	"Strong Throw":["Slightly increases the power of grabbing and throwing attacks.",2,1],
	"Weapon Attack ↑":["Slightly increases the power of swords, whips, hammers, etc.",2,1],
	"Shooting Attack ↑":["Slightly increases the power of projectile weapons such as bows or guns.",2,1],
	"Dash Attack ↑":["Increases tackle and dash attack power, and slightly increases move speed.",2,1],
	"Hyper Smash Attacks":["Increases attack power and smash-attack charge speed.",4,1],
	"Neutral Special ↑":["Slightly increases the power of neutral special moves.",3,1],
	"Side Special ↑":["Slightly increases the power of side special moves.",3,1],
	"Up Special ↑":["Slightly increases the power of up special moves.",3,1],
	"Down Special ↑":["lightly increases the power of down special moves.",3,1],
	"Special-Move Power ↑":["Slightly increases the power of all special moves.",4,1],
	"Aura Attack ↑":["Slightly increases the power of Lucario's Aura attacks.",1,1],
	"Magic Attack ↑":["Slightly increases the power of magic attacks, such as Zelda's and Robin's spells.",1,1],
	"PSI Attack ↑":["Slightly increases the power of Ness's and Lucas's PSI attacks.",1,1],
	"Fire & Explosion Attack ↑":["Slightly increases the power of explosion and fire attacks.",1,1],
	"Water & Ice Attack ↑":["Slightly increases the power of water and ice attacks.",1,1],
	"Electric Attack ↑":["Slightly increases the power of electricity attacks.",1,1],
	"Energy-Shot Attack ↑":["Slightly increases the power of energy attacks, such as Fox's Blaster.",1,1],
	"Toss & Meteor":["Increases upward and downward launch power.",2,1],
	"Shield Damage ↑":["Increases the damage dealt to enemy shields.",3,1],
	"Giant Killer":["Increases the damage dealt to giant opponents.",4,1],
	"Metal Killer":["Increases the damage dealt to metal opponents.",4,1],
	"Assist Killer":["Increases the damage dealt to assist trophies.",4,1],
	"Critical Hit ↑":["Grants a 5% chance to land a devastating critical hit.",3,1],
	"Impact Run":["Damages enemies when dashing into them.",1,1]
}

Defense_Skills ={
	"Shield Durability ↑":["Increases shield strength.",3,1],
	"Easier Perfect Shield":["Widens the window for performing a perfect shield.",3,1],
	"Perfect-Shield Reflect":["Reflects incoming projectiles when you perform a perfect shield.",2,1],
	"Air Defense ↑":["Slightly reduces the damage taken from air attacks.",2,1],
	"Weapon Resist ↑":["Decreases damage taken from melee weapons like swords and whips.",2,2],
	"Aura Resist ↑":["Slightly reduces the damage taken from Lucario's Aura attacks.",1,1],
	"Magic Resist ↑":["Slightly reduces the damage taken from magic attacks, such as Zelda's and Robin's spells.",1,1],
	"PSI Resist ↑":["Slightly reduces the damage taken from Ness's and Lucas's PSI attacks.",1,1],
	"Fire/Explosion Resist ↑":["Slightly reduces the damage taken from explosion and fire attacks.",1,1],
	"Water/Freezing Resist ↑":["Slightly reduces the damage taken from water attacks.",1,1],
	"Electric Resist ↑":["Slightly reduces the damage taken from electricity attacks.",1,1],
	"Energy-Shot Resist ↑":["Slightly reduces the damage taken from energy attacks, such as Fox's Blaster.",1,1],
	"Slow Super Armor":["Makes it more difficult to flinch or be launched, but move speed decreases.",3,2],
	"Super Armor":["Makes it more difficult to flinch or be launched.",4,3],
	"Unflinching Charged Smashes":["Gain super armor while charging smash attacks.",3,2]
 }

Recovery_Skills = {
	"Autoheal":["Recover a small amount of health every five seconds.",3,2],
	"Great Autoheal":["Recovers some health automatically every five seconds.",4,3],
	"Healing Shield":["Recovers health when enemy attacks are shielded.",4,2],
	"KOs Heal Damage":["Recovers health when enemies are KO'd.",3,2],
	"Critical-Health Healing":["Recovers a great deal of health when a certain amount of damage is taken.",3,2],
	"Lifesteal":["Steal opponents' life force when you strike.",0,0]
}


Mobility_Skills = {
	"Move Speed ↑":["Slightly increases left and right move speed.",2,1],
	"Braking Ability ↑":["Makes stopping easier when walking or running.",1,1],
	"Lightweight":["Greatly increases jump and move speed, but become easier to launch.",1,1],
	"Jump ↑":["Increases jump height.",2,1],
	"Floaty Jumps":["Slows your fall speed after jumping.",1,1],
	"Additional Midair Jump":["Increases number of midair jumps by one.",4,2],
	"Landing Lag ↓":["Reduces vulnerability when landing, making movement possible sooner.",1,1],
	"Easier Dodging":["Increases period of invincibility when dodging, and air dodges travel farther.",3,1],
	"Instadrop":["Grants the ability to do a quick-drop attack by tilting down while in the air.",1,2]
}


Item_Skills = {
	"Battering Items ↑":["Increases the power of battering items.",2,1],
	"Shooting Items ↑":["Increases the power and ammo of shooting items.",2,1],
	"Thrown Items ↑":["Increases the distance and power of thrown items.",2,1],
	"Hammer Duration ↑":["Increases the amount of time the Hammer and Golden Hammer items last.",0,0],
	"Item Gravitation":["Draws nearby items closer.",2,1],
	"Beam Sword Equipped":["Start battles with a Beam Sword. Use it to batter opponents.",2,1],
	"Killing Edge Equipped":["Start battles with a Killing Edge. Hit it when it glows for extra power.",2,1],
	"Fire Bar Equipped":["Start battles with a Fire Bar. Bash and burn opponents while it lasts.",1,1],
	"Death's Scythe Equipped":["Start battles with a Death's Scythe. KO badly injured opponents in one hit!",2,1],
	"Lip's Stick Equipped":["Start battles with a Lip's Stick. Hit an opponent with it to slowly drain their health.",1,1],
	"Star Rod Equipped":["Start battles with a Star Rod. Swing it to launch projectiles.",1,1],
	"Ore Club Equipped":["Start battles with an Ore Club. Create a tornado with a smash attack.",3,3],
	"Ray Gun Equipped":["Start battles with a Ray Gun. Fire at opponents from a distance.",2,1],
	"Super Scope Equipped":["Start battles with a Super Scope. Fire multiple shots, or charge up for a stronger blast.",2,2],
	"Steel Diver Equipped":["Start battles with a Steel Diver. Fire powerful shots that are hard to see.",1,2],
	"Rage Blaster Equipped":["Start battles with a Rage Blaster. Deal more damage when you have more damage.",1,1],
	"Banana Gun Equipped":["Start battles with a Banana Gun. Use the leftover peel after you fire.",1,1],
	"Staff Equipped":["Start battles with a Staff. Fire at faraway opponents to deal more damage.",1,1],
	"Drill Equipped":["Start battles with a Drill. Fire a single shot, but if it hits, it keeps on hitting.",1,1],
	"Fire Flower Equipped":["Start battles with a Fire Flower. Shoot fire at opponents.",1,1],
	"Ramblin' Evil Mushroom Equipped":["Start battles with a Ramblin' Evil Mushroom. Spray opponents with it to reverse their controls.",1,1],
	"Green Shell Equipped":["Start battles with a Green Shell. Throw it and it'll slide across the stage.",1,1],
	"Freezie Equipped":["Start battles with a Freezie. Hit opponents with it to freeze them.",1,1],
	"Hothead Equipped":["Start battles with a Hothead. Toss it, and it'll loop around platforms to hit enemies.",1,2],
	"Boomerang Equipped":["Start battles with a Boomerang. Deal damage when you throw it and when it returns.",1,1],
	"Beastball Equipped":["Start battunles with a Beastball. Throw it, and it will warp toward a nearby opponent.",1,1],
	"Unira Equipped":["Start battles with a Unira. Attack it to make spikes come out.",1,1],
	"Mr. Saturn Equipped":["Start battles with a Mr. Saturn. Break enemies' shields easily.",2,1],
	"Bob-omb Equipped":["Start battles with a Bob-omb. Launch foes with its powerful blast.",2,1],
	"Bomber Equipped":["Start battles with a Bomber. Raise it up to cause a huge explosion.",2,1],
	"Black Hole Equipped":["Start battles with a Black Hole. Activate it, and it'll pull in nearby fighters.",3,2],
	"Super Launch Star Equipped":["Start battles with a Super Launch Star. Touch it and get launched.",2,1],
	"Fairy Bottle":["Start battles with a Fairy Bottle. Heal when at least 100% damage is taken.",2,1],
	"Made of Metal":["Start battles in metal form. Become harder to launch.",3,1],
	"Mouthful of Curry":["Start battles with Superspicy Curry breath. Continuously spit out fire.",2,2],
	"Bunny Hood Equipped":["Start battles with a Bunny Hood. Move faster and jump higher.",1,1],
	"Back Shield Equipped":["Start battles with a Back Shield. Guard against attacks from behind.",2,1],
	"Franklin Badge Equipped":["Start battles wearing a Franklin Badge. Reflect enemy projectiles.",3,2],
	"Super Leaf Equipped":["Start battles with a Super Leaf. Press and hold the jump button to float through the air.",1,1],
	"Rocket Belt Equipped":["Start battles with a Rocket Belt. Fly around until it runs out of fuel.",1,1],
	"Screw Attack Equipped":["Start battles with a Screw Attack. Attack with your jumps.",1,2],
	"Stats ↑ after Eating":["Slightly increases attack, defense, and move speed after eating food.",2,1],
	"Stats ↑↑ after Eating":["Greatly increases attack, defense, and move speed after eating food.",3,2],
	"Invincibility after Eating":["Become invincible for a while after eating food.",4,2]
}


Hazard_Skills = {
	"Poison Damage Reduced":["Reduces the damage taken from poison.",2,1],
	"Poison Immunity":["Grants immunity to poison.",3,2],
	"Poison Heals":["Poison heals instead of harms.",4,3],
	"Lava-Floor Resist":["Reduces damage taken from lava floors.",2,1],
	"Lava-Floor Immunity":["Grants immunity to lava floors.",3,2],
	"Ice-Floor Immunity":["Grants immunity to ice floors and freezing attacks.",3,2],
	"Zap-Floor Immunity":["Grants immunity to zap floors and stun attacks.",3,2],
	"Slumber Immunity":["Grants immunity to slumber floors and sleeping in general.",3,1],
	"Sticky-Floor Immunity":["Become immune to sticky floors.",2,2],
	"Strong-Wind Resist":["Reduces the effect of strong winds.",2,1],
	"Strong-Wind Immunity":["Become immune to strong winds.",3,2],
	"Fog Immunity":["Removes fog from the stage.",2,2],
	"Screen-Flip Immunity":["Stops the screen from flipping upside down.",2,2],
	"Irreversible Controls":["Become immune to left-and-right control reversal.",2,2],
	"Gravity-Change Immunity":["Become immune to changes in gravity.",3,2]
}

Other_Skills = {
	"Falling Immunity":["Grants immunity to tripping from earthquakes, Banana Peels, etc.",2,1],
	"Bury Immunity":["Grants immunity to being buried by Pitfalls, bury attacks, etc.",2,1],
	"Swimmer":["Grants the ability to stay in water indefinitely.",1,1],
	"Improved Escape":["Makes grabs and stuns easier to escape.",1,1],
	"Transformation Duration ↑":["Extends the amount of time transformation items like the Super Mushroom last.",1,1],
	"Critical-Health Attack ↑":["Increases attack power for a while when badly damaged.",1,1],
	"Critical-Health Defense ↑":["Increases defense for a while when badly damaged.",1,1],
	"Critical-Health Stats ↑":["Slightly increases attack, defense, and move speed for a while when badly damaged.",2,1],
	"Critical-Health Stats ↑↑":["Increases attack, defense, and move speed for a while when badly damaged.",3,2],
	"Critical Immunity":["Become invincible for a while when badly damaged.",4,2],
	"Trade-Off Attacks ↑":["Start battles with 30% damage and higher attack power.",2,1],
	"Trade-Off Defense ↑":["Start battles with 30% damage and higher defense.",2,1],
	"Trade-Off Speed ↑":["Start battles with 30% damage and increased move speed.",1,1],
	"Trade-Off Ability ↑":["Start battles with 30% damage and slightly increased attack, defense, and move speed.",3,1],
	"Undamaged Attack ↑":["Increases attack power while at 0% damage.",2,1],
	"Undamaged Speed ↑":["Increases move speed while at 0% damage.",1,1],
	"Undamaged Attack & Speed ↑":["Slightly increases attack and move speed while at 0% damage.",3,1],
	"Running Start":["Increases attack, defense, and move speed for a while at the start of the battle.",4,2],
	"First-Strike Advantage":["Become invincible for a while after landing the first hit of the battle.",3,2],
	"Fast Final Smash Meter":["Increases FS Meter charging speed.",4,2],
	"Chance of Double Final Smash":["Sometimes grants a second Final Smash after using a Final Smash.",3,2],
	"Double Final Smash":["Grants a second Final Smash after using a Final Smash.",4,3],
	"Jam FS Charge":["Slows down the charge rate of the opposition's FS Meter.",4,2],
	"Weapon Attack & Move Speed ↑":["Increases the power of melee weapons, and slightly increases move speed.",4,2],
	"Energy Shot Attack/Resistance ↑":["Slightly reduces damage taken from energy attacks, and slightly increases energy attack power.",2,2],
	"Armor Knight":["Reduces move speed, but greatly increases defense and slightly increases attack.",4,2],
	"Stamina ↑":["Start battles with extra stamina when fighting in stamina battles.",1,1]
}


Special_Skills = {
	"Metal and Giant":["Become giant and metal for a while at the start of the battle.",0,0],
	"Giant":["Become giant for a while at the start of the battle.",3,2],
	"Critical Hit ↑↑":["Grants a 12% chance to land a devastating critical hit.",4,2],
}

Skill_Set = {
'Attack':Attack_Skills,
'Defense':Defense_Skills,
'Recovery':Recovery_Skills,
'Mobility':Mobility_Skills,
'Item':Item_Skills,
'Hazard':Hazard_Skills,
'Other':Other_Skills,
'Special':Special_Skills,
}
