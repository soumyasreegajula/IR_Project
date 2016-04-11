import json
import math
import operator
from collections import defaultdict, OrderedDict, Counter
import sys
import os


rel_docs={}
recall = defaultdict(float)
MRR={}

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
				count=0
				for line in lines:
					rank=1

					terms=line.split()
					retrived_doc = terms[2].strip()
					
					for que,value in rel_docs.items():
						
						if ("Query"+str(que)+".txt"==str(os.path.basename(os.path.normpath(dir_entry_path)))):
							
							if str(retrived_doc) in value:
								if (count==0):
									rank=terms[3].strip()
									MRR[que]=str((float(1/float(rank))))
									
									count+=1

	with open ("MRR\\Query_MRR"+".txt",'a+') as recall_file:
		for key in sorted(MRR.keys()):
			recall_file.write(str(key) + " "+str(MRR[key])+'\n')


								
									
								



								

								
							
								
									

								 
									
									
									


			

					
		


load_rel()
recall()