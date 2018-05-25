# ===========================================================================
# FILE:         Index.py
#
# AUTHOR:       Anyi Chen; Yuqi Ma
#
# DESCRIPTION:  This file deals with multiple parsing and retrieving problems
#
# ===========================================================================

from collections import defaultdict
from bs4 import BeautifulSoup
import json
import re
import math
from nltk.tokenize import word_tokenize


class Index:

    def __init__(self, j_file):
        self.json = defaultdict(str)
        self.j_file = j_file
        self.idf = defaultdict(float)
        self.total = 0
        self.token = defaultdict(lambda: defaultdict(float))

    def parse_json(self):
        """
        This method reads a json file, and parse the file into a dictionary
        :return: modify the self.json in the init
        """
        collection = open(self.j_file)
        self.json = json.load(collection)
        self.total = len(self.json)
        collection.close()

    def cal_tf(self):
        """
        This method will calculate tf-idf for each doc
        :return: modify tf-idf for a particular word in particular file
        """
        for word, docs in self.token.items():
            count = float(len(docs))
            for doc_id, num in docs.items():
                tf = 1 + math.log10(num)
                idf = math.log10(self.total / count)
                self.idf[word] = idf
                self.token[word][doc_id] = tf * idf

    def parse_html(self, html_doc, doc_id):
        """
        This method parse the html string;
            for title, we add texts 10 times more,
            for bold, we add texts 3 times more,
            for header, we add texts 5 times more.
        :param html_doc: the html going to be parsed
        :param doc_id: the document id
        :return: updates information
        """
        print("Start Parsing...")
        soup = BeautifulSoup(html_doc, 'html.parser')
        text = list()
        text.extend(soup.find_all("a"))
        text.extend(soup.find_all("p"))
        for _ in range(3):
            text.extend(soup.find_all("b"))
        for _ in range(10):
            text.extend(soup.find_all("title"))
        for _ in range(5):
            text.extend(soup.find_all(re.compile(r'h\d+')))
        for item in text:
            context = item.string
            if context is not None and context != "" and not is_url(context):
                self.tokenize(context, doc_id)
        print("Parse Completed for " + doc_id)

    def tokenize(self, context, doc_id):
        """
        This method tokenize the context and put words into dictionary
        Here are the heuristics:
            list[0]: td-idf
        :param context: The context we retrieve from html
        :param doc_id: The document id of the word
        :return: modify the list
        """
        parsed = word_tokenize(context)
        for word in parsed:
            if len(word) == 0 or word is None:
                pass
            else:
                self.token[word][doc_id] += 1

    def update_list(self):
        """
        This method parse the html, and updates the index dictionaries
        :return: updates the index dictionary
        """
        for doc_id in self.json.keys():
            html = get_html(doc_id)
            self.parse_html(html, doc_id)

    def generate_post_dict_file(self):
        """
        This method will generate both dictionary and posting files from self.posting dictionary
        :return: create files
        """
        dic = open("dictionary.txt", "w")
        pos = open("posting.txt", "w")
        for k, v in self.token.items():
            dic.write(k.encode('utf-8') + "\n")
            pos.write(k.encode('utf-8') + " - ")
            for d, h in v.items():
                pos.write(d + ":" + str(h) + "; ")
            pos.write("\n")
        dic.close()
        pos.close()

    def get_total_doc(self):
        """
        This method returns the total number of documents
        :return: the total number of documents
        """
        return self.total

    def get_dict_unique_len(self):
        """
        This method returns the total number of unique words (excluding stop words) we get
        :return: the total number of words
        """
        return len(self.token.keys())

    def get_index(self):
        """
        This method will get the index dictionary
        :return: The whole index dictionary
        """
        return json.dumps(self.token)

    def get_idf(self):
        """
        This method will get the idf dictionary
        :return: The whole idf dictionary
        """
        return json.dumps(self.idf)


def get_html(doc_id):
    """
    This function reads data from the json dictionary, and get the corresponding html file from the dictionary
    :return: The string of html
    """
    files = open('WEBPAGES_RAW/' + doc_id, 'r')
    raw_text = files.read()
    files.close()
    return raw_text


def is_url(context):
    """
    This function determine whether the context is a url or not
    :param context: the context that we retrieve
    :return: if it is url, return true; if it is not url, return false
    """
    return len(context) > 5 and context[0:4] == "http"
