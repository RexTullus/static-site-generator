import os
from pathlib import Path

from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2: ]
    raise ValueError("No title found")    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path)
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, file)
        if os.path.isfile(full_path):
            if Path(full_path).suffix == ".md":
                dest_path = os.path.join(dest_dir_path, file)
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(full_path, template_path, dest_path)
        else:
            new_dest_dir = os.path.join(dest_dir_path, file)
            generate_pages_recursive(full_path, template_path, new_dest_dir)


