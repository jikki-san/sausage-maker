import os
import shutil


def dir_copy(src, dst):
    print(f"Copying {src} -> {dst}")
    # base case: current object is a file, copy it and return
    if os.path.isfile(src):
        shutil.copy(src, dst)
        return
    # if the destination directory exists
    # empty destination directory
    if os.path.exists(dst):
        shutil.rmtree(dst)
    # create the directory
    os.mkdir(dst)
    # recursively copy children
    for path in os.listdir(src):
        dir_copy(os.path.join(src, path), os.path.join(dst, path))
