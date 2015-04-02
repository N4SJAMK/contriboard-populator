# helper functions for fabric script
import time
import os

def create_dir(name):
    if not name:
        name = str(int(time.time()))
    if os.path.exists(name):
        return None, "Snapshot exists"
    else:
        os.makedirs(name)
        return name, None

def parse_config(file_name):
    with open(file_name) as f:
        return yaml.safe_load(f)

def set_symlink(link, target):
    if os.path.exists(link):
        os.unlink(link)
    os.symlink(link, target)

def list_dirs(parent):
    return filter(os.path.isdir, [os.path.join(parent, d) for d in os.listdir(parent)])
