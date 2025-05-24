import os
import shutil


def dir_copy(src, dst):
    print(f"Copying {src} -> {dst}")
    if os.path.isfile(src):
        shutil.copy(src, dst)
        return
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for path in os.listdir(src):
        dir_copy(os.path.join(src, path), os.path.join(dst, path))
