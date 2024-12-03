import os
from pathlib import Path


def display_directory_tree(root_path, max_depth=3):
    root_path = Path(root_path)
    prefix = ""
    max_items = 10

    def inner(path, prefix, level):
        if level > max_depth:
            return
        print(f"{prefix}{path.name}/")
        if path.is_dir():
            children = sorted(path.iterdir())
            for child in children[:max_items]:
                inner(child, prefix + "    ", level + 1)
            if len(children) > max_items:
                print(f"{prefix}    ... ({len(children) - max_items} more)")

    inner(root_path, prefix, level=0)
