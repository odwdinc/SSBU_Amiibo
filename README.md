# SSBU_Amiibo
Just a start for the Amiibo editor 

you will need to porvide your own Amiibo Keys in retail.key for Encription and Decription to work

Need python3 and tkinter for the Ui,

you will need to compile amiitool. 
  you probley just need build-essential
    sudo apt update
    sudo apt install build-essential
  run setup.sh to build and install, this shoud install amiitool to /usr/local/bin/amiitool.
  conferm by running 'which amiitool'
  
Just run ui.py to start

You can allso pass your Decripted Amiibo to amiibo_class.py for re-signing the data block.
