from __future__ import division
import json
import math
import operator
from collections import defaultdict, OrderedDict, Counter
import sys
import bs4
from bs4 import BeautifulSoup
import re
import nltk
from nltk.util import ngrams
import os
from os import listdir
import glob
from os.path import isfile, join
from collections import OrderedDict
import os
import re
import math
from sets import Set
from bs4 import BeautifulSoup

from nltk.stem.wordnet import WordNetLemmatizer
import en
lmtzr = WordNetLemmatizer()
variations={}
tset=en.verb.tenses()
qfile="testquery.txt"
tenseset1 = ['infinitive', 'present_participle', 'past_participle',]
tenseset2=['past', 'present']
subtense=['1','2','3','"*"']
def singularize(term):
    if en.is_noun(term):
         sterm = en.noun.singular(term)
         if sterm is not term :
            variations[term].add(sterm)

def pluralize(term):
    if en.is_noun(term):
         pterm = en.noun.plural(term)
         if pterm is not term :
            variations[term].add(pterm)

def toverb(term):
     if en.is_noun(term):
        vterm=lmtzr.lemmatize(term,'v')
        if vterm is not term:
           variations[term].add(vterm)
def tonoun(term):
     if en.is_verb(term):
        nterm=lmtzr.lemmatize(term)
        if nterm is not term:
           variations[term].add(nterm)

def totenses(term):
    #if en.is_verb(term):
    for tense in tset:
        try:
            if en.verb.is_tense(term, tense, negated=True):
                for ctense in tenseset1:
                   fn= 'en.verb.' + ctense+'("'+term+'")'
                   tterm = eval(fn)
                   if tterm is not term:
                     variations[term].add(tterm)
                for ctense in tenseset2:
                   for st in subtense:
                     fn='en.verb.' + ctense+'("'+term+'",person='+st+ ',negate=False)'
                     tterm = eval(fn)
                     if tterm is not term:
                      variations[term].add(tterm)
        except:
            pass
def query_expansion_inflection(qterm):
    variations[qterm]=Set([qterm])
    singularize(qterm)
    pluralize(qterm)
    tonoun(qterm)
    toverb(qterm)
    totenses(qterm)
    current_terms=variations[qterm]
    for fterm in current_terms:
        totenses(fterm)
    return variations[qterm]

number_of_files =3204
query_freq = defaultdict(int)
tf_idf = defaultdict()
total_tf_idf = defaultdict()
unigram_index = {}
data = {}
docfreq={}
index_file = sys.argv[1]
doc_freq_file = sys.argv[2]
ignore = 0
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
            for aterm in data.split():
                eterms= query_expansion_inflection(aterm)
                for term in eterms:
                    if query_freq.get(term)==None:
                        query_freq[term] = 1
                    else:
                        query_freq[term] += 1
            for term in query_freq:
                try:
                    if docfreq.get(term) == None:
                        ni = 0
                        ignore+=1
                        print term
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
tf_idf_run("tf_idf_scoring_qe2")

