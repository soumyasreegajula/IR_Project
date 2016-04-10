
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
def bm25_run():
	
	index_file = sys.argv[1]
	queries_file = sys.argv[2]
	
	

	with open(queries_file, 'r') as query_file_obj:
		query_id = 1
		
		cleantext = BeautifulSoup(query_file_obj.read(),"html.parser")
		for tag in cleantext.findAll('docno'):
			tag.extract()
		for tag in cleantext.findAll('doc'):
			
			bm25.clear()
			text= str(tag.get_text()).replace('\n',' ')
			final_data=re.sub(r'[ ]+',r' ',text)
			data= re.sub(r'[^a-zA-Z0-9\s]+',r' ',final_data).lower()

			for term in data.split():
				query_freq[term] += 1
			
			
				for term in query_freq:

					
					if index.get(term)==None:
						continue
					else:
						ni = len(index[term])

						
						for doc_id,tf in index[term].items():
								
							k = k1*((1-b) + (b* (number_of_tokens[doc_id]['tokens_count'] / avdl)))
							term1 =  (N - ni + 0.5) / (ni + 0.5)
							term2 =  ((k1 + 1) * tf) / (k + tf)
							term3 =  ((k2 + 1) * query_freq[term]) / (k2 + query_freq[term])
									
							bm25[doc_id] += math.log(term1)*term2*term3
			
				sorted_index = OrderedDict(sorted(bm25.items(), key=operator.itemgetter(1), reverse=True))
				sorted_index_100 = Counter(bm25).most_common(100)

				sorted_index_list = sorted(bm25.items(), key=operator.itemgetter(1), reverse=True)

			

				
			rank = 1
			with open ("BM_25_Output\\Query"+ str(query_id)+".txt","w") as bm_25_score:
				bm_25_score.write(data+'\n')

				for doc,bm25o in sorted_index_100:
					bm_25_score.write (str(query_id)  + "  "+ "Q0"+"  "+str(doc) + "  "+str(rank)   +  "  "+str(bm25o)+"\n")
				 	
					rank += 1
				
			query_id += 1
			query_freq.clear()
			

bm25_run()