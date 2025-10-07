from gencontent import generate_page 
from markdown_renderer import markdown_to_html_node
import os
import shutil




def copy_static_to_public(src: str, dest: str):
    """
    Recursively copies all contents from src to dest.
    Deletes the destination directory first.
    Logs each file copied (source -> destination).
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' does not exist")

    # Delete destination directory if it exists
    if os.path.exists(dest):
        print(f"Deleting existing directory: {dest}")
        shutil.rmtree(dest)

    os.makedirs(dest, exist_ok=True)
    print(f"Created directory: {dest}")

    # Start the recursive copy
    _recursive_copy(src, dest)
    


def _recursive_copy(current_src: str, current_dest: str):
    """
    Recursively copies contents from current_src to current_dest.
    This is a standalone recursive function.
    """
    for item in os.listdir(current_src):
        if item.startswith("."):
            continue
        s_item = os.path.join(current_src, item)
        d_item = os.path.join(current_dest, item)

        try:
            if os.path.isdir(s_item):
                os.makedirs(d_item, exist_ok=True)
                print(f"Created directory: {d_item}")
                _recursive_copy(s_item, d_item)
            elif os.path.isfile(s_item) or os.path.islink(s_item):
                shutil.copy2(s_item, d_item)
                print(f"Copied: {s_item} -> {d_item}")
            else:
                print(f"Skipping unknown item type: {s_item}")
        except PermissionError:
            print(f"Permission denied: {s_item}")



def main():
    copy_static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    print("Static site regenerated successfully!")


if __name__ == "__main__":
    main()
