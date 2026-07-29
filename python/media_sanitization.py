# import all necessary libraries
import html
import shutil
import string
import uuid
import logging
from pathlib import Path

# establish the requirements for the note and uploaded media (2MB)
MAX_NOTE_LENGTH = 2000
ALLOWED_FILE_TYPES = ('.txt', '.jpg', '.jpeg', '.png')
MAX_FILE_SIZE = 2 * 1024 * 1024  
UPLOAD_DIR = Path("uploads")
NOTES_DIR = Path("notes")

# ensure that a directory for the uploads exists
UPLOAD_DIR.mkdir(exist_ok=True)
NOTES_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename="error_log.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# function to validate and sanitize the note uploaded by the user
def sanitize_note(note: str) -> str:
    """Validate and sanitize the user's note."""
    
    # error handling for empty note
    if not note.strip():
        raise ValueError("Note cannot be empty.")
        
    # error handling for notes over 2000 characters
    if len(note) > MAX_NOTE_LENGTH:
        raise ValueError("Note exceeds the maximum length (2000 characters).")

    # remove characters that are potentially malicious
    # error handling for characters that can be considered "unprintable or unsafe"
    for ch in note:
        if ch not in string.printable:
            raise ValueError("Note contains unprintable or unsafe characters.")

    # escape HTML/script tags to prevent code execution
    safe_note = html.escape(note)
    return safe_note

# store sanitized note
def save_note(note: str) -> Path:
    filename = f"note_{uuid.uuid4()}.txt"
    note_path = NOTES_DIR / filename
    note_path.write_text(note, encoding="utf-8")
    return note_path

# validate and store the file in the appropriate path
def validate_and_store_file(file_path: str) -> Path:
    """Validate and safely copy an uploaded file to the uploads directory."""
    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError("File does not exist.")

    # validate the uploaded file type
    # error handling for unsupported file types
    if file.suffix.lower() not in ALLOWED_FILE_TYPES:
        raise ValueError(f"File type '{file.suffix}' not allowed. Allowed types: {ALLOWED_FILE_TYPES}")

    # validate file size
    # error handling for files that are too large
    if file.stat().st_size > MAX_FILE_SIZE:
        raise ValueError("File is too large (must be under 2MB).")

    # establish file name and path
    safe_name = f"userfile_{uuid.uuid4()}{file.suffix.lower()}"
    dest_path = UPLOAD_DIR / safe_name

    # copy the file without overwriting files that already exist
    shutil.copy2(file, dest_path)
    return dest_path

# main 
# Secure Note Storage
def main():
    print("---Secure Note Storage Program---")
    
    # prompt user to enter a note
    try:
        note = input("Enter your note: ")
        
        # sanitize note to make it safe
        safe_note = sanitize_note(note)
        note_path = save_note(safe_note)

        # asks user to upload file (optional)
        upload_choice = input("Would you like to upload a file? (y/n): ").lower().strip()

        # if/else statements for note uploads
        # IF user wants to upload a note
        if upload_choice == 'y':
            file_path = input("Enter full file path: ").strip()
            stored_path = validate_and_store_file(file_path)
            print(f"File has been safely stored as: {stored_path}")
            
        # ELSE (user does not want to upload a note)
        else:
            print("No file uploaded.")

        print(f"Note has been safely stored as: {note_path}")

        # display the stored note
        print("\n---Your Stored Note---")
        print(safe_note)

    # exception for validation errors
    except ValueError as e:
    
        # error message for user
        print(f"\n Error: {e}")

        # log for technical errors
        # keeps track of errors for troubleshooting
        logging.exception(e)

    # exception for missing files
    except FileNotFoundError as e:
        print(f"\n Error: {e}")
        logging.exception(e)

    # exception for operating system errors
    except OSError as e:
        print(f"\n Error: {e}")
        logging.exception(e)

    # exception for unexpected errors
    except Exception as e:
        print(f"\n Error: {e}")
        logging.exception(e)

    # message to let the user know that the program has finished running
    print("\nProgram finished safely.")

# lets program run
if __name__ == "__main__":
    main()