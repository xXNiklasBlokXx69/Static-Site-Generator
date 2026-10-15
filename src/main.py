import os
import shutil
import sys

from textnode import TextNode
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    from_static_to_public()
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

def copy_directory(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            os.mkdir(destination_path)

            copy_directory(source_path, destination_path)

def from_static_to_public():
    source = dir_path_static
    destination = dir_path_public

    # Delete public if it already exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Create a fresh public directory
    os.mkdir(destination)

    # Copy everything from static to public
    copy_directory(source, destination)


main()