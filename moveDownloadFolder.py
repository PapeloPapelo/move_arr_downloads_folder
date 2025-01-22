import os
import shutil

# Dictionary to store inode-to-file path mappings
inode_map = {}

def build_inode_map(drive):
    """
    Scan the drive once and build a map of inodes to file paths.
    """
    for root, dirs, files in os.walk(drive):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_stat = os.stat(file_path)
                inode = file_stat.st_ino
                
                # If the inode is not in the map, add it
                if inode not in inode_map:
                    inode_map[inode] = []
                inode_map[inode].append(file_path)
            except FileNotFoundError:
                continue

def get_hardlink_target(file_path, source_location):
    """
    Returns the path to the file associated with multiple hard links,
    ensuring that the returned path is not in the source directory.
    """
    # Get the inode number of the file
    file_stat = os.stat(file_path)
    inode = file_stat.st_ino

    # Check if the inode is in the inode map
    if inode in inode_map:
        # Look for a hard link that is not in the source location
        for path in inode_map[inode]:
            # Exclude the source location path
            if os.path.commonpath([path, source_location]) != source_location:
                return path

    return None

def copy_files_with_symlinks(source_dir, dest_dir):
    """
    Copies files from source_dir to dest_dir with the following logic:
    - If a file has multiple hard links, a symlink is created at the destination
      that points to the correct file (not the hard link in the source folder).
    - Otherwise, the file is copied normally.
    """
    # Walk through the source directory
    for dirpath, dirnames, filenames in os.walk(source_dir):
        # Calculate relative path from the source directory
        rel_path = os.path.relpath(dirpath, source_dir)
        dest_dirpath = os.path.join(dest_dir, rel_path)
        
        # Create the corresponding directory in the destination
        if not os.path.exists(dest_dirpath):
            os.makedirs(dest_dirpath)

        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            dest_file = os.path.join(dest_dirpath, filename)

            try:
                # Check how many hard links exist for the file
                stat_info = os.stat(source_file)
                link_count = stat_info.st_nlink

                if link_count > 1:
                    # The file has multiple hard links, resolve the hard link target
                    hardlink_target = get_hardlink_target(source_file, source_dir)

                    if hardlink_target:
                        # Create a symlink to the correct hard link in the source
                        # The symlink should point to the hardlink_target (on the source drive)
                        os.symlink(hardlink_target, dest_file)
                        print(f"Created symlink: {dest_file} -> {hardlink_target}")
                    else:
                        # If no target is found, copy the file as a fallback
                        shutil.copy2(source_file, dest_file)
                        print(f"Copied file (hard link issue): {source_file} -> {dest_file}")
                else:
                    # Single hard link, copy the file normally
                    shutil.copy2(source_file, dest_file)
                    print(f"Copied file (single hard link): {source_file} -> {dest_file}")

            except Exception as e:
                print(f"Error processing file {source_file}: {e}")

if __name__ == "__main__":
    source_location = input("Enter the source directory: ").strip()
    dest_location = input("Enter the destination directory: ").strip()

    if not os.path.exists(source_location):
        print(f"Source directory does not exist: {source_location}")
    elif not os.path.exists(dest_location):
        print(f"Destination directory does not exist: {dest_location}")
    else:
        # Build the inode map (this is done only once per drive)
        # Ensure the drive is correctly formatted for Windows (e.g., 'D:\\')
        drive, rest_of_path = os.path.splitdrive(source_location)
        drive_root = drive + '\\'  # Correct format for Windows root

        # Build the inode map for the source drive
        build_inode_map(drive_root)

        # Now run the copy process
        copy_files_with_symlinks(source_location, dest_location)
