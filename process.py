import glob
import os
from shutil import copyfile
import sys

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE = f"{BASE_PATH}/data/source/"
CLEAN = f"{BASE_PATH}/data/clean/"

def process(blink):
    for filename in glob.iglob(f"{blink}/**/*.in", recursive=True):
        copyfile(filename, f"{SOURCE}{filename.split('/')[-1]}")

        with open(filename, "r") as f:
            content = [l.strip() for l in f.readlines() if not l.startswith(("#", "//"))]

        index = next(i for i, s in enumerate(content) if not s) if content[0].startswith("namespace") else 0
        values = filter(None, [value.split(" ")[0] for value in content[index:]])
        
        with open(f"{CLEAN}{filename.split('/')[-1].rstrip('in')}lst", "w") as f:
            f.write("\n".join(values) + "\n")

def _create(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <blink_folder>")

    _create(SOURCE)
    _create(CLEAN)

    process(sys.argv[1].strip("/"))
