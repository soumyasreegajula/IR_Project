import re
import sys
import json
from collections import defaultdict
import os
import nltk
from nltk import ngrams

index_one_gram = defaultdict(lambda: defaultdict(int))



number_of_tokens_one_gram = defaultdict(lambda: defaultdict(int))


regex = re.compile("^#\\s*[0-9]+$")

def inverted_index():
	Stemmed_Corpus= sys.argv[1]
	
	  
	data = {}
	with open(Stemmed_Corpus, 'r') as file_object:
		for line in file_object.readlines():
			
			if regex.match(line):
				document_number = line.split()[-1]
			else:

				for word in filter(lambda x: not x.isdigit(), line.split()):

					index_one_gram[word.lower()][document_number] += 1
					number_of_tokens_one_gram[document_number]['tokens_count'] += 1

					

					
	##### UNIGRAM FILES##############################################################################################################################################

	
	with open('Inverted_index_Stemmed_Corpus\\index_one_gram.txt', 'w') as file_object:
		file_object.write(json.dumps(index_one_gram))


	with open('Inverted_index_Stemmed_Corpus\\number_of_tokens_one_gram.txt', 'w') as file_object:
		
		file_object.write(json.dumps(number_of_tokens_one_gram))

	with open('Inverted_index_Stemmed_Corpus\\Total_number_of_tokens_one_gram_in_1000_documnents.txt', 'w') as file_object:
		
		tokens_count=0
		for doc_id,value in number_of_tokens_one_gram.items():

			for dl,count in value.items():
				tokens_count+=count

		file_object.write(str(tokens_count))

	
	with open('Inverted_index_Stemmed_Corpus\\word_frequency_one_gram.txt', 'w') as file_object:
		for word,value in index_one_gram.items():
			file_object.write("("+ word + ")"+ " ")
			for doc_id, tf in value.items():
				file_object.write("(" + str(doc_id) + "," + str(tf) + ") ")
			file_object.write("\n")

	term_frequency_one_gram={}

	with open('Inverted_index_Stemmed_Corpus\\term_frequency_one_gram.txt', 'w') as file_object:

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


	

	


	with open('Inverted_index_Stemmed_Corpus\\doc_term_frequency_one_gram.txt', 'w') as file_object:

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
