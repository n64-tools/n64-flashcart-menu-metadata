# Requires: Pillow (pip install pillow)
import os
from PIL import Image

# Suggested sizes
SIZES = {
    "boxart_front.png": (158, 112),
    "boxart_back.png": (158, 112),
    "boxart_top.png": (158, 22),
    "gamepak_front.png": (158, 112),
    # Add more if needed
}

def resize_image(path, size, out_path):
    with Image.open(path) as img:
        img = img.convert("RGBA")
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(out_path)

def process_metadata(metadata_dir, output_dir):
    for root, dirs, files in os.walk(metadata_dir):
        for file in files:
            if file in SIZES:
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, ".")  # keep "metadata" in path
                out_folder = os.path.join(output_dir, rel_path)
                os.makedirs(out_folder, exist_ok=True)
                out_path = os.path.join(out_folder, file)
                resize_image(in_path, SIZES[file], out_path)

if __name__ == "__main__":
    metadata_dir = "metadata"
    output_dir = "release"
    process_metadata(metadata_dir, output_dir)
