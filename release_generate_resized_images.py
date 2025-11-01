# ---------------------------------------------------------------------------------
# Game Art Automation Script
# Version: 0.1.0
#
# Description:
# This script automatically prepares box art for N64 flashcart menus that use
# a Game Code-based directory structure.
#
# Prerequisites:
# - Python 3 (https://www.python.org/downloads/)
# - Pillow library (run 'pip install Pillow' in your terminal/cmd)
# ---------------------------------------------------------------------------------
import os
import sys
import time
import traceback
import shutil
from PIL import Image

# Suggested sizes (multiple allowed per type)
SIZES = {
    "boxart_front.png": [(158, 112), (112, 158), (129, 112)],  # US/EU, JP, 64DD
    "boxart_back.png": [(158, 112), (112, 158), (129, 112)],
    "boxart_top.png": [(158, 22)],
    "boxart_bottom.png": [(158, 22)],
    "boxart_left.png": [(112, 22)],
    "boxart_right.png": [(112, 22)],
    "gamepak_front.png": [(158, 112)],
    "gamepak_back.png": [(158, 112)],
    # Add more if needed
}

def resize_image(path, valid_sizes, out_path):
    with Image.open(path) as img:
        img = img.convert("RGBA")
        # Find the first valid size that the image is at least as large as
        target_size = None
        for size in valid_sizes:
            if img.width >= size[0] and img.height >= size[1]:
                target_size = size
                break
        if not target_size:
            raise ValueError(
                f"Image '{path}' is too small ({img.width}x{img.height}) for any valid target size: {valid_sizes}"
            )
        # Preserve aspect ratio, fit image inside target_size, center on transparent canvas
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        if img_ratio > target_ratio:
            # Image is wider than target: fit width
            new_width = target_size[0]
            new_height = round(target_size[0] / img_ratio)
        else:
            # Image is taller than target: fit height
            new_height = target_size[1]
            new_width = round(target_size[1] * img_ratio)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        # Create transparent canvas and paste centered
        canvas = Image.new("RGBA", target_size, (0, 0, 0, 0))
        x = (target_size[0] - new_width) // 2
        y = (target_size[1] - new_height) // 2
        canvas.paste(resized_img, (x, y))
        canvas.save(out_path)

def _print_progress_bar(idx, total, width=40, msg=""):
    if total <= 0:
        return
    pct = idx / total
    filled = int(width * pct)
    bar = "[" + "#" * filled + "-" * (width - filled) + "]"
    percent_text = f"{int(pct*100):3d}%"
    sys.stdout.write(f"\r{bar} {idx}/{total} {percent_text} {msg}")
    sys.stdout.flush()

def clean_output_dir(output_dir):
    """Remove all contents of output_dir and recreate it empty."""
    if not output_dir:
        return
    if os.path.exists(output_dir):
        try:
            shutil.rmtree(output_dir)
        except Exception:
            # best-effort fallback if rmtree fails
            for root, dirs, files in os.walk(output_dir, topdown=False):
                for name in files:
                    try:
                        os.unlink(os.path.join(root, name))
                    except Exception:
                        pass
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception:
                        pass
    os.makedirs(output_dir, exist_ok=True)

def process_metadata(metadata_dir, output_dir):
    # detect debug mode and whether stdout is a TTY
    DEBUG = os.getenv("DEBUG", "0") == "1" or ("--debug" in sys.argv)
    TTY = sys.stdout.isatty()
    use_progress_bar = (not DEBUG) and TTY

    # By default, clean output unless --no-clean or NO_CLEAN=1 is set
    no_clean_env = os.getenv("NO_CLEAN", "0") == "1"
    no_clean_cli = "--no-clean" in sys.argv
    clean_output = not (no_clean_env or no_clean_cli)

    # Clean the output folder before processing if requested
    if clean_output:
        clean_output_dir(output_dir)

    # Gather all matching files first so we can report a total
    images = []
    for root, dirs, files in os.walk(metadata_dir):
        for file in files:
            if file in SIZES:
                images.append((root, file))

    total = len(images)
    if not use_progress_bar:
        print(f"Found {total} image(s) to process.", flush=True)
    else:
        # still print a short header so user knows what's happening
        print(f"Found {total} image(s) to process. Starting...", flush=True)

    succeeded = 0
    failed = 0
    skipped = 0
    start_time = time.time()

    for idx, (root, file) in enumerate(images, start=1):
        in_path = os.path.join(root, file)
        # preserve relative path inside metadata_dir
        rel_path = os.path.relpath(root, metadata_dir)
        out_folder = os.path.join(output_dir, rel_path) if rel_path != "." else output_dir
        os.makedirs(out_folder, exist_ok=True)
        out_path = os.path.join(out_folder, file)

        short_msg = os.path.basename(root) + "/" + file
        if use_progress_bar:
            _print_progress_bar(idx - 1, total, msg=f"Processing {short_msg[:40]}")

        try:
            resize_image(in_path, SIZES[file], out_path)
            succeeded += 1
            if use_progress_bar:
                _print_progress_bar(idx, total, msg=f"Saved {file}")
            else:
                print(f"[{idx}/{total}] Processing: {in_path} -> {out_path}", flush=True)
                print(f"[{idx}/{total}] Saved: {out_path}", flush=True)
        except ValueError as ve:
            skipped += 1
            if use_progress_bar:
                sys.stdout.write("\n")
                sys.stdout.flush()
                print(f"[{idx}/{total}] SKIPPED {in_path}: {ve}", flush=True)
            else:
                print(f"[{idx}/{total}] SKIPPED {in_path}: {ve}", flush=True)
        except Exception:
            failed += 1
            if use_progress_bar:
                # break the progress bar line before printing the traceback
                sys.stdout.write("\n")
                sys.stdout.flush()
                print(f"[{idx}/{total}] ERROR processing {in_path}:", flush=True)
                traceback.print_exc()
            else:
                print(f"[{idx}/{total}] ERROR processing {in_path}:", flush=True)
                traceback.print_exc()

    elapsed = time.time() - start_time
    if use_progress_bar:
        # ensure final bar shows 100% and move to next line
        _print_progress_bar(total, total, msg="Done")
        sys.stdout.write("\n")
        sys.stdout.flush()

    print(f"Done. Processed: {total}, Succeeded: {succeeded}, Failed: {failed}, Skipped (too small): {skipped}, Elapsed: {elapsed:.2f}s", flush=True)

if __name__ == "__main__":
    metadata_dir = "metadata"
    output_dir = "release"
    # example usage:
    #   python script.py --clean
    # or set env CLEAN_OUTPUT=1
    process_metadata(metadata_dir, output_dir)
