#!/usr/bin/env python
import json

def webPages():
    json_file_path = 'webPages.json'  
    with open(json_file_path, 'r') as json_file:
        web_pages = json.load(json_file)

    webPage_array = []
    for page in web_pages:
        pageData = [page["name"], page["url"]]
        webPage_array.append(pageData)
    return webPage_array

def htmlTags():
    json_file_path = 'htmlTags.json'  
    with open(json_file_path, 'r') as json_file:
        htmlTags = json.load(json_file)

    tag_array = []

    for tag in htmlTags:
        tag_array.append(tag)
    return tag_array
    

def searchWords():
    json_file_path = 'searchWords.json'  
    with open(json_file_path, 'r') as json_file:
        word_list = json.load(json_file)

    word_array = []

    for word in word_list:
        word_array.append(word)
    return word_array
