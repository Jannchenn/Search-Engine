from flask import Flask, request, render_template
from Database import db, get_json, idf_db
from wtforms import Form, StringField
from collections import defaultdict
import math
import time

app = Flask(__name__)

t1 = time.time()
db = db()
j = get_json()
i = idf_db()
t2 = time.time()
print("Read time: " + str(t2-t1))


class SearchBar(Form):
    word = StringField(label="Search: ")


@app.route('/', methods=['GET', 'POST'])
def index():
    word = SearchBar(request.form)
    return render_template("index.html", word=word)


@app.route('/Search')
def search():
    words = request.full_path[request.full_path.find('=')+1:].split("+")
    t3 = time.time()
    wq = cal_tfidf(words)
    rd = cal_score(words, wq)
    t4 = time.time()
    print ("Calculation time: " + str(t4-t3))
    t5 = time.time()
    lst = sorted(rd.keys(), key=lambda x: rd[x], reverse=True)
    t6 = time.time()
    print ("Sort time: " + str(t6-t5))
    urls = []
    t7 = time.time()
    for i in lst:
        if len(urls) < 20:
            urls.append(j[i])
        else:
            break
    t8 = time.time()
    print ("List time: " + str(t8-t7))
    return render_template("result.html", word=" ".join(words), url=urls)


def cal_tfidf(words):
    """
    This function calculates tfidf from the query word
    :param words: the list of words from query
    :return: the tfidf of each word in the query
    """
    query = defaultdict(float)
    for w in words:
        query[w] += 1
    for word, freq in query.items():
        tf = 1 + math.log10(freq)
        idf = math.log10(i[word])
        query[word] = tf * idf
    return query


def cal_score(words, wq):
    """
    This function calculate the score for each url, and return a dictionary with doc_id:scores
    :param words: the query words
    :param wq: the tfidf weights of query
    :return: the dictionary with doc_id and scores
    """
    rd = defaultdict(float)
    lg = defaultdict(float)
    for w in words:
        ww = wq[w]
        for word, docs in db.items():
            for doc_id, wd in docs.items():
                rd[doc_id] += ww * wd
                lg[doc_id] += wd**2
    for doc_id, v in rd.items():
        rd[doc_id] = v / math.sqrt(lg[doc_id])
    return rd


if __name__ == "__main__":
    app.run(debug=True)
