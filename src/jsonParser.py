#!/usr/bin/env python
import json


class JsonParser:
    def webPages(self):
        json_file_path = "inputData/webPages.json"
        with open(json_file_path, "r") as json_file:
            web_pages = json.load(json_file)

        webPage_array = []
        for page in web_pages:
            pageData = [page["name"], page["url"]]
            webPage_array.append(pageData)
        return webPage_array


    def htmlTags(self):
        json_file_path = "inputData/htmlTags.json"
        with open(json_file_path, "r") as json_file:
            htmlTags = json.load(json_file)

        tag_array = []

        for tag in htmlTags:
            tag_array.append(tag)
        return tag_array


    def searchWords(self):
        json_file_path = "inputData/searchWords.json"
        with open(json_file_path, "r") as json_file:
            word_list = json.load(json_file)

        word_array = []

        for word in word_list:
            word_array.append(word)
        return word_array


    def companyNames(self):
        json_file_path = "inputData/companies.json"
        with open(json_file_path, "r") as json_file:
            word_list = json.load(json_file)

        word_array = []

        for word in word_list:
            word_array.append(word)
        return word_array
