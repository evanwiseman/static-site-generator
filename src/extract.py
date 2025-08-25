import re

from typing import List

def extract_markdown_images(text) -> List[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text) -> List[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_title(text):
    pattern = r"^\s*#\s+(.*)$"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise Exception("Error: extract_markdown_title invalid h1")
    return match.group(1).strip()
    
    