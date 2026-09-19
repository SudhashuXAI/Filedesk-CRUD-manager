# File Desk: CRUD File Manager

A file manager built with Python and Streamlit. Create, read, update and delete files from a clean browser interface, with live file cards and an activity feed.

The project started as a menu-driven console program (`main.py`) and grew into a full web UI (`app.py`).

<!-- Add a screenshot or GIF of the app here: ![File Desk](screenshot.png) -->

## Features

- **Create** a file and write its content
- **Read** any file in the workspace and download it
- **Update** a file: rename it, clear it, append text, or overwrite its content
- **Delete** a file, with a confirmation step to prevent accidents
- **Live dashboard** showing the file count, total size and actions in the session
- **Activity feed** that records every create, read, update and delete
- **Error handling** with clear messages, for example when a file already exists

## Tech stack

- Python 3
- `pathlib` for file operations
- Streamlit for the web interface

## Getting started

1. Clone the repository:

   ```
   git clone https://github.com/SudhashuXAI/file-desk-crud-manager.git
   cd file-desk-crud-manager
   ```

2. Install the dependency:

   ```
   pip install -r requirements.txt
   ```

3. Run the app:

   ```
   streamlit run app.py
   ```

   On Windows, if `pip` or `streamlit` isn't recognized, use `py -m pip install -r requirements.txt` and `py -m streamlit run app.py`.

To try the original console version instead, run `python main.py`.

## Project structure

```
.
├── app.py            # Streamlit web interface
├── main.py           # Original console CRUD program
├── requirements.txt  # Python dependencies
└── workspace/        # Created automatically; all managed files live here
```

## How it works

Every action in the UI runs a real file operation on disk. All files are kept inside the `workspace/` folder, and file names are sanitised so the app can't read or change anything outside it.

## Author

Made by **Sudhanshu Tiwari**.
