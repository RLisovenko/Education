"""
File: folder_contents.py
Performed by: R. Lisovenko
Date: 07-10-2026

Description:
Displays the contents of a project directory and its subdirectories.
"""

from pathlib import Path


def print_folder_contents(folder_path="data"):
    folder = Path(folder_path)

    print("\n" + "=" * 60)
    print(f"FOLDER CONTENTS: {folder}")
    print("=" * 60)

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    for item in sorted(folder.rglob("*")):
        if item.is_file():
            print(item)

    print("=" * 60)


if __name__ == "__main__":
    print_folder_contents()