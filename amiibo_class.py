#!/usr/bin/env python3
import sys, struct
from pathlib import Path
from collections import namedtuple
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
		self.ds1 =0
		self.ds = namedtuple('ds', 'learn un0 move1 move2 move3 un1 xp un2 atc hp un3 gift')
		self.DataPatern = "<?9sBBB91sIHhh1sH"
		self.DataOffset = 0x02
		self.unpackData()

	def calLevel(self, xp):
		x = xp / 1000000
		y = int(11.950147 + 0.2657001*x - 0.0004574763*x**2)
		return y

	def calXP(self,lev):
		y = 485 - 25.46969*lev + 0.4188126*lev**2
		return int(y * 1000000)

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

	def unpackData(self):
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
		DBName = "db_"+fName
		my_file = Path(DBName)
		if my_file.is_file():
			print("updateing DataBlock")
			ssb.dataBlockFromeFile(DBName)
			ssb.unpackData()
		else:
			ssb.dataBlockToFile(DBName)

		#ssb.setLevel(ssb.calXP(45))

		for cc in ssb.ds1:
			if not "un" in cc:
				print(cc, ssb.ds1[cc])
		
		#print()
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