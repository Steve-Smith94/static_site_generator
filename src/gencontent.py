import os
from markdown_renderer import markdown_to_html_node




def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        s = line.lstrip()
        if s.startswith("# ") and not s.startswith("##"):
            return s[1:].strip()
    raise Exception("No h1 title found")



def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
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
    page = (
        page
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    # 7) ensure dest dir exists and write file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        rel_path = os.path.relpath(root, dir_path_content)

        # Normalize "." to "" so we don’t get "public/./..."
        if rel_path == ".":
            dest_root = dest_dir_path
        else:
            dest_root = os.path.join(dest_dir_path, rel_path)

        os.makedirs(dest_root, exist_ok=True)

        for file in files:
            if file.startswith(".") or not file.endswith(".md"):
                continue

            from_path = os.path.join(root, file)
            dest_file_name = os.path.splitext(file)[0] + ".html"
            dest_path = os.path.join(dest_root, dest_file_name)

            generate_page(from_path, template_path, dest_path, basepath)