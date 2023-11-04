#!/usr/bin/env python

import subprocess
import time

url_array = []

def createFileToParse(url, i):
    filename = str(i) + ".html"
    path = "htmlFiles/" 
    path += filename
    subprocess.run(["curl", "-o", path, url])

def createContentFiles(listOfUrls):
    subprocess.run(["mkdir", "htmlFiles"])
    iterator = 1
    for i in listOfUrls:
        createFileToParse(i[2], iterator)
        iterator += 1

nrk = ["", "nrk",   "https://www.nrk.no/"]
dn  = ["", "dn",    "https://www.dn.no/"]
e24 = ["", "e24",   "https://www.e24.no/"]
url_array.append(nrk)
url_array.append(dn)
url_array.append(e24)


def main():
    while True:
        createContentFiles(url_array)
        time.sleep(300)

if __name__ == "__main__":
    main()