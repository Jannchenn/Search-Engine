import sys
import simplejson as json


def get_top_ten(word, token, json):
    """
    This method gets the top ten urls from a specific word
    :param word: the query word
    :return: the top 10 url
    """
    # lst = sorted(token[word].items(), key=lambda x: x[1][0])
    result = []
    for i, j in token[word].items():
        if len(result) < 10:
            result.append(json[i])
        else:
            break
    return result


if __name__ == '__main__':
    f = open("database.txt", "r")
    token = json.load(f)
    f.close()

    collection = open('WEBPAGES_RAW/bookkeeping.json')
    j = json.load(collection)
    collection.close()
    while True:
        query = raw_input("Please enter the word you'd like to search: ")
        list_of_urls = get_top_ten(query, token, j)
        print(query + ":")
        for link in list_of_urls:
            print("\t" + link)
        print
        print
