from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import cPickle as pickle
import string


"""
Goal: read in a file as a string and count LIWC words
"""

   
#Initializes Pennebaker dictionary from the real format
def init_pennebaker(filename):

    penne_dict={}
    
    #Read until we pass the second % sign
    in_dict=open(filename,'r')
    percent_count=0 #we have not passed the second % sign, this variable switches to true when we are reading in words
    
    for line in in_dict:
        if line.split()[0]=='%':
            percent_count+=1
            print 'found percent'
            continue
        if percent_count==2:
            #add the word to the dictionary
            tokens=line.split()
            key=tokens[0]
            penne_dict[key]=[]
            for i in range(1,len(tokens)):
                penne_dict[key].append(tokens[i])
                
    return penne_dict


#Takes in tokenized text and a dictionary of form {word:list of pennebaker categories}
#Outputs a dictionary of form {PennebakerCategory:Count}
#uncomment lines referring to 'log' for a sanity check
def count_pennebaker_words(words):


    #load Pennebaker dictionary
    penne_dict=pickle.load(open('penne_dict.p','rb'))
    
    #delete 'like' and 'kind' from Pennebaker dictionary (strange values)
    del penne_dict['like']
    del penne_dict['kind']
    
    #log=open('log.txt','w')
    
#init pennebaker_categories counts dict
    counts={}
    for i in range(1,23):
        counts[str(i)]=0
    for i in range(121,144):
        counts[str(i)]=0
    for i in range(146,151):
        counts[str(i)]=0
    for i in range(250,254):
        counts[str(i)]=0
    for i in range(354,361):
        counts[str(i)]=0
    for i in range(462,465):
        counts[str(i)]=0

    
    #Count pennebaker words
    for word in words:
        truncated_word=''
        for p_word in penne_dict.keys():
            truncate_index=p_word.find('*')
            if truncate_index != -1:#find returns -1 if the char is not found
                truncated_word=word[:truncate_index]
                if truncated_word == p_word.strip('*'):
                    #log.write('word is: '+word+'\n')
                    #log.write('match is: '+p_word+'\n')
                    for cat in penne_dict[p_word]:
                        counts[cat]+=1
            else:#word has no * in it
                if word==p_word:
                    #log.write('word is: '+word+'\n')
                    #log.write('match is: '+p_word+'\n')
                    for cat in penne_dict[p_word]:
                        counts[cat]+=1

    
    #normalize counts by word count
    # Leo: this is normalizing only the counts of the last category of the last seen word several times; 
    # the effect is to nullify one of the categories of a document.
    for count in counts:
        counts[cat]=float(counts[cat])/float(len(words))

    # Leo: fixed counts bug
#     print 'Cat:%s, unnorm. count:%d'%(cat, counts[cat])
#     print 'Cat:%s, norm. count:%f'%(cat, counts[cat]/float(len(words)))
#     
#    for cat in counts:
#        counts[cat]=float(counts[cat])/float(len(words))

    
    #log.close()
    return counts


#Computes Average Sentence Length
def avg_sentence_length(text):
    #tokenize the raw text into sentences
    sentences = sent_tokenize(text)
    
    #keep a running sum of words in each sentence
    sentence_lengths_sum=0
    for sentence in sentences:
        sentence_lengths_sum+=len(word_tokenize(sentence))

    #divide by the number of sentences to get the average
    avg_len = float(sentence_lengths_sum)/float(len(sentences))
    return avg_len

def word_count(words):
    return len(words)
    
#Loads a file as a string
def load_file(filename):
    #Read file in as a string
    inFile=open(filename,'r')
    raw_text=inFile.read()
    inFile.close()
    return raw_text
