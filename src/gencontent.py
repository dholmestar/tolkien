from src.markdown_blocks import markdown_to_html_node #type: ignore
from pathlib import Path
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# ") and not line.startswith("##"):
            title = line[1:].strip()
            return title
    raise Exception("no h1 header found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    file = open(from_path, "r")
    markdown_contents = file.read()
    file.close()

    file = open(template_path, "r")
    template_contents = file.read()
    file.close()

    node = markdown_to_html_node(markdown_contents)
    html = node.to_html()

    title = extract_title(markdown_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    template_contents = template_contents.replace('href="/', f'href="{basepath}')
    template_contents = template_contents.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    
    file = open(dest_path, "w")
    file.write(template_contents)
    file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            _, ext = os.path.splitext(from_path)
            if ext == ".md":
                new_dest_path = Path(dest_path).with_suffix(".html")
                generate_page(from_path, template_path, new_dest_path, basepath)
                
        elif os.path.isdir(from_path):
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(from_path, template_path, dest_path, basepath)