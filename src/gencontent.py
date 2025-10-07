import os
from markdown_renderer import markdown_to_html_node




def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        s = line.lstrip()
        if s.startswith("# ") and not s.startswith("##"):
            return s[1:].strip()
    raise Exception("No h1 title found")



def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    # 1) print status message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # 2) read markdown
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # 3) read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 4) convert markdown to html string
    html = markdown_to_html_node(markdown).to_html()

    # 5) extract title
    title = extract_title(markdown)

    # 6) substitute placeholders
    page = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html)
    )

    # 7) ensure dest dir exists and write file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)