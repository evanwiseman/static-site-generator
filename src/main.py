import os
import shutil
import sys

from generate import generate_pages_recursive

def remove_contents(path):
    # Everything is already removed
    if not os.path.exists(path):
        return
    
    # Remove contents inside destination
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_contents(source, destination):
    # Ensure both paths exist
    if not os.path.exists(source):
        os.mkdir(source)
    if not os.path.exists(destination):
        os.mkdir(destination)
    
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path) or os.path.islink(source_path):
            shutil.copy(source_path, destination)
        elif os.path.isdir(source_path):
            copy_contents(source_path, destination_path)
        
def main(args):
    basepath = "/"
    if len(args) > 1:
        basepath = args[1]
    
    remove_contents("public")
    copy_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public", basepath)


if __name__ == "__main__":
    main(sys.argv)
