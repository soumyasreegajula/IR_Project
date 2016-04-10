
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
from nltk.corpus import wordnet 





number_of_tokens_file = "number_of_tokens_one_gram.txt"


number_of_tokens = json.load(open(number_of_tokens_file))
index = json.load(open(sys.argv[1]))


N = len(number_of_tokens)
sum_tokens= sum(x['tokens_count'] for x in number_of_tokens.values())

avdl= float(sum_tokens/N)

query_freq = defaultdict(int)
bm25 = defaultdict(float)
			
k1 = 1.2 
k2 = 100.00
b = 0.75

data = {}
query_list=[]
index_file = sys.argv[1]
query_id=1


def Query_Expansion():
	
	queries_file = sys.argv[2]
	
	query_count = 1
	with open(queries_file, 'r') as query_file_obj:
		
		
		cleantext = BeautifulSoup(query_file_obj.read(),"html.parser")
		for tag in cleantext.findAll('docno'):
			tag.extract()
		for tag in cleantext.findAll('doc'):
			data={}
			
			text= str(tag.get_text()).replace('\n',' ')
			final_data=re.sub(r'[ ]+',r' ',text)
			data= re.sub(r'[^a-zA-Z0-9\s]+',r' ',final_data).lower()
			for term in data.split():
				query_freq[term] += 1
				
				for term in query_freq:

					query_list.append(term)
					
					
					for i,j in enumerate(wordnet.synsets(term)):
						
						
						query_list.append(j.lemma_names()[0])
						
					

			
			with open("Query_and_its_synonyms\\Query"+str(query_count)+".txt",'w') as query_exp:
				
				query_exp.write(str(query_list)+" ")
			query_exp.close()
				
			query_list.clear()
			
			with open("Query_and_its_synonyms\\Query"+str(query_count)+".txt",'r') as query_expansion:
				tokens = nltk.word_tokenize(query_expansion.read())
			with open("Expanded_Queries_Thesaurus\\Query_expanded"+str(query_count)+".txt",'w') as query_exp2:
				for i in set(tokens):
					
					clean_token=re.sub(r'[^a-zA-Z0-9\s]+',r'',str(i))
					token=re.sub(r'[ ]+',r' ',clean_token)
					query_exp2.write(str(token)+" ")
			query_exp2.close()
			query_expansion.close()		
			query_count+=1
			query_freq.clear()
			

					
			

Query_Expansion()
