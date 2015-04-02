# helper functions for fabric script
import time
import os
import yaml

def create_dir(name, parent = "."):
    if not name:
        name = str(int(time.time()))
    dir_path = os.path.join(parent, name)
    if os.path.exists(dir_path):
        return None, "Snapshot exists"
    else:
        os.makedirs(dir_path)
        return name, None

def parse_config(file_name):
    with open(file_name) as f:
        return yaml.safe_load(f)

def set_symlink(link, target, parent_dir = "."):
    link_path = os.path.join(parent_dir, link)
    if os.path.exists(link_path):
        os.unlink(link_path)
    os.symlink(target, link_path)

def list_dirs(parent):
    return filter(os.path.isdir, [os.path.join(parent, d) for d in os.listdir(parent)])
