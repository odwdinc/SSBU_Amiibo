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

# Run the Code

### Find copy of "KEY RETAIL MUST HAVE TO FLASH AMIIBO.zip" or other copy of "key_retail.bin"

### Copy/Extract "key_retail.bin" to folder called Amiibo

### Rename "key_retail.bin" to "retail.key"

### While holding down ctrl+shift right click in the Amiibo folder to get acces to the "Open PowerShell window here"

### Run the UI with the  command "ssbu_amiibo"

### New window will load with UI.
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_7.PNG)


### Go into File menu to access "Decrypt amiibo"
![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_8.PNG)


## Hex editor usage if installed with pip

```console
pyhex
```
