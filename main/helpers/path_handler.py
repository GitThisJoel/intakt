import sys, os
from pathlib import Path


def root_dir() -> Path:
    return Path(__file__).parent.parent.parent.resolve()


def main_dir() -> Path:
    return root_dir() / "main"


def assets_dir() -> Path:
    return main_dir() / "assets"


def credentials_dir() -> Path:
    return main_dir() / "credentials"


def tex_dir() -> Path:
    return main_dir() / "tex_compiler"


if __name__ == "__main__":
    print("All available dirs are:")
    all_funcs = {
        "root": root_dir,
        "main": main_dir,
        "assets": assets_dir,
        "credentials": credentials_dir,
        "tex": tex_dir,
    }

    for name, func in all_funcs.items():
        print(f"{name}:".ljust(15), func())
