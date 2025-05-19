# N64 ROM metadata

This is a filesystem database that can be used by flashcart and menu emulators to better organise ROM information.

## Structure
It uses the following files organised by the ROM ID (each character as sub folders):

* boxart_front.png
* boxart_back.png
* boxart_spine.png
* gamepak_front.png
* description.txt

### Why this is needed
For speed on flashcarts, traversing multiple files by filename is slow, whereas accessing them by folder is exponentially faster.

## Description
This is the first paragraph contained on the back of the boxart as a description shown to the menu.

## Images
Before they can be used, they need to be converted to either:

* be sprites
* be reduced in size

So that they can be consumed at a reasonable speed.

This will (hopefully) happen as a release lib.

We can also generate a `thumbnail`, which may help.


## Atributions
ABeezy from: 
* https://forums.launchbox-app.com/files/category/127-nintendo-64/