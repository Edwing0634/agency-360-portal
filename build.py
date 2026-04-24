"""PyInstaller build script — generates a single .exe for Windows deployment."""

import subprocess
import sys
import os

APP_NAME = "Agency360Portal"
ICON_PATH = "static/img/icon.ico"


def build() -> None:
    args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", APP_NAME,
        "--add-data", "templates;templates",
        "--add-data", "static;static",
        "--hidden-import", "webview",
        "--hidden-import", "pyodbc",
    ]
    if os.path.exists(ICON_PATH):
        args += ["--icon", ICON_PATH]
    args.append("app.py")
    subprocess.run(args, check=True)
    print(f"\nBuild complete: dist/{APP_NAME}.exe")


if __name__ == "__main__":
    build()
