#!/usr/bin/env python3

"""
Panda3D Cache Purge Tool

You have modified some assets in the library
and then when you relaunch the game you don't
see your changes?

That is because Panda3D stores downloaded or processed assets in
a 'cache' directory to improve performance on subsequent runs.

This tool helps you quickly find and clear the *contents* of that cache directory
for your operating system (Linux, macOS, Windows), leaving the directory itself intact.
"""

import os
import sys
import platform
import shutil  # Module needed for removing directory trees
from pathlib import Path # Modern way to handle paths

def get_panda3d_cache_dir():
    """Detects the OS and returns the expected Panda3D cache directory path."""
    system = platform.system()
    home = Path.home() # Get user's home directory object

    if system == "Linux":
        cache_base = os.environ.get('XDG_CACHE_HOME', home / ".cache")
        cache_path = Path(cache_base) / "panda3d"
        print(f"Detected Linux. Cache expected at: {cache_path}")
        return cache_path
    elif system == "Darwin": # Darwin is macOS
        cache_path = home / "Library/Caches/Panda3D"
        print(f"Detected macOS. Cache expected at: {cache_path}")
        return cache_path
    elif system == "Windows":
        local_appdata = os.environ.get('LOCALAPPDATA')
        if not local_appdata:
            print("Error: Could not determine LOCALAPPDATA environment variable.", file=sys.stderr)
            return None
        cache_path = Path(local_appdata) / "Panda3D"
        print(f"Detected Windows. Cache expected at: {cache_path}")
        return cache_path
    elif system == "Android":
         print("Detected Android. Cache location can vary greatly.")
         print("Assuming Linux-like structure within user home as a fallback.")
         cache_base = home / ".cache"
         cache_path = Path(cache_base) / "panda3d"
         print(f"Guessing cache might be at: {cache_path}")
         return cache_path
    else:
        print(f"Unsupported operating system detected: {system}", file=sys.stderr)
        return None

def clear_directory_contents(directory_path: Path):
    """
    Removes all files and subdirectories within the given directory path.
    Returns True if successful or directory was already empty, False otherwise.
    """
    print(f"\nAttempting to clear contents of {directory_path}...")
    items_deleted = 0
    items_failed = 0

    # Check if directory exists before iterating
    if not directory_path.is_dir():
        print(f"Error: Cannot clear contents, path is not a directory: {directory_path}", file=sys.stderr)
        return False

    # Iterate through items (files and subdirs) directly inside the target path
    for item_path in directory_path.iterdir():
        try:
            if item_path.is_file() or item_path.is_symlink():
                item_path.unlink() # Remove file or symbolic link
                print(f"  Deleted file/link: {item_path.name}")
                items_deleted += 1
            elif item_path.is_dir():
                shutil.rmtree(item_path) # Remove subdirectory and its contents
                print(f"  Deleted directory: {item_path.name}")
                items_deleted += 1
            else:
                # Should not happen often with standard filesystems
                print(f"  Skipping unknown item type: {item_path.name}")

        # Catch errors during deletion of a specific item
        except PermissionError:
            print(f"\n  Error: Permission denied. Could not remove item: {item_path.name}", file=sys.stderr)
            items_failed += 1
        except OSError as e:
            print(f"\n  Error: Could not remove item {item_path.name} due to OS error: {e}", file=sys.stderr)
            items_failed += 1

    if items_failed > 0:
        print(f"\n-> Finished clearing: {items_deleted} items deleted, {items_failed} items failed.")
        return False # Indicate that the clearing was not fully successful
    elif items_deleted > 0:
        print(f"\n-> Successfully cleared {items_deleted} items from the cache directory.")
        return True
    else:
        print("\n-> Cache directory was already empty.")
        return True # Considered successful if it was already empty

def purge():
    """Finds and attempts to clear the contents of the Panda3D cache directory."""

    target_path = get_panda3d_cache_dir()

    if target_path is None:
        sys.exit(1) # Exit if OS is unsupported or path couldn't be determined

    print(f"\nTarget cache directory: {target_path}")

    # 1. Check if the path exists AND is a directory
    if target_path.is_dir():
        print(f"-> Cache directory exists.")

        # Check permissions needed to modify the *contents* of the directory
        # Need Write permission IN the directory to delete items
        # Need Execute permission IN the directory to list items (iterdir)
        is_readable = os.access(target_path, os.R_OK) # Good to have, but not strictly needed for deletion
        is_writable = os.access(target_path, os.W_OK)
        is_executable = os.access(target_path, os.X_OK)

        print(f"  Directory Permissions: Readable={'YES' if is_readable else 'NO'}, "
              f"Writable={'YES' if is_writable else 'NO'}, "
              f"Executable={'YES' if is_executable else 'NO'}")

        if not is_writable or not is_executable:
             print("\nWarning: Script might not have sufficient permissions to list or modify the contents of this directory.")
             proceed = input("Attempt to clear contents anyway? (Y/N): ").lower().strip()
             if proceed != 'y':
                 print("Aborting content clearing.")
                 sys.exit(0)

        # ----------------------------------
        # Confirmation before destructive action
        # ----------------------------------
        print("\n!!! WARNING !!!")
        print(f"This will permanently delete the *contents* of the directory:") # Modified warning
        print(f"  {target_path}")
        print("Files and subdirectories inside it will be removed. This action cannot be undone.")
        print("The directory itself will remain.") # Added clarification

        confirm = input("Are you sure you want to proceed? (Y/N): ").lower().strip()

        if confirm == 'y':
            # Call the function to clear contents
            success = clear_directory_contents(target_path)
            if not success:
                 print("\nWarning: Some items might not have been removed due to errors.", file=sys.stderr)
                 # Decide if you want to exit with error code if clearing wasn't perfect
                 # sys.exit(1)
        else:
            print("-> Content clearing cancelled by user.")

    # Handle cases where the path exists but isn't a directory, or doesn't exist
    elif target_path.exists():
        print(f"-> Path exists but is NOT a directory: {target_path}")
        print("   Cannot clear contents. No action taken.")
    else:
        print(f"-> Cache directory does NOT exist at the expected location.")
        print("   No action needed.")

    print("\nPurge process complete.")

if __name__ == '__main__':
   purge()