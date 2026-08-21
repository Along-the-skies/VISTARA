# VISTARA

## Local File Search Engine aka Local Google

### Did you ever wonder where you saved that file? Was Explorer useful at that time?

Here, I made **VISTARA**, a local file search engine that can find files from that tiny bit of memory left in your brain. 🗿

### Why?

I have also come across situations like this:

I wanted to find a PDF where I remembered typing **"Scratch readme"**, but I had apparently saved it as something like `Untitled().pdf`.

Few months later...

I got cooked. 💀

That's where VISTARA comes in.

Instead of remembering the **exact filename**, you can search using what you remember about the file.

### How does it work?

VISTARA combines:

* 🔎 Keyword search
* 🧠 Semantic search
* ⚡ Hybrid ranking
* 📄 File snippets
* 📂 Direct file opening
* 🛡️ Sensitive-file filtering

It searches your local files instead of sending them to some random cloud service.

### Supported Files

Currently VISTARA can index:

* `.txt`
* `.md`
* `.pdf`
* `.docx`

### How to use?

Currently, I am unable to package this into an `.exe` because of the dependency size.

So for now, you need Python.

#### 1. Clone the repo

```
git clone <your-repository-url>
cd Local-google
```

#### 2. Create a virtual environment

```
python -m venv .venv
```

Activate it:

```
.\.venv\Scripts\Activate.ps1
```

#### 3. Install dependencies

```
pip install -r requirements.txt
```

### Dataset Setup

Before searching, VISTARA needs to build its local search database.

Run:

```
python setup_data.py
```

This will:

1. Scan your available Windows drives.
2. Find supported files.
3. Skip system and development directories.
4. Extract their text.
5. Store the documents in SQLite.
6. Create searchable chunks.
7. Build the FTS5 search indexes.
8. Mark sensitive files.

The scanner skips directories such as:

* `Windows`
* `Program Files`
* `Program Files (x86)`
* `ProgramData`
* `$Recycle.Bin`
* `System Volume Information`
* `.venv`
* `venv`
* `env`
* `node_modules`
* `__pycache__`
* `.git`

> ⚠️ The first scan can take some time depending on how many files are on your drives.

### 4. Start VISTARA

After the dataset has been indexed:

```
python main.py
```

Wait for the UI to show up.

Then search for whatever you remember.

For example:

* `Scratch readme`
* `python project`
* `school notes`
* `that PDF about Godot`

You don't necessarily need to remember the exact filename.

### NOTE ⚠️

The **first search after starting VISTARA can take a few minutes** because the semantic search model (`all-MiniLM-L6-v2`) needs to load.

You may see a Hugging Face message while the model loads.

That's normal.

###  Local Search

VISTARA uses:

* **SQLite FTS5** for keyword search
* **Sentence Transformers** for semantic search
* **Hybrid ranking** to combine both

This means you can search by both exact words and approximate meaning.

###  Built With

* Python
* SQLite
* SQLite FTS5
* Sentence Transformers
* `all-MiniLM-L6-v2`
* PySide6
* QtWebEngine
* HTML
* CSS
* JavaScript

###  Project Status

**VISTARA is currently in its first shippable version.**

It's not an `.exe` yet because of the dependency size...

but it works. 🗿

### Notable features !!

Clean UI
Sensitive content filter (passwords,apis,tokens) and if you were searching that u can see it with sensitive filter off.


**Vistara is alive.**
