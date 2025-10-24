Student Library Management System 📚

A simple, CLI-based library management project in Python — perfect for your GitHub portfolio.
Clean, minimal, and built with plain Python (no external deps). It stores data in a JSON file and supports adding/removing books & students, borrowing/returning books, listing active/overdue loans, and safe file I/O.

Made to be practical and reliable — old-school values with a new-school vibe. 😎

Features

Add / view / search / remove books

Register / list / remove students

Borrow & return books (with due date and simple fine calculation)

List active loans and overdue loans

Atomic, safe JSON saves (uses a .tmp file and os.replace)

Flexible data file location: environment variable, CLI arg, or default file next to script

Defensive input handling and robust JSON loading

Quick start
Requirements

Python 3.8+ (recommended)

No external packages — just the Python standard library

Run locally

From the repo root:

# default: uses library_data.json next to the script
python library.py

# OR pass a data file path as the first CLI argument:
python library.py /path/to/my_data.json

# OR set environment variable (preferred for repeatable runs):
export LIB_DATA_FILE="/path/to/my_data.json"
python library.py


(Windows PowerShell)

$env:LIB_DATA_FILE = "C:\path\to\my_data.json"
python library.py


The program auto-saves after each operation.

How data file is chosen (no hard-coding)

Priority for DATA_FILE:

LIB_DATA_FILE environment variable (if set)

First CLI argument sys.argv[1] (if provided)

Default file library_data.json located next to the script

If a directory path is given, the code will auto-append library_data.json for you.

Usage (menu guide)

When you run the script you'll see a menu:

 1. Add Book
 2. View Books
 3. Search Books
 4. Remove Books
 5. Register Student
 6. List Students
 7. Borrow Book
 8. Return Book
 9. List Active Loans
10. List Overdue Loans
 0. Quit


Typical flow:

Register students (option 5).

Add books (option 1).

Borrow a book (option 7) — due in 14 days.

Return a book (option 8) — late returns are fined at 10 units/day.

View active/overdue loans (options 9/10).

Example JSON structure

If you open the library_data.json, it looks like:

{
  "book_list": [
    { "book_id": 1, "name": "Clean Code", "price": 2500, "available": true }
  ],
  "student_list": [
    { "reg_id": 101, "name": "Alice" }
  ],
  "loan_list": [
    {
      "loan_id": 1,
      "book_id": 1,
      "student_reg_id": 101,
      "borrowed_at": "2025-10-24T20:00:00",
      "due_at": "2025-11-07T20:00:00",
      "returned_at": null
    }
  ]
}

Notes & tips

OneDrive / synced folders: If you keep the JSON in OneDrive, ensure the file is accessible and not locked by the sync client. The script uses atomic writes to reduce corruption risk.

Duplicate book IDs: Each copy should have a unique book_id. If you want multiple copies of the same title, add multiple book records with different book_ids.

Testing: Delete the library_data.json to reset the database during dev.

Fine calculation: 10 units per late day; this is simple and easily adjustable in code.

Code structure

library.py — main CLI app (contains Library class, dataclasses, helpers)

library_data.json — saved state (auto-created; location per env/arg/default)

TODO / future ideas (nice-to-have for your portfolio)

Add --data-file arg support via argparse (user-friendly flags)

Add unit tests for borrow/return flows

Add logging and a small web UI (Flask / FastAPI) for a demo

Add CSV import/export for bulk data

Add user auth and per-student history view

Contributing

Small PRs welcome. Keep changes minimal and add tests where appropriate. If you fork, update README.md with what you changed.

License

MIT — do your thing, just don’t claim you wrote the original if you didn’t 😉
