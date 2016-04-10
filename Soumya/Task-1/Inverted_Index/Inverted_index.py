import re
import sys
import json
from collections import defaultdict
import os
import nltk
from nltk import ngrams

index_one_gram = defaultdict(lambda: defaultdict(int))
index_bi_gram = defaultdict(lambda: defaultdict(int))
index_tri_gram = defaultdict(lambda: defaultdict(int))


number_of_tokens_one_gram = defaultdict(lambda: defaultdict(int))
number_of_tokens_bi_gram = defaultdict(lambda: defaultdict(int))
number_of_tokens_tri_gram = defaultdict(lambda: defaultdict(int))



def inverted_index():
	corpus_file = sys.argv[1]
	
	  
	data = {}
	for dir_entry in os.listdir(corpus_file):
		dir_entry_path = os.path.join(corpus_file, dir_entry)
		if os.path.isfile(dir_entry_path):
			
			with open(dir_entry_path,'r') as file_object:
				data[dir_entry]=file_object.read()
				for line in data[dir_entry].splitlines():
					document_number = dir_entry


					n = 1
					onegrams = ngrams(line.split(), n)
					for grams in onegrams:

						index_one_gram[str(grams).replace(',','').replace('\'','').replace('[','').replace(']','').replace(')','').replace('(','')][document_number] += 1
						number_of_tokens_one_gram[document_number]['tokens_count'] += 1

					

					
	##### UNIGRAM FILES##############################################################################################################################################

	
	with open('index_one_gram.txt', 'w') as file_object:
		file_object.write(json.dumps(index_one_gram))


	with open('number_of_tokens_one_gram.txt', 'w') as file_object:
		
		file_object.write(json.dumps(number_of_tokens_one_gram))

	with open('Total_number_of_tokens_one_gram_in_1000_documnents.txt', 'w') as file_object:
		file_object.write("Number of tokens(unigram) for 1000 documents is as below:")
		tokens_count=0
		for doc_id,value in number_of_tokens_one_gram.items():

			for dl,count in value.items():
				tokens_count+=count

		file_object.write(str(tokens_count))

	
	with open('word_frequency_one_gram.txt', 'w') as file_object:
		for word,value in index_one_gram.items():
			file_object.write("("+ word + ")"+ " ")
			for doc_id, tf in value.items():
				file_object.write("(" + str(doc_id) + "," + str(tf) + ") ")
			file_object.write("\n")

	term_frequency_one_gram={}

	with open('term_frequency_one_gram.txt', 'w') as file_object:

		for word,value in index_one_gram.items():
			term_frequency_one_gram[word]=[]
			
			term_frequency=0
			for doc_id, tf in value.items():
				term_frequency+=tf
				
			term_frequency_one_gram[word].append(term_frequency)
		for k,v in sorted(term_frequency_one_gram.items(), key=lambda x: x[1],reverse=True):
			

			file_object.write(str(k) +" ")
			file_object.write(str(term_frequency_one_gram[k])+" ")
			file_object.write("\n")


	

	


	with open('doc_term_frequency_one_gram.txt', 'w') as file_object:

		for word,value in sorted(index_one_gram.items()):
			file_object.write("("+ word + ")"+ " ")
			doc_frequency=[]
			doc_id_list=[]
			for doc_id, tf in value.items():
				doc_frequency.append(doc_id)
				doc_id_list.append(doc_id)
			file_object.write(str(doc_id_list)+" ")
			file_object.write(str(len(doc_frequency)))
			file_object.write("\n")
	



inverted_index()
