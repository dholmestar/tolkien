import os
import shutil

from src.copystatic import copy_files_recursive #type: ignore
from src.gencontent import generate_pages_recursive #type: ignore

def main():
    print("Beginning static site generation...")

    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"

    print(f"Deleting contents of {dir_path_public} if it exists...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    print(f"Creating new directory: {dir_path_public}...")
    os.mkdir(dir_path_public)
    print(f"Successfully prepared {dir_path_public}.")

    print(f"Copying static files from {dir_path_static} to {dir_path_public}...")
    copy_files_recursive(dir_path_static, dir_path_public)
    print("Static files copied successfully!")

    print("Generating pages recursively...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

    print("Static site generation complete.")

if __name__ == "__main__":
    main()