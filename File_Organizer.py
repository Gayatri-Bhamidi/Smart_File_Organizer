import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from datetime import datetime


# ---------- FILE ORGANIZER LOGIC ----------
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Programs": [".exe", ".msi"],
    "Archives": [".zip", ".rar"]
}


def organize_files(folder_path, progress, status):
    files = [f for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))]

    total_files = len(files)
    if total_files == 0:
        messagebox.showinfo("Info", "No files to organize.")
        return

    log_file = os.path.join(folder_path, "organizer_log.txt")

    with open(log_file, "a") as log:
        log.write(f"\n--- Organizing started at {datetime.now()} ---\n")

        for index, file in enumerate(files, start=1):
            file_path = os.path.join(folder_path, file)
            moved = False

            for folder, extensions in FILE_TYPES.items():
                if file.lower().endswith(tuple(extensions)):
                    dest_folder = os.path.join(folder_path, folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, dest_folder)

                    log.write(f"{file} → {folder}\n")
                    moved = True
                    break

            if not moved:
                other = os.path.join(folder_path, "Others")
                os.makedirs(other, exist_ok=True)
                shutil.move(file_path, other)
                log.write(f"{file} → Others\n")

            # Update UI
            progress["value"] = (index / total_files) * 100
            status.config(text=f"Organizing: {file}")
            root.update_idletasks()

        log.write("--- Organizing completed ---\n")

    status.config(text="Completed!")
    messagebox.showinfo("Success", "Files organized successfully!")


# ---------- GUI FUNCTION ----------
def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        progress["value"] = 0
        status.config(text="Starting...")
        organize_files(folder, progress, status)


# ---------- GUI WINDOW ----------
root = tk.Tk()
root.title("Smart File Organizer")
root.geometry("450x260")
root.resizable(False, False)

title = tk.Label(root, text="Smart File Organizer", font=("Arial", 16, "bold"))
title.pack(pady=10)

info = tk.Label(
    root,
    text="Select a folder (Downloads/Desktop)\nFiles will be organized automatically",
    font=("Arial", 10)
)
info.pack(pady=5)

btn = tk.Button(
    root,
    text="Choose Folder",
    font=("Arial", 11),
    width=20,
    command=select_folder
)
btn.pack(pady=10)

progress = ttk.Progressbar(root, length=350, mode="determinate")
progress.pack(pady=10)

status = tk.Label(root, text="Waiting...", font=("Arial", 9))
status.pack()

footer = tk.Label(root, text="Python Desktop Utility", font=("Arial", 9))
footer.pack(side="bottom", pady=5)

root.mainloop()
