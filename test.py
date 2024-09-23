#!/usr/bin/env python
import subprocess

# subprocess.run(["make"])


def download_web_pages(name, url):
    filename = name + ".html"
    path = "htmlFiles/"
    path += filename
    print(f"\n downloading {url} to {path}")
    subprocess.run(["curl", "-L", "-o", path, url])

download_web_pages("e24aksjer", "https://e24.no/bors")
