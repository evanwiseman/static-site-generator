import os

from convert import markdown_to_html_node
from extract import extract_markdown_title
from htmlnode import HTMLNode

def generate_page(source, template_path, destination, basepath):
    print(f"Generating page from {source} to {destination} using {template_path}")
    markdown = ""
    with open(source) as file:
        markdown = file.read()
    
    template = ""
    with open(template_path) as file:
        template = file.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_markdown_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")

    os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
    with open(destination, "w") as file:
        file.write(template)

def generate_pages_recursive(source:str, template_path:str, destination:str, basepath:str):
    if not os.path.exists(source):
        raise FileNotFoundError("Error: generate_pages_recursive source not found")
    if not os.path.isdir(source):
        raise IsADirectoryError("Error: generate_pages_recursive invalid source directory")
    if not os.path.exists(template_path):
        raise FileNotFoundError("Error: generate_pages_recursive template_path not found")
    
    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        if os.path.isfile(source_item) or os.path.islink(source_item):
            destination_item = os.path.splitext(os.path.join(destination, item))[0] + ".html"
            generate_page(source_item, template_path, destination_item, basepath)
        elif os.path.isdir(source_item):
            destination_item = os.path.join(destination, item)
            generate_pages_recursive(source_item, template_path, destination_item, basepath)
        
            