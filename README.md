# Splatoon-3-Only-Up
A level generator for Splatoon 3

This is the first early release. Most levels generated should be beatable.
This mod should be online safe as it only edits the level files

## How to run:

Clone this repository and make sure you have Python 3.8+ installed

Open the folder in a command prompt and install dependencies by running:  
`py -3.8 -m pip install -r requirements.txt` (on Windows)  
`python3 -m pip install -r requirements.txt` (on Mac)  
`python3 -m pip install $(cat requirements.txt) --user` (on Linux)

Then run the code with:  
`py -3.8 main.py` (on Windows)  
`python3 main.py` (on Mac)  
`python3 main.py` (on Linux)  

Before running the code, create a folder named `output` and put all the level files that you want to mod inside.
The level files are located in the game's RomFS at `romfs/Pack/Scene`

## How to play:

To play the levels, you will either need a homebrewed Switch console or a Nintendo Switch emulator

Switch: On the root of your SD card, create a folder structure like `atmosphere/contents/0100C2500FC20000/romfs/Pack/Scene`.
Drag the modified files from the output folder into the created folder.
After this, simply start up Splatoon 3 while in CFW and enjoy the levels!

Emulator: Inside the Splatoon 3 mods directory, create a folder structure like `Only Up!/romfs/Pack/Scene`.
Drag the modified files from the output folder into the created folder.
After this, simply start up Splatoon 3 with the mod enabled and enjoy the levels!
