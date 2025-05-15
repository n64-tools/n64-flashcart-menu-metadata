import os
import shutil

source_root = os.path.join(os.path.dirname(__file__), 'metadata')
dest_root = os.path.join(os.path.dirname(__file__), 'release', 'metadata')

for dirpath, dirnames, filenames in os.walk(source_root):
    if 'description.txt' in filenames:
        rel_dir = os.path.relpath(dirpath, source_root)
        dir_parts = [p for p in rel_dir.replace('\\', '/').split('/') if p]
        # If the last folder is media type 'E', move up one directory
        if dir_parts and dir_parts[-1] == 'E':
            dest_dir = os.path.join(dest_root, *dir_parts[:-1])
        else:
            dest_dir = os.path.join(dest_root, rel_dir)
        os.makedirs(dest_dir, exist_ok=True)
        src_file = os.path.join(dirpath, 'description.txt')
        dst_file = os.path.join(dest_dir, 'description.txt')
        shutil.copy2(src_file, dst_file)
