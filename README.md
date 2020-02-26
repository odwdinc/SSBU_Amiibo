# SSBU_Amiibo
Just a start for the Amiibo editor 

you will need to porvide your own Amiibo Keys in key_retail.bin for Encription and Decription to work

Each Amiibo has to be "upgraded" from the SSB format to SSBU, you should see this message in game the first time you scan a fresh Amiibo in SSBU. After the upgraded the tag is marked and the data block is reformatted to the new SSBU preserving some of the SSB data just reformatted, scaled, etc. If the Amiibo has SSBU data in the data block before the upgraded this data will be interpreted as SSB data not SSBU data.

# How To
  * You will need at least 2 tags (Tagmo) or somthing like the N2 Elite. One will need to be have a stock no mods Amiibo.
  * This will then be upgraged in game by SSBU.
  * After the upgraged by SSBU the bin file is read form the Amiibo.
  * This upgraged bin file then can be decrepcted by SSBU_Amiibo
  * Apply any mods and **save** befor encrypting back to a bin fie.
  * Write the new bin file to a new tag (Tagmo) or back to the N2.
  

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
