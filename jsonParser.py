#!/usr/bin/env python
import json

def webPages():
    json_file_path = 'webPages.json'  
    with open(json_file_path, 'r') as json_file:
        web_pages = json.load(json_file)

    for page in web_pages:
        print(page)

def htmlTags():
    json_file_path = 'htmlTags.json'  
    with open(json_file_path, 'r') as json_file:
        htmlTags = json.load(json_file)

    for tag in htmlTags:
        # print(tag)
        return tag

def searchWords():
    json_file_path = 'searchWords.json'  
    with open(json_file_path, 'r') as json_file:
        word_list = json.load(json_file)

    word_array = []
    for word in word_list:
        # print(word)
        word_array.append(word)
        # return word
    return word_array

# webPages()
# htmlTags()
# searchWords()