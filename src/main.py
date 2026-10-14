import os
import shutil

from textnode import TextNode

def main():
    from_static_to_public()
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)

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
    source = "static"
    destination = "public"

    # Delete public if it already exists
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Create a fresh public directory
    os.mkdir(destination)

    # Copy everything from static to public
    copy_directory(source, destination)


main()