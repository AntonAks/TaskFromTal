import os


def generate_tree(
    path: str, level: int = 0, exclude_dirs: list["str"] | None = None
) -> str:
    if exclude_dirs is None:
        exclude_dirs = []

    tree = ""
    try:
        if os.path.isdir(path):
            items = sorted(os.listdir(path))
            for item in items:
                item_path = os.path.join(path, item)
                if item in exclude_dirs:
                    continue
                tree += "│   " * level + "├── " + item + "\n"
                tree += generate_tree(item_path, level + 1, exclude_dirs)
    except PermissionError:
        pass
    return tree


def print_project_structure(
    root_dir: str, exclude_dirs: list[str] | None = None
) -> None:
    structure = generate_tree(root_dir, exclude_dirs=exclude_dirs)
    print(f"{root_dir}\n{structure}")


if __name__ == "__main__":
    exclude_dirs = [
        ".venv",
        ".idea",
        ".git",
        "__pycache__",
        ".terraform",
        "lambda_packages",
        ".mypy_cache",
    ]
    print_project_structure(os.getcwd(), exclude_dirs=exclude_dirs)
