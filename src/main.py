import shutil
import os
import sys
from generator import generate_pages_recursively
from textnode import TextNode, TextType


def main():
    dummy_node = TextNode('Dummy text', TextType.LINK, 'https://www.boot.dev')
    print(dummy_node)
    
    basepath = sys.argv[1]
    # If no basepath, default to "/"
    if not basepath:
        basepath = "/"

    # Log the basepath being used
    print(f"Using basepath: {basepath}")
    copy_static_files_to_docs()
    generate_pages_recursively('content', 'template.html', 'docs', basepath)


def copy_static_files_to_docs():

    # Create docs directory if it doesn't exist, otherwise delete all files in docs before copying
    if not os.path.exists('docs'):
        # Create the docs directory and log that it was created
        os.makedirs('docs')
        print(f"Created directory: {os.path.join('docs')}")
    else:
        # Delete all files in docs and subdirectories before copying and log all deleted files
        for root, dirs, files in os.walk('docs'):
            for filename in files:
                file_path = os.path.join(root, filename)
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")

    # Copy all files from static and subdirectories to docs and log all copied files
    for root, dirs, files in os.walk('static'):
        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join('docs', os.path.relpath(src_path, 'static'))
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {dst_path}")

if __name__ == "__main__":
    main()