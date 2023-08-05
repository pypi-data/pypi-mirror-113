import os 

def create_dir(dirpath):
    os.mkdir(dirpath)

def check_dir(dirpath):
    return os.path.isdir(dirpath)

def check_file(filepath):
    return os.path.isfile(filepath)
