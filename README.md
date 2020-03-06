# SSBU_Amiibo
Just a start for the Amiibo editor 

you will need to porvide your own Amiibo Keys in key_retail.bin for Encription and Decription to work

Each Amiibo has to be "upgraded" from the SSB format to SSBU, you should see this message in game the first time you scan a fresh Amiibo in SSBU. After the upgraded the tag is marked and the data block is reformatted to the new SSBU preserving some of the SSB data just reformatted, scaled, etc. If the Amiibo has SSBU data in the data block before the upgraded this data will be interpreted as SSB data not SSBU data.


# How To Example:
I want to create a supper SSBU Amiibo. You will need at least 2 tags (Tagmo) or somthing like the N2 Elite. One will need to be have a stock no mods Amiibo.

 1. If starting with a liget Amiibo skip to 3
 1. Take unmodafided .bin (somthing.bin) file write to blank Amiibo tag or to N2 Elite.
 1. Load unmodafided Amiibo in SSBU in game (Note, this will perfrom an update to the Amiibo.)
 1. "Put-Away" Amiibo in SSBU in game (Note, this will save the updates to the Amiibo.)
 1. Once the Amiibo as been updated ingame use eather Tagmo or N2 Elite to get a new bin file (somthing_new.bin)
 1. Open the **Amiibo editor** and go to **File->Decript**, and select the new bin file (somthing_new.bin).
 1. Make any changes to the Amiibo then **SAVE** (Noet. you can conferm the changes by reopening the save file.)
 1. Once happy with changes go to **File->Encript** and save to a new bin file (somthing_mod.bin)
 1. With a blank Amiibo tag write the new bin file (somthing_mod.bin) to a tag.
 
 # Note on Tagmo Unknow as i do not use. 
  Tagmo will not recognize it unless you go into the settings and turn off amiibo file browser, and even still, there's an error in loading the amiibo onto the nfc sticker. it shoue still work.

# Windows 10 64 bit
  Grab the [Release](https://github.com/odwdinc/SSBU_Amiibo/releases)

# Windows build Guide

## Get python 3.? [Link](https://www.python.org/downloads/)
![Get Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python.PNG)


### Start the installer, Conferm the "Add to Path" and pick "Customize installation"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_2.PNG)


### Conferm "pip" and "tcl/tk"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_3.PNG)


### Conferm "Install for all users"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_4.PNG)

## Download and Install Git

### https://git-scm.com/download/win


# Run the Code

### Find copy of "KEY RETAIL MUST HAVE TO FLASH AMIIBO.zip" or other copy of "key_retail.bin"

### Copy/Extract "key_retail.bin" to folder called Amiibo

### While holding down ctrl+shift right click in the Amiibo folder to get acces to the "Open PowerShell window here"

# Install with pip

install to your users home directory.

```console
python -m pip install --user git+https://github.com/odwdinc/SSBU_Amiibo.git
```


### Run the UI with the command 

```console
$env:Path += "$env:APPDATA\Python\Python37\Scripts;"
ssbu_amiibo.exe
```

### New window will load with UI.

### Go into File menu to access "Decrypt amiibo"

![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_7.PNG)

## Hex editor usage if installed with pip

```console
pyhex
```
