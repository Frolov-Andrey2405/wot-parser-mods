# WOT Parser Mods

**WOT Parser Mods** is a Python project designed to automate the parsing, downloading, and extraction of mod files for World of Tanks from the Russian website [wotspeak.org](https://wotspeak.org). The project consists of several scripts that work together to collect mod information, download mod archives, and organize the extracted files for easy use.

## Features

- Parse mod information from wotspeak.org, including title, update date, patch version, and download links.
- Download mod archives automatically, preferring EU/NA/ASIA server variants if available.
- Extract and organize mod files from ZIP and RAR archives.
- Clean up unnecessary files and folders after extraction.
- Organize extracted content into the correct directory structure for further use.

## Project Structure

```
.
├── downloads.py         # Script for downloading mod archives
├── parser.py            # Script for parsing mod info from wotspeak.org
├── unpacking.py         # Script for extracting and organizing mod files
├── json/
│   ├── links.json       # List of mod page URLs to parse
│   └── results.json     # Parsed mod info (output from parser.py, input for downloads.py)
├── download_mods/       # Folder for downloaded mod archives
└── unpacking_mods/      # Folder for extracted mod files
```

## Usage

### 1. Parse Mod Information

Run the parser to collect mod information from the links in `json/links.json`:

```bash
python parser.py
```

- Output: `json/results.json` (contains mod metadata and download links)

### 2. Download Mod Archives

Download all mod archives listed in `json/results.json`:

```bash
python downloads.py
```

- Downloads archives to the `download_mods/` directory.

### 3. Extract and Organize Mods

Extract all downloaded archives and organize the files for use:

```bash
python unpacking.py
```

- Extracts archives from `download_mods/` to `unpacking_mods/`
- Removes unnecessary files and folders

## Requirements

All necessary dependencies for this project are listed in the `requirements.txt` file.  
You can install them with the following command:

```bash
python -m pip install -r requirements.txt
```

## Notes

Along with standard, officially allowed modifications, the scripts may also download cheat mods.
These cheat mods are strictly prohibited by the game’s rules and may lead to account suspension or permanent ban. The content is provided for review and educational purposes only. You use it entirely at your own risk.
