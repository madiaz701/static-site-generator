import shutil
import os
from textnode import TextNode, TextType


def main():
    dummy_node = TextNode('Dummy text', TextType.LINK, 'https://www.boot.dev')
    print(dummy_node)
    copy_static_files_to_public()


def copy_static_files_to_public():

    # Create public directory if it doesn't exist, otherwise delete all files in public before copying
    if not os.path.exists('public'):
        # Create the public directory and log that it was created
        os.makedirs('public')
        print(f"Created directory: {os.path.join('public')}")
    else:
        # Delete all files in public and subdirectories before copying and log all deleted files
        for root, dirs, files in os.walk('public'):
            for filename in files:
                file_path = os.path.join(root, filename)
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")

    # Copy all files from static and subdirectories to public and log all copied files
    for root, dirs, files in os.walk('static'):
        for filename in files:
            src_path = os.path.join(root, filename)
            dst_path = os.path.join('public', os.path.relpath(src_path, 'static'))
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {dst_path}")

if __name__ == "__main__":
    main()