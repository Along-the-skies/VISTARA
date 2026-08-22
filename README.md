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

## How to use 

Download the zip from the github relases --> 
extract and double click to use vistara

NOTE :- First Run will take few minutes to setup database for ur searches (depends on ur files)
NOTE2 :- Every time u open vistara, It will take 2-3 minutes to setup ml model,after that searching can be quick
NOTE3 :- currently able to ingest txt,pdf,docs,md others are unable to search rn

If found a 🪲 feel free to report it
Made for stardance Frictionless mission

Made by ***Vasudev*** aka ***along-the-skies***