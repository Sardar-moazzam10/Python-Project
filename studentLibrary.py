from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import json
import os
import sys
from datetime import datetime, timedelta

_env_path = os.environ.get("LIB_DATA_FILE")
_arg_path = sys.argv[1] if len(sys.argv) > 1 else None

try:
    _base_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # __file__ may not exist in some interactive environments
    _base_dir = os.getcwd()

if _env_path:
    DATA_FILE = _env_path
elif _arg_path:
    DATA_FILE = _arg_path
else:
    DATA_FILE = os.path.join(_base_dir, "library_data.json")

# If user accidentally gives a directory path, append filename
if os.path.isdir(DATA_FILE):
    DATA_FILE = os.path.join(DATA_FILE, "library_data.json")


def parse_iso(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def safe_int_input(prompt: str) -> Optional[int]:
    try:
        raw = input(prompt)
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "":
            return None
        return int(raw)
    except ValueError:
        print("❌ Invalid input. Must be a number.")
        return None
    except (KeyboardInterrupt, EOFError):
        print("\n❌ Input cancelled.")
        return None


@dataclass
class Student:
    name: str
    reg_id: int


@dataclass
class Book:
    book_id: int
    name: str
    price: int
    available: bool = True


@dataclass
class Loan:
    book_id: int
    student_reg_id: int
    borrowed_at: Optional[str]
    due_at: Optional[str]
    returned_at: Optional[str] = None
    loan_id: Optional[int] = None


class Library:
    def __init__(self, data_file: str = DATA_FILE):
        # If constructor gets a folder path, append filename
        if os.path.isdir(data_file):
            data_file = os.path.join(data_file, "library_data.json")
        self.data_file = data_file
        self.book_list: List[Dict] = []
        self.student_list: List[Dict] = []
        self.loan_list: List[Dict] = []

    def load(self):
        if not os.path.exists(self.data_file):
            # No saved data yet — start fresh
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print("⚠️ Failed to parse JSON data file:", e)
            return
        except Exception as e:
            print("⚠️ Failed to open data file:", e)
            return

        # Normalize books defensively and support legacy key "avaliable"
        raw_books = data.get("book_list", []) or []
        normalized = []
        for b in raw_books:
            normalized.append({
                "book_id": b.get("book_id"),
                "name": b.get("name", "<unknown>"),
                "price": b.get("price", 0),
                "available": b.get("available", b.get("avaliable", True))
            })
        self.book_list = normalized
        self.student_list = data.get("student_list", []) or []
        self.loan_list = data.get("loan_list", []) or []

    def save(self):
        data = {
            "book_list": self.book_list,
            "student_list": self.student_list,
            "loan_list": self.loan_list,
        }
        tmp = f"{self.data_file}.tmp"
        try:
            dirpath = os.path.dirname(self.data_file) or "."
            os.makedirs(dirpath, exist_ok=True)
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            os.replace(tmp, self.data_file)  # atomic replace across platforms
        except Exception as e:
            print("❌ Error saving data:", e)
            # attempt to cleanup tmp file
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass

    def library_menu(self):
        menu_text = """
Welcome To "Student Library Management System 📚"

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
"""
        print(menu_text)

    # ---------- Book Methods ----------
    def add_books(self):
        n = safe_int_input("Enter number of books to add: ")
        if not n or n <= 0:
            print("Nothing to add.")
            return

        for i in range(n):
            while True:
                book_id = safe_int_input(f"Enter unique Book ID {i+1}: ")
                if book_id is None:
                    continue
                if any(b.get("book_id") == book_id for b in self.book_list):
                    print("ID already exists. Try another.")
                    continue
                break
            name = input(f"Enter Name of Book {i+1}: ").strip()
            if not name:
                print("Name empty. Skipping this book.")
                continue
            price = safe_int_input(f"Enter Price of Book {i+1}: ")
            if not price or price <= 0:
                print("Invalid price. Skipping.")
                continue
            self.book_list.append({"book_id": book_id, "name": name, "price": price, "available": True})
            print(f"✅ Book '{name}' added successfully.")

    def view_books(self):
        if not self.book_list:
            print("Library empty.")
            return
        for b in self.book_list:
            status = "Available" if b.get("available", True) else "Borrowed"
            print(f"ID: {b.get('book_id')} | Name: {b.get('name')} | Price: {b.get('price')} | {status}")

    def search_books(self):
        book_id = safe_int_input("Enter Book ID to search: ")
        if book_id is None:
            return
        book = next((b for b in self.book_list if b.get("book_id") == book_id), None)
        if book:
            status = "Available" if book.get("available", True) else "Borrowed"
            print(f"Found -> ID: {book.get('book_id')} | Name: {book.get('name')} | Price: {book.get('price')} | {status}")
        else:
            print("Book not found.")

    def remove_books(self):
        book_id = safe_int_input("Enter Book ID to remove: ")
        if book_id is None:
            return
        book = next((b for b in self.book_list if b.get("book_id") == book_id), None)
        if not book:
            print("Book not found.")
            return
        if any(l for l in self.loan_list if l.get("book_id") == book_id and l.get("returned_at") is None):
            print("Cannot remove. Book is borrowed.")
            return
        self.book_list.remove(book)
        print(f"✅ Book '{book.get('name')}' removed.")

    # ---------- Student Methods ----------
    def register_student(self):
        n = safe_int_input("Enter number of students to register: ")
        if not n or n <= 0:
            return
        for i in range(n):
            while True:
                reg_id = safe_int_input(f"Enter unique Reg ID for student {i+1}: ")
                if reg_id is None:
                    continue
                if any(s.get("reg_id") == reg_id for s in self.student_list):
                    print("ID exists. Try another.")
                    continue
                break
            name = input(f"Enter Name for student {i+1}: ").strip()
            if not name:
                print("Name empty. Skipping.")
                continue
            self.student_list.append({"reg_id": reg_id, "name": name})
            print(f"✅ Student '{name}' registered.")

    def view_students(self):
        if not self.student_list:
            print("No students registered.")
            return
        for s in self.student_list:
            print(f"ID: {s.get('reg_id')} | Name: {s.get('name')}")

    def remove_student(self):
        reg_id = safe_int_input("Enter Student Reg ID to remove: ")
        if reg_id is None:
            return
        student = next((s for s in self.student_list if s.get("reg_id") == reg_id), None)
        if not student:
            print("Student not found.")
            return
        if any(l for l in self.loan_list if l.get("student_reg_id") == reg_id and l.get("returned_at") is None):
            print("Cannot remove. Student has borrowed books.")
            return
        self.student_list.remove(student)
        print(f"✅ Student '{student.get('name')}' removed.")

    # ---------- Borrow & Return ----------
    def borrow_book(self, max_loans_per_student: int = 3):
        if not self.book_list:
            print("Library has no books.")
            return
        if not self.student_list:
            print("No students registered.")
            return

        reg_id = safe_int_input("Enter Student Reg ID: ")
        book_id = safe_int_input("Enter Book ID to borrow: ")
        if reg_id is None or book_id is None:
            return

        student = next((s for s in self.student_list if s.get("reg_id") == reg_id), None)
        book = next((b for b in self.book_list if b.get("book_id") == book_id), None)
        if not student:
            print("Student not found.")
            return
        if not book:
            print("Book not found.")
            return
        if not book.get("available", True):
            print("Book already borrowed.")
            return

        # enforce max concurrent loans per student
        active_loans_for_student = [
            l for l in self.loan_list
            if l.get("student_reg_id") == reg_id and l.get("returned_at") is None
        ]
        if len(active_loans_for_student) >= max_loans_per_student:
            print(f"Student already has {len(active_loans_for_student)} active loans (limit {max_loans_per_student}).")
            return

        now = datetime.now()
        # create a simple loan_id
        next_loan_id = max((l.get("loan_id", 0) for l in self.loan_list), default=0) + 1
        loan = {
            "loan_id": next_loan_id,
            "book_id": book_id,
            "student_reg_id": reg_id,
            "borrowed_at": now.isoformat(),
            "due_at": (now + timedelta(days=14)).isoformat(),
            "returned_at": None
        }
        book["available"] = False
        self.loan_list.append(loan)
        print(f"✅ Book '{book.get('name')}' borrowed by '{student.get('name')}'. Due: {loan.get('due_at')}")

    def return_book(self):
        book_id = safe_int_input("Enter Book ID to return: ")
        if book_id is None:
            return

        # find an active loan for that book (most recently borrowed if multiples)
        active_loans = [l for l in self.loan_list if l.get("book_id") == book_id and l.get("returned_at") is None]
        if not active_loans:
            print("No active loan found for this book.")
            return
        # choose the latest borrowed (in case of weird duplicates)
        loan = max(active_loans, key=lambda L: parse_iso(L.get("borrowed_at")) or datetime.min)

        now = datetime.now()
        loan["returned_at"] = now.isoformat()

        due_dt = parse_iso(loan.get("due_at"))
        if due_dt is not None and now > due_dt:
            late_days = (now - due_dt).days
            fine = late_days * 10
            print(f"⚠️ Late by {late_days} day(s). Fine: {fine} units.")
        else:
            print("✅ Returned on time. No fine.")

        # mark book available again (if book record exists)
        book = next((b for b in self.book_list if b.get("book_id") == book_id), None)
        if book:
            book["available"] = True
        else:
            print("⚠️ Warning: returned book not found in book list.")

    # ---------- Loans ----------
    def list_active_loans(self):
        active = [l for l in self.loan_list if l.get("returned_at") is None]
        if not active:
            print("No active loans.")
            return
        for l in active:
            print(f"Loan ID: {l.get('loan_id')} | Book ID: {l.get('book_id')} | Student: {l.get('student_reg_id')} | Due: {l.get('due_at')}")

    def list_overdue_loans(self):
        now = datetime.now()
        overdue = []
        for l in self.loan_list:
            if l.get("returned_at") is not None:
                continue
            due_dt = parse_iso(l.get("due_at"))
            if due_dt is None:
                continue
            if due_dt < now:
                overdue.append(l)

        if not overdue:
            print("No overdue loans.")
            return
        for l in overdue:
            due = l.get("due_at") or "<unknown>"
            print(f"Loan ID: {l.get('loan_id')} | Book ID: {l.get('book_id')} | Student: {l.get('student_reg_id')} | Due: {due}")

    # ---------- Exit ----------
    @staticmethod
    def exit_library():
        print("Goodbye 👋")
        raise SystemExit

    # ---------- Menu mapping ----------
    def menu_actions(self):
        return {
            1: self.add_books,
            2: self.view_books,
            3: self.search_books,
            4: self.remove_books,
            5: self.register_student,
            6: self.view_students,
            7: self.borrow_book,
            8: self.return_book,
            9: self.list_active_loans,
            10: self.list_overdue_loans,
            0: self.exit_library
        }


# ---------- Menu Loop ----------
def main():
    lib = Library()
    lib.load()

    while True:
        lib.library_menu()
        choice = safe_int_input("Enter your choice: ")
        if choice is None:
            continue

        action = lib.menu_actions().get(choice)
        if action:
            action()
            lib.save()  # Auto-save after each operation
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
