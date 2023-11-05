#!/usr/bin/env python
import jsonParser
import htmlParser

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

# dn          =   ["", "dn",              "https://www.dn.no/"]
# url_array.append(dn)
nrk         =   ["", "nrk",             "https://www.nrk.no/"]
e24         =   ["", "e24",             "https://www.e24.no/"]
euronext    =   ["", "euronext",        "https://live.euronext.com/en/markets/oslo"]
finansavisen =  ["", "finansavisen",    "https://www.finansavisen.no"]
investor =      ["", "investor",        "https://www.dn.no/investor/"]
aftenposten =   ["", "aftenposten",     "https://www.aftenposten.no/okonomi"]

url_array.append(nrk)
url_array.append(e24)
url_array.append(euronext)
url_array.append(finansavisen)
url_array.append(investor)
url_array.append(aftenposten)

# url_array.append(aftenposten)
# url_array.append(investor)


# def main():
#     # while True:
#         createContentFiles(url_array)
#         # time.sleep(300)
#         # jsonParser.webPages()
#         htmlParser.updateDatabase()

def main():
    createContentFiles(url_array)
    # time.sleep(300)
    # jsonParser.webPages()
    htmlParser.updateDatabase()

if __name__ == "__main__":
    main()


