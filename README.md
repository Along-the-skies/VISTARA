# VISTARA

### Local Google 

Ever forgot where you saved a file?

Yeah. Same.

File explorer is not good to find files which saved like Untitled.pdf

So I made **VISTARA**, a local file search engine that searches the actual content of your files.

## What it does

- Searches `.txt`, `.md`, `.pdf`, and `.docx`
- SQLite + FTS5 keyword search
- Semantic search with `sentence-transformers`
- Document chunking
- File change detection
- Sensitive file detection
- Opens files directly

## How it works

```text
Files
 ↓
Scanner
 ↓
SQLite
 ↓
Chunking
 ↓
Keyword + Semantic Search
 ↓
Results
```
## How to use 

Download setup executable from relases --> https://github.com/Along-the-skies/VISTARA/releases/tag/Ship
## Sneak 
https://drive.google.com/file/d/1osAVD3Y9BO_79VajyqJ-u9IGjBYq6If0/view?usp=sharing
NOTE :- First Run will take few minutes to setup database for ur searches (depends on ur files)
NOTE2 :- Every time u open vistara, It will take 2-3 minutes to setup ml model,after that searching can be quick
NOTE3 :- currently able to ingest txt,pdf,docs,md others are unable to search rn

If found a 🪲 feel free to report it
Made for stardance Frictionless mission

Made by ***Vasudev*** aka ***along-the-skies***
