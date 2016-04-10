
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
	
	

	for dir_entry in os.listdir(queries_file):
		dir_entry_path = os.path.join(queries_file, dir_entry)
		if os.path.isfile(dir_entry_path):


			with open(dir_entry_path, 'r') as query_file_obj:

				bm25.clear()
		
				data = query_file_obj.read()
				
				
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

					sorted_index_list = sorted(bm25.items(), key=operator.itemgetter(1), reverse=True)#[:limit]
				
					rank = 1
					with open ("BM_25_Output\\"+ str(os.path.basename(os.path.normpath(dir_entry_path))),"w") as bm_25_score:
						

						for doc,bm25o in sorted_index_100:
							bm_25_score.write (str(os.path.basename(os.path.normpath(dir_entry_path)))  + "  "+ "Q0"+"  "+str(doc) + "  "+str(rank)   +  "  "+str(bm25o)+"\n")
				 	
							rank += 1
			
					
					query_freq.clear()
				
		
				
		
			

			

bm25_run()