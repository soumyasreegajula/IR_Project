import bs4
from bs4 import BeautifulSoup
import re
import nltk
import sys
#nltk.download()
from nltk.util import ngrams
import os


Unclean_Corpus_file = sys.argv[1]

data = {}
for dir_entry in os.listdir(Unclean_Corpus_file):
    dir_entry_path = os.path.join(Unclean_Corpus_file, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            
            data[dir_entry] = my_file.read()
            
            
            data[dir_entry]= data[dir_entry].replace("b'",'')
            
            
            
            cleantext = BeautifulSoup(data[dir_entry],"html.parser")
            
            
            for tag in cleantext.findAll('pre'):
                
                final_cleaned_data=cleantext.get_text()

                
            
            
            text= cleantext.get_text()
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            final_data=re.sub(r'[ ]+',r' ',text)
            cleancorpus= re.sub(r'[^a-zA-Z0-9\s]+',r' ',final_data).lower()
            
            
            tokens = nltk.word_tokenize(cleancorpus)
            

        with open(str(dir_entry),'a') as file_object:
            for i in tokens:
                file_object.write(i+" ")
