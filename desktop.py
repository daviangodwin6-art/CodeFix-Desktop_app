"""CodeFix desktop app: the local server (server.py) in a background thread, the page in a native window.
Closing the window ends the program. Run: python desktop.py   (Windows build: codefix.spec + installer.iss, see README)"""
import html
import shutil
import socket
import sys
import threading
import time
import urllib.request

import webview

from agent import paths

HOST, PORT = "127.0.0.1", 8000
# The window opens localhost, not 127.0.0.1: GitHub sign-in (Firebase) rejects 127.0.0.1. The server still binds
# 127.0.0.1 only, and its Host/Origin check (server.refuse_other_sites) accepts both names.
URL = f"http://localhost:{PORT}"


def log_to_file():
    """The windowed build has no console (sys.stdout is None), and uvicorn's logging fails without one."""
    if sys.stdout is None or sys.stderr is None:
        paths.data_dir().mkdir(parents=True, exist_ok=True)
        sys.stdout = sys.stderr = open(paths.data_dir() / "codefix.log", "a", encoding="utf-8", buffering=1)


def port_taken():
    with socket.socket() as s:
        return s.connect_ex((HOST, PORT)) == 0


def startup_problem():
    if not shutil.which("git"):
        return ("Git was not found.",
                "CodeFix needs Git to make working copies of your repositories. Install it from "
                "https://git-scm.com/download/win (keep the default \"Git from the command line\" option), "
                "then start CodeFix again.")
    if port_taken():
        return ("Port 8000 is already in use.",
                "CodeFix may already be running: look for its window. Otherwise close the program "
                "that uses port 8000 (another CodeFix server?) and start CodeFix again.")
    return None


def wait_until_up(timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(f"http://{HOST}:{PORT}/api/me", timeout=2):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def show_message(title, text):
    page = (f"<body style='font:15px Segoe UI,sans-serif;padding:24px;line-height:1.5'>"
            f"<h2>{html.escape(title)}</h2><p>{html.escape(text)}</p></body>")
    webview.create_window("CodeFix", html=page, width=560, height=300)
    webview.start()


def main():
    log_to_file()
    problem = startup_problem()
    if problem:
        return show_message(*problem)

    import uvicorn

    import server

    threading.Thread(target=uvicorn.run, args=(server.app,), kwargs={"host": HOST, "port": PORT}, daemon=True).start()
    if not wait_until_up():
        log = paths.data_dir() / "codefix.log" if paths.FROZEN else "the console"
        return show_message("CodeFix could not start.", f"The local server did not answer. Details are in {log}.")
    webview.create_window("CodeFix", URL, width=1280, height=860, min_size=(900, 600))
    webview.start()  # returns when the window closes; the server thread is a daemon and dies with the process


if __name__ == "__main__":
    main()
