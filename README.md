# N64 ROM metadata
This is a filesystem database that can be used by flashcart and menu emulators to better organise ROM information.


## Structure
It uses the following files organised by the ROM's Game code (each character as sub folders) within the `metadata` folder:
* boxart_front.png
* boxart_back.png
* boxart_spine.png
* gamepak_front.png
* description.txt

### Game Code
The [Game Code](https://n64brew.dev/wiki/ROM_Header) is 4 characters long consisting of:
* The category code (one character)
* The unique code (two characters)
* The media-type/destination code (one character)
  
For instance, Goldeneye USA would be `metadata/N/G/E/E`.

### Why this is needed
For speed on flashcarts, traversing multiple files by filename is slow, whereas accessing them by folder is exponentially faster.


## Description
This is the first paragraph contained on the back of the boxart as a description shown to the menu.
A good place to start when deciding which ones to add first would be: https://www.nintendolife.com/guides/50-best-nintendo-64-games-of-all-time#top-10


## Images
Before they can be used, they need to be converted to either:
* sprites.
* png images reduced in size.

So that they can be consumed at a reasonable speed.

This will (hopefully) happen as a release lib.

We can also generate a `thumbnail`, which can be consumed by the menu and may help.

### Image sizes
Suggested image sizes:
- American/European N64 boxart images are landscape: 158x112.
- Japanese N64 boxart images are generally portrait: 112x158.
- 64DD boxart images are CD case square.
- GamePak images are landscape: 158x112.


## to sort
All files in the `to_sort` folder have not yet been added to the metadata and need adding/converting.

Also:
* Sub Folders in the `metadata` folder are unlikely to contain all expected images.
* Sub Folders in the `metadata` folder are unlikely to contain `description.txt` files and contents.
* There is no new/current boxart available (yet) for PAL ROM's.


## Releases
Run the `generate_release.ps1` script.
It currently only handles files called `description.txt`

Files contained in the directory of `media-type/destination code` with a type of `E` will be moved to parent `unique code` directory to use them as a failback (rather than multiple duplicate files for each).

### TODO:
- Generate a script to reduce sizes of PNG images for release.
- Generate a script to use libDragon sprites rather than PNG images for release.

## Atributions
ABeezy from: 
* https://forums.launchbox-app.com/files/category/127-nintendo-64/
