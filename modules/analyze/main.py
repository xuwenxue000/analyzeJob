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
def copyFiles(sourceDir,  targetDir):
    if sourceDir.find(".svn") > 0:
        return
    for file in os.listdir(sourceDir):
        sourceFile = os.path.join(sourceDir,  file)
        targetFile = os.path.join(targetDir,  file)
        if os.path.isfile(sourceFile):
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)

def tokenization(filename):
    result = []
    with open(filename, 'r') as f:
        text = f.read()
        words = pseg.cut(text,)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result

filenames = {}
data_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


source_data_dir =data_dir + "/data/original/" + data_source
template_dir = source_data_dir+ "/template"
template_ids_file = source_data_dir + "/template.txt"
no_template_ids_file = source_data_dir + "/no_template.txt"
data_detail_dir = source_data_dir + "/detail"
template_ids =[]
for id in open(template_ids_file):
    id = id.strip().replace("\n", "").replace("\r", "")
    template_ids.append(id)

if len(template_ids)>0:
    for id in template_ids:
        id = id.strip().replace("\n","").replace("\r","")
        sourceDir = data_detail_dir+"/"+id
        targetDir = template_dir+"/"+id
        copyFiles(sourceDir,  targetDir)

no_template_ids =[]
for id in open(no_template_ids_file):
    id = id.strip().replace("\n", "").replace("\r", "")
    no_template_ids.append(id)



if os.path.exists(data_detail_dir):
    files = os.listdir(data_detail_dir)
    for id in files:
        filepath = data_detail_dir+"/"+id+"/"+id+"_content.txt"
        filenames[id]= filepath
all_id=[]

with open(source_data_dir+"/all_id.txt","w") as f:
    for id in filenames.keys():
        f.write(id+"\n")
        all_id.append(id)
with open(source_data_dir+"/no_check.txt","w") as f:
    for id in all_id:
        if id not in template_ids and id not in no_template_ids:
            f.write(id+"\n")




corpus = []


for id in template_ids:
    path = filenames[id]
    word_file = template_dir+"/"+id+"/word_all.txt"
    cut_word = tokenization(path)
    o_cut_word = sorted(set(cut_word))
    corpus.append(cut_word)
    with open(word_file,"w") as f:
        for w in o_cut_word:
            f.write(w+"\n")
    #break
dictionary = corpora.Dictionary(corpus)
doc_vectors = [dictionary.doc2bow(text) for text in corpus]

tfidf = models.TfidfModel(doc_vectors)
tfidf_vectors = tfidf[doc_vectors]
lsi_model = models.LsiModel(tfidf_vectors, id2word=dictionary, num_topics=3)
index = similarities.MatrixSimilarity(tfidf_vectors)
def average(seq):
 return float(sum(seq)) / len(seq)

for id in filenames.keys():
    file_path = filenames[id]
    query = tokenization(file_path)
    query_bow = dictionary.doc2bow(query)
    sims = index[query_bow]
    ave_sims = average(sims)
    #0.12
    if ave_sims>0.12 and id not in template_ids:
        print(id+":"+str(ave_sims))



"""

print(len(words_all))
print(words_all)

query = tokenization(file_dir+'/my.txt')
corpus.append(query)







documents = lsi_model[corpus]
query_vec = lsi_model[query]
index = similarities.MatrixSimilarity(documents)


"""


