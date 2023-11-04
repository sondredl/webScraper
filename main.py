#!/usr/bin/env python

import subprocess
import time

url_array = []

def createFileToParse(page, url, i):
    filename = page + ".html"
    path = "htmlFiles/" 
    path += filename
    subprocess.run(["curl", "-o", path, url])

def createContentFiles(listOfUrls):
    subprocess.run(["mkdir", "htmlFiles"])
    iterator = 1
    for i in listOfUrls:
        createFileToParse(i[1], i[2], iterator)
        iterator += 1

dn  = ["", "dn",    "https://www.dn.no/"]
nrk = ["", "nrk",   "https://www.nrk.no/"]
e24 = ["", "e24",   "https://www.e24.no/"]
euronext = ["", "euronext",   "https://live.euronext.com/en/markets/oslo"]
url_array.append(dn)
url_array.append(nrk)
# url_array.append(e24)
url_array.append(euronext)


def main():
    # while True:
        createContentFiles(url_array)
        # time.sleep(300)

if __name__ == "__main__":
    main()