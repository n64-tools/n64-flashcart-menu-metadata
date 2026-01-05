[![#yourfirstpr](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](https://github.com/n64-tools/n64-flashcart-menu-metadata/blob/main/CONTRIBUTING.md)

# N64 ROM metadata
This is a filesystem database that can be used by flashcart and menu emulators to better organise ROM information.
It is initially designed for use as metadata for the [N64 Flashcart Menu](https://github.com/Polprzewodnikowy/N64FlashcartMenu)

It works towards fully implementing the [ROM Metadata](https://n64brew.dev/wiki/ROM_Metadata) structure.

## Structure
It uses the following files organised by the ROM's Game code (each character as sub folders) within the `metadata` folder:

- boxart_front.png
- boxart_back.png
- boxart_top.png
- boxart_bottom.png
- boxart_left.png
- boxart_right.png
- gamepak_front.png
- gamepak_back.png
- description.txt
- metadata.ini

### Game Code
The [Game Code](https://n64brew.dev/wiki/ROM_Header) is 4 characters long consisting of:
- The category code (one character)
- The unique code (two characters)
- The media-type/destination code (one character)

For instance, Goldeneye USA would be `metadata/N/G/E/E`.

> [!TIP]
> destination-market-region `E` will be used as the fallback ROM description text (when available), other destination-market-region folders will be used if the destination-market-region is different and the description file exists.

> [!WARNING]
> destination-market-region ROM's may contain multiple languages. We (currently) only aim to support English.

### Why this is needed
For speed on flashcarts, traversing multiple files by filename is slow, whereas accessing them by folder is exponentially faster.

## Description
This should be (at least) the first paragraph contained on the back of the original boxart. It will be used within the menu as a description of the ROM to give the atmosphere of a game, without being able to read the original back boxart text (due to screen resolution).

> [!TIP]
> A good place to start when deciding which ones to add first (via pull requests) would be: https://www.nintendolife.com/guides/50-best-nintendo-64-games-of-all-time

## Metadata
A `metadata.ini` file implementing the [ROM metadata.ini](https://n64brew.dev/wiki/ROM_Metadata) file structure for external metadata.

## Images
Before they can be used, they need to be converted to either:
- png images reduced in size.
- jpg images reduced in size (not supported yet).

So that they can be consumed at a reasonable speed.

We could also generate a `thumbnail` or sprites, which can be consumed by the menu and may help.

### Suggested reduced image sizes:
When processing:
- American/European N64 front and back boxart images are landscape, e.g. 158x112.
- Japanese N64  front and back boxart images are generally portrait, e.g. 112x158.
- 64DD boxart  front and back images are generally CD case square, e.g. 129x112.
- GamePak images are generally landscape, e.g. 158x112.
- Boxart top and bottom images are generally landscape, e.g. 158x22.

## to sort
All files in the `to_sort` folder have not yet been added to the metadata and need adding/converting.

Also:
- Files already added to the `metadata` folder are likely named incorrectly.
- Folders are unlikely to not contain `description.txt` files and contents.
- There is no new/current boxart available (yet) for PAL ROM's.


## Releases
- Run `release_generate_resized_images.py -- clean` to generate reduced size images.
- Run `release_generate_descriptions.py` to add `description.txt`.

Files contained in the directory of `media-type/destination code` with a type of `E` will be moved to parent `unique code` directory to use them as a failback (rather than multiple duplicate files for each).


## Atributions
ABeezy from: 
* https://forums.launchbox-app.com/files/category/127-nintendo-64/
