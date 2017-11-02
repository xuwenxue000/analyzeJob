import jieba.posseg as pseg
import codecs
from gensim import corpora, models, similarities
import os

data_source = 'liepin'
file_dir = os.path.dirname(__file__)
stop_words = file_dir+'/stop_words.txt'
stopwords = codecs.open(stop_words,'r',encoding='utf8').readlines()
stopwords = [ w.strip() for w in stopwords ]

key_words = file_dir+'/job_dict.txt'
key_words = codecs.open(key_words,'r',encoding='utf8').readlines()
key_words = [ w.strip() for w in key_words ]
stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
words_all=set()

def tokenization(filename):
    result = []
    with open(filename, 'r') as f:
        text = f.read()
        words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
            if word not in key_words:
                words_all.add(word)
    return result

filenames = []
data_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_dir = data_dir + "/data/original/" + data_source + "/detail"
if os.path.exists(data_dir):
    files = os.listdir(data_dir)
    for id in files:
        filepath = data_dir+"/"+id+"/"+id+"_content.txt"
        filenames.append(filepath)

corpus = []

for each in filenames:
    corpus.append(tokenization(each))
print(len(words_all))
print(words_all)


dictionary = corpora.Dictionary(corpus)
doc_vectors = [dictionary.doc2bow(text) for text in corpus]
tfidf = models.TfidfModel(doc_vectors)
tfidf_vectors = tfidf[doc_vectors]
index = similarities.MatrixSimilarity(tfidf_vectors)
lsi = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=3)

query = tokenization(file_dir+'/my.txt')
query_bow = dictionary.doc2bow(query)
sims = index[query_bow]
print(sims)