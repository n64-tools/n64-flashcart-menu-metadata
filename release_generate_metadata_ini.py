import os
import shutil

source_root = os.path.join(os.path.dirname(__file__), 'metadata')
dest_root = os.path.join(os.path.dirname(__file__), 'release', 'metadata')

for dirpath, dirnames, filenames in os.walk(source_root):
    if 'metadata.ini' in filenames:
        rel_dir = os.path.relpath(dirpath, source_root)
        dir_parts = [p for p in rel_dir.replace('\\', '/').split('/') if p]
        dest_dir = os.path.join(dest_root, rel_dir)
        os.makedirs(dest_dir, exist_ok=True)
        src_file = os.path.join(dirpath, 'metadata.ini')
        dst_file = os.path.join(dest_dir, 'metadata.ini')
        shutil.copy2(src_file, dst_file)
