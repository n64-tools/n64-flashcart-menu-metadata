[![#yourfirstpr](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://github.com/n64-tools/n64-flashcart-menu-metadata/blob/main/CONTRIBUTING.md)

# N64 ROM metadata
This is a filesystem database that can be used by flashcart and menu emulators to better organise ROM information.
It is initially designed for use as metadata for the [N64 Flashcart Menu](https://github.com/Polprzewodnikowy/N64FlashcartMenu)

## Structure
It uses the following files organised by the ROM's Game code (each character as sub folders) within the `metadata` folder:

* description.txt

### Game Code
The [Game Code](https://n64brew.dev/wiki/ROM_Header) is 4 characters long consisting of:
* The media-type-category code (one character)
* The unique code (two characters)
* The destination-market-region code (one character)

For instance, Goldeneye USA would be `metadata/N/G/E/E`

### Why this is needed
For speed on flashcarts (using FatFS), traversing multiple files by filename is slow, whereas accessing them by folder is exponentially faster.

## Description
This should be (at least) the first paragraph contained on the back of the original boxart. It will be used within the menu as a description of the ROM to give the atmosphere of a game, without being able to read the original text (due to screen resolution).

> [!TIP]
> A good place to start when deciding which ones to add first (via pull requests) would be: https://www.nintendolife.com/guides/50-best-nintendo-64-games-of-all-time
