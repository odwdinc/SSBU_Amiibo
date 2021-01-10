# SSBU_Amiibo
Just a start for the Amiibo editor 

You will need to provide your own Amiibo Keys in key_retail.bin for Encryption and Decryption to work

Each Amiibo has to be "upgraded" from the SSB format to SSBU, you should see this message in game the first time you scan a fresh Amiibo in SSBU. After the upgraded the tag is marked and the data block is reformatted to the new SSBU preserving some of the SSB data just reformatted, scaled, etc. If the Amiibo has SSBU data in the data block before the upgraded this data will be interpreted as SSB data not SSBU data.


# How To Example:
So, you want to create a Super Smash Bros. Ultimate Amiibo. You will need at least 2 tags (Tagmo) or something like the N2 Elite. One will need to be have a stock no mods Amiibo.

 1. If starting with a legitimate Amiibo skip to step 3
 1. Take unmodified .bin (somthing.bin) file, and write it to a blank Amiibo tag or to the N2 Elite.
 1. Load unmodified Amiibo in SSBU in game (Note, this will perform an update to the Amiibo.)
 1. Choose "Put Away" in SSBU (Note, this will save the updates to the Amiibo.)
 1. Once the Amiibo as been updated in-game, use either TagMo or N2 Elite to get a new .bin file (something_new.bin)
 1. Open the **Amiibo editor**, go to **File->Decrypt**, and select the new .bin file (something_new.bin).
 1. Make any changes to the Amiibo, then **SAVE** (Note: you can confirm the changes by reopening the save file.)
 1. Once you're happy with the changes, go to **File->Encript** and save to a new bin file (something_mod.bin)
 1. With a blank Amiibo tag write the new bin file (somthing_mod.bin) to a tag.
 
 Editor's note: if using TagMo, you can simply use "restore tag" to update the .bin, thereby only using one tag. You may need to check "allow restore to different tag"
 
 # Note on Tagmo - Unknown, as I do not use it. 
TagMo will not recognize it unless you go into the settings and turn off amiibo file browser, and even still, there's an error in loading the amiibo onto the nfc sticker. it should still work.

# Windows 10 64 bit
  Grab the [Release](https://github.com/odwdinc/SSBU_Amiibo/releases)
 
# Run the Code

 Find copy of "KEY RETAIL MUST HAVE TO FLASH AMIIBO.zip" or other copy of "key_retail.bin"
 
 Copy/Extract "key_retail.bin" to folder called \src\dist\windows\ui

 Run the ui.exe

 New window will load with UI.

 Go into File menu to access "Decrypt amiibo"

![Run Code](https://github.com/odwdinc/SSBU_Amiibo/blob/master/docs/RunCode_7.PNG)
