
import json
import math
import operator
from collections import defaultdict, OrderedDict, Counter
import sys
import bs4
from bs4 import BeautifulSoup
import re
import nltk
import sys
from nltk.util import ngrams
import os
from os import listdir
import glob
from os.path import isfile, join
import sys


number_of_files =3204
query_freq = defaultdict(int)
tf_idf = defaultdict()
total_tf_idf = defaultdict()
unigram_index = {}
data = {}
docfreq={}
index_file = sys.argv[1]
doc_freq_file = sys.argv[2]
stop_file = sys.argv[4]
ignore = 0
stoplist=list()
def loadindex():
    with open(doc_freq_file,'r') as myfile:
         lines=myfile.readlines()
         for line in lines:
             termrec= line.split()
             docfreq[termrec[0]]=int(termrec[2])

    with open(index_file,'r') as unifile:
        lines=unifile.readlines()
        for line in lines:
            terms= line.split()
            terms_no_key = terms[1:]
            unigram_index[terms[0]] = {}
            for docf in terms_no_key:
                docterms = docf.split(',')
                unigram_index[terms[0]][docterms[0]]=int(docterms[1])
    with open(stop_file,'r') as unifile:
        lines=unifile.readlines()
        for w in lines:
            stoplist.append(w.strip())
        print stoplist

def tf_idf_run(folder):
    queries_file = sys.argv[3]
    with open(queries_file, 'r') as query_file_obj:
        global ignore
        query_id = 1
        cleantext = BeautifulSoup(query_file_obj.read(),"html.parser")
        for tag in cleantext.findAll('docno'):
            tag.extract()
        query_cnt = 0
        for tag in cleantext.findAll('doc'):
            query_cnt += 1
            text= str(tag.get_text()).replace('\n',' ')
            final_data=re.sub(r'[ ]+',r' ',text)
            data= re.sub(r'[^a-zA-Z0-9\s]+',r' ',final_data).lower()

            for term in data.split():
                if term not in stoplist:
                    if query_freq.get(term)==None:
                        query_freq[term] = 1
                    else:
                        query_freq[term] += 1
                else:
                    print term

            for term in query_freq:
                try:
                    if docfreq.get(term) == None:
                        ni = 0
                        ignore+=1
                        continue
                    else:
                        ni = docfreq[term]
                    idf = math.log(number_of_files/ni)
                    for doc_id,tf in unigram_index[term].items():
                        global tf_idf
                        if tf_idf.get(doc_id) == None:
                            tf_idf[doc_id] = 0
                        tf_idf[doc_id] += tf*idf
                except KeyError:
                    print ("error")
            sorted_index = OrderedDict(sorted(tf_idf.items(), key=operator.itemgetter(1), reverse=True))
            sorted_index_100 = Counter(tf_idf).most_common(100)
            sorted_index_list = sorted(tf_idf.items(), key=operator.itemgetter(1), reverse=True)#[:limit]
            rank = 1
            with open(folder+"\\tf_idf_query_"+str(query_cnt)+".txt",'a') as tf_idf_output:
                for doc,tf_idf1 in sorted_index_100:
                    tf_idf_output.write(str(query_id)  + "  "+ "Q0"+"  "+str(doc) + "  "+str(rank)   +  "  "+str(tf_idf1)+"\n")
                    rank += 1
                    query_id += 1
            tf_idf.clear()
            query_freq.clear()


loadindex()
tf_idf_run("tf_idf_scoring_stopping")