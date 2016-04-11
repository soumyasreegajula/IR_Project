from __future__ import division
from collections import OrderedDict
import os
import math
import shutil
from sets import Set
from bs4 import BeautifulSoup
import re
import sys
k1=1.2
b=0.75
k2=100
K = 0
N=3204
docfreq={}
unigram_index= {}
document_list = {}
doc_id_hash = {}
unigram_index = {}
avdoclen = 0
mypath = "Clean_Corpus_punctuation_removed"
from os import listdir
corpusfiles = [f for f in listdir("Clean_Corpus_punctuation_removed")]
query={}
queries_file = "cacm.query"
rel_judgment = "cacm.rel"
rel_docs={}
def bm25_term(term,doc_freq,K,term_freq,query_freq,r,R):
    term1 = 0
    term2 = 0
    term3 = 0
    #print term,r,R,doc_freq,N
    temp1 = ((r + 0.5) / (R - r + 0.5))
    temp2 = (doc_freq - r + 0.5)
    temp3 = (N - doc_freq - R + r + 0.5)
    #print temp1,temp2,temp3
    temp = ((r + 0.5) / (R - r + 0.5))/((doc_freq - r + 0.5)/(N - doc_freq - R + r + 0.5))
    #print temp
    term1 = math.log(temp)
    term2=((k1 + 1)*term_freq)/(K + term_freq)
    term3 =((k2 + 1)*query_freq)/(k2 + query_freq)
    return (term1*term2*term3)

def bm25_score(qid,queryterms,qf):
    bm25 = {}
    relavant_set = rel_docs[str(qid)]
    R = len(relavant_set)
    for term in queryterms.keys():
        if unigram_index.get(term) == None:
            continue;
        document_list= unigram_index[term]
        #print document_list
        doc_set=Set()
        doc_set.update(document_list)
        #print term,doc_set
        temprelset = Set()
        temprelset.update(relavant_set)
        #print temprelset
        temprelset = temprelset.intersection(doc_set)
        print temprelset
        r = len(temprelset)
        #print r
        if(r > 0):
            print relavant_set
            print temprelset
            print qid,r,term
        for doc in document_list.keys():
            statinfo = os.stat(mypath+"\\"+doc)
            size_factor = statinfo.st_size / avdoclen
            K = (k1 * ( (1 - b) + (b*size_factor)))
            if bm25.get(doc) == None:
                bm25[doc] = 0
            bm25[doc] += round(bm25_term(term,docfreq[term],K,unigram_index[term][doc],queryterms[term],r,R),2)
    sort_dict = sorted(bm25, key = bm25.get,reverse = True)[:100]
    rank =1
    with open('BM25_op_relevance\\Query'+str(qid)+'.txt','a+') as myfile:
        myfile.write("########################################################\n")
        myfile.write("Query: "+query[qid]+"\n")
        myfile.write("########################################################\n")
        for doc in sort_dict:
            myfile.write(str(qid)+" "+"Q0 "+doc+ " " +str(rank)+ " "+ str(bm25[doc])+" BM25\n")
            rank += 1

def average_doc_length():
    total_length = 0
    for f in corpusfiles:
        statinfo = os.stat(mypath+"\\"+f)
        total_length += statinfo.st_size
    average_doc_len = 0
    average_doc_len = total_length / N
    print average_doc_len
    return average_doc_len

def load_rel():
    i = 1
    while ( i < 65):
       rel_docs[str(i)]=Set()
       i += 1
    print rel_docs
    with open(rel_judgment,'r') as myfile:
        lines=myfile.readlines()
        for line in lines:
            terms=line.split()
            que = terms[0].strip()
            rel_docs[que].add(terms[2].strip()+".html")
        print rel_docs
def loadindex():
    with open("table2_unigram.txt",'r') as myfile:
         lines=myfile.readlines()
         for line in lines:
             termrec= line.split()
             docfreq[termrec[0]]=int(termrec[2])

    with open("unigram_index.txt",'r') as unifile:
        lines=unifile.readlines()
        for line in lines:
            terms= line.split()
            terms_no_key = terms[1:]
            unigram_index[terms[0]] = {}
            for docf in terms_no_key:
                docterms = docf.split(',')
                unigram_index[terms[0]][docterms[0]]=int(docterms[1])
try:
    shutil.rmtree("BM25_op_relevance")
except:
    pass
loadindex()
load_rel()
avdoclen = average_doc_length()
os.getcwd()
os.mkdir("BM25_op_relevance")
with open(queries_file, 'r') as query_file_obj:
    query_id = 0
    cleantext = BeautifulSoup(query_file_obj.read(),"html.parser")
    for tag in cleantext.findAll('docno'):
        tag.extract()
    for tag in cleantext.findAll('doc'):
        text= str(tag.get_text()).replace('\n',' ')
        final_data=re.sub(r'[ ]+',r' ',text)
        data= re.sub(r'[^a-zA-Z0-9\s]+',r' ',final_data).lower()
        query_id +=1
        query[query_id] = data
        terms=data.split()
        queryterms={}
        for term in terms:
            if queryterms.get(term) == None:
                queryterms[term]=1
            else:
                queryterms[term]+=1
        bm25_score(query_id,queryterms,queries_file)

