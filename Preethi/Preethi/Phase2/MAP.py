from __future__ import division
from collections import OrderedDict
import os
import math
from sets import Set
from bs4 import BeautifulSoup
import re
import sys
import shutil
output_dir=sys.argv[1]
relavance_file = sys.argv[2]
myrank = {}
precision = {}
p_at_k_5 = {}
p_at_k_20 = {}
average_precision={}

rel_docs={}
def load_rel():
    i = 1
    while ( i < 65):
       rel_docs[str(i)]=Set()
       i += 1
    with open(relavance_file,'r') as relfile:
        lines=relfile.readlines()
        for line in lines:
            terms=line.split()
            que = terms[0].strip()
            rel_docs[que].add(terms[2].strip()+".html")

try:
    shutil.rmtree("Precision")
except:
    pass
os.getcwd()
os.mkdir("Precision")
load_rel()

qid = 1
while qid <= 64:
    relavant_retrieved = 0
    precision.clear()
    with open(output_dir+"\\Query_"+str(qid)+".txt",'r') as opfile:
        records= opfile.readlines()
        rank = 1
        relavant = rel_docs[str(qid)]
        sum_precision = 0
        for record in records:
            rel = False
            terms = record.split()
            current_retrieval = terms[2].strip()
            myrank[rank] = current_retrieval
            if current_retrieval in relavant:
                relavant_retrieved += 1
                rel = True
            precision[rank] = relavant_retrieved/rank
            if (rel):
                sum_precision += precision[rank]
            rank += 1
        average_precision[qid] = 0
        if relavant_retrieved == 0:
             average_precision[qid] = 0
        else:
            average_precision[qid] = sum_precision / relavant_retrieved
        p_at_k_5[qid] = precision[5]
        p_at_k_20[qid] = precision[20]
        with open('Precision\\Query_'+str(qid)+'.txt','a+') as precfile:
            precfile.write("###############################\n")
            precfile.write("Precision Values for Query "+str(qid)+"\n")
            precfile.write("###############################\n")
            for r in precision.keys():
                precfile.write("Query "+str(qid)+" Rank "+str(rank) + " Precision "+str(precision[r])+"\n")
    qid += 1

sum_average_precision=0
for doc_rank in average_precision.keys():
    print doc_rank,average_precision[doc_rank]
    sum_average_precision +=average_precision[doc_rank]
mean_avg_precision = sum_average_precision/64

with open('Precision\\MAP.txt','a+') as mapfile:
        mapfile.write("########################################\n")
        mapfile.write("Mean Average Precision Value for System \n")
        mapfile.write("########################################\n")
        mapfile.write(str(mean_avg_precision)+"\n")



with open('Precision\\P_at_5.txt','a+') as mapfile:
    mapfile.write("########################################\n")
    mapfile.write("Precision Values at K=5 for System \n")
    mapfile.write("########################################\n")
    for prec in p_at_k_5.keys():
        mapfile.write("Query_"+str(prec)+ " Precision at K=5: "+str(p_at_k_5[prec])+"\n")

with open('Precision\\P_at_20.txt','a+') as mapfile:
    mapfile.write("########################################\n")
    mapfile.write("Precision Values at K=20 for System \n")
    mapfile.write("########################################\n")
    for prec in p_at_k_20.keys():
        mapfile.write("Query_"+str(prec)+ " Precision at K=20: "+str(p_at_k_20[prec])+"\n")



