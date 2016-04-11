import json
import math
import operator
from collections import defaultdict, OrderedDict, Counter
import sys
import os


rel_docs={}
recall = defaultdict(float)

def load_rel():
	rel_file=sys.argv[2]
	i = 0
	while ( i <=64):
		rel_docs[str(i)]=set()
		i += 1
	
	with open(rel_file,'r') as myfile:
		lines=myfile.readlines()
		for line in lines:
			terms=line.split()
			
			que = terms[0].strip()
			rel_docs[que].add(terms[2].strip()+".html")


def recall():

	retrieved_file=sys.argv[1]
	
	for dir_entry in os.listdir(retrieved_file):
		dir_entry_path = os.path.join(retrieved_file, dir_entry)

		if os.path.isfile(dir_entry_path):

			retrieved_count=0
			with open(dir_entry_path, 'r') as retrieved_file_obj:
				lines=retrieved_file_obj.readlines()
				
				for line in lines:
					terms=line.split()
					retrived_doc = terms[2].strip()
					for que,value in rel_docs.items():
						
						if ("Query"+str(que)+".txt"==str(os.path.basename(os.path.normpath(dir_entry_path)))):
							
							
							with open ("Recall_BM_25_Task_1\\Query"+str(que)+"recall"+".txt",'a+') as recall_file:
									
								
								if str(retrived_doc) in value:
									retrieved_count+=1
								
							
								if (len(value)!=0):
									recall=(retrieved_count)/(len(value))
									recall_file.write(str(round(recall,2)) +'\n')
									

								 
									
									
									


			

					
		


load_rel()
recall()