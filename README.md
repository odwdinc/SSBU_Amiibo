# SSBU_Amiibo
Just a start for the Amiibo editor 

you will need to porvide your own Amiibo Keys in retail.key for Encription and Decription to work

Need python3, cryptography, and tkinter

ModuleNotFoundError: No module named 'cryptography'

    pip install --user cryptography
    
Just run python ui.py to start

You can allso pass your Decripted Amiibo to amiibo_class.py for re-signing the data block.


# Windows install Guide

## Get python 3.6 [Link](https://www.python.org/downloads/)
![Get Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python.PNG)


### Start the installer, Conferm the "Add to Path" and pick "Customize installation"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_2.PNG)


### Conferm "pip" and "tcl/tk"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_3.PNG)


### Conferm "Install for all users"
![Install Python](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Install_Python_4.PNG)


# Get the Code

### "Download ZIP" form this repo
![Get Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/GetCode.PNG)


### Click the link at the top of this repo to go to [odwdinc/pyamiibo](https://github.com/odwdinc/pyamiibo/tree/fb8fa6e12c3583f180d9582e2214a87565b12b41)
![Get Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/GetCode_2.PNG)


### "Download ZIP" form odwdinc/pyamiibo
![Get Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/GetCode_3.PNG)


# Prep the Code


### Move bouth ZIP files to common folder
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode.PNG)


### Extract the "SSBU_Amiibo-master.zip", check your SSBU_Amiibo-maste folder shoud look as such.
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode_2.PNG)


### Check your pyamiibo folder shoud look empty as such.
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode_3.PNG)


### Open the "pyamiibo-fb8fa6e12c3583f180d9582e2214a87565b12b41.zip" 
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode_4.PNG)


### Extract all the files in to the empty pyamiibo folder.
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode_5.PNG)


### Check your pyamiibo folder shoud now look as such.
![Prep Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/ExtractCode_5.PNG)


# Run the Code

### Find copy of "KEY RETAIL MUST HAVE TO FLASH AMIIBO.zip" or other copy of "key_retail.bin"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode.PNG)


### Copy/Extract "key_retail.bin" to SSBU_Amiibo-master folder
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_2.PNG)


### Rename "key_retail.bin" to "retail.key"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_3.PNG)


### While holding down ctrl+shift right click in the SSBU_Amiibo-master folder to get acces to the "Open PowerShell window here"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_4.PNG)


### Run the UI with the  command "python.exe .\ui.py"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_5.PNG)


### Power shell will out put some info about the Skills this is mostley debug.
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_6.PNG)


### New window will load with UI.
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_7.PNG)


### Go into File menu to access "Decrypt amiibo"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_8.PNG)


# Error??


### On first run you will probley see this as we need to install cryptography
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Error.PNG)


### As you proby dont have permation to install to program files cryptography may faile. 
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Error_2.PNG)


### install cryptography as user. 
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/Error_3.PNG)

### Try running to run the UI with the command "python.exe .\ui.py"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_5.PNG) 


# Install with pip

Install globally (requires root)

```console
sudo python3 -m pip install git+https://github.com/odwdinc/SSBU_Amiibo.git
```

Or install to your users home directory (no root required).

```console
python3 -m pip install --user git+https://github.com/odwdinc/SSBU_Amiibo.git
```

Add the bin directory for python local installs to your PATH in your `~/.bashrc`
file.

```console
export PATH="${PATH}:$(python3 -c 'import site; print(site.USER_BASE)')/bin"
```

## Hex editor usage if installed with pip

```console
pyhex
```
