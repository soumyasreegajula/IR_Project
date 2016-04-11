import os

unigram_index = {}
bigram_index = {}
trigram_index = {}
doc_id_hash={}

try:
    os.remove("table1_unigram.txt")
    os.remove("table2_unigram.txt")
    os.remove("numberoftokens.txt")

except OSError:
    pass


with open("unigram_index.txt",'r') as unifile:
    lines=unifile.readlines()
    for line in lines:
        terms= line.split()
        terms_no_key = terms[1:]
        unigram_index[terms[0]] = {}
        for docf in terms_no_key:
            docterms = docf.split(',')
            unigram_index[terms[0]][docterms[0]]=int(docterms[1])




unigram_index_term_freq={}



for key in unigram_index.keys():
    unigram_index_term_freq[key]=0
    docs = unigram_index[key]
    for doc in docs.keys():
        unigram_index_term_freq[key] += int(docs[doc])



sort_dict = sorted(unigram_index_term_freq, key = unigram_index_term_freq.get,reverse = True)

numberofunigramtokens = 0
with open("table1_unigram.txt",'a') as myfile:
    for key in  sort_dict:
        myfile.write(key+ ' '+str(unigram_index_term_freq[key])+"\n")
        numberofunigramtokens += unigram_index_term_freq[key]



sort_dict =  unigram_index.keys()
sort_dict.sort()
with open("table2_unigram.txt",'a') as  myfile:
    for key in sort_dict:
        term_dict = unigram_index[key]
        doclist = " {"+ ','.join(term_dict.keys())+"} "
        myfile.write(key + doclist + str(len(term_dict.keys()))+"\n")


with open("numberoftokens.txt",'a') as  myfile:
     myfile.write("No of unigram tokens " + str(numberofunigramtokens)+"\n")
