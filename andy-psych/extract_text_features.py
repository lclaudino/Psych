#Makes use of the functions in doc_feature_extractors.py to perform feature extraction on text data.
#There is a delineated area for you to put in your own feature extraction methods. They can be put into doc_feature_extractors.py. Just add the proper call and name the key in the feature dictionary appropriately.

#You want to run method 'extract' given your metadata output from 'extract_metadata_features.py'.
#This method will automatically prune that dictionary down to only contain files with matching text files (ie, files which appear in the filemap.) Make sure only files which actually exist appear in the filemap.

import os, os.path
import sys
import cPickle as pickle
from nltk.tokenize import wordpunct_tokenize
import string

import doc_feature_extractors as dfe

def load_file_map(file_map_filename):
    file_map={}
    #load file map dictionary.
    #expects a tsv where the last token on a line is the filename and the
    #preceding values make up a primary key from the metadata features
    in_file_map=open(file_map_filename,'r')
    for line in in_file_map:
        tokens=line.split('\t')
        curKey=[]
        for token in tokens[0:len(tokens)-1]:
            curKey.append(token)
        key_tuple=tuple(curKey)
        file_map[key_tuple]=tokens[len(tokens)-1].strip()
    return file_map

def check_files(metadata,file_map):
    unfound_count=0
    for key in metadata:
        if key not in file_map:
            unfound_count+=1
    print 'Couldn\'t find files for '+str(unfound_count)+' keys.'

def extract(metadata,data_dir,working_dir):
        
    file_map=load_file_map(data_dir+'file_map.tsv')
    check_files(metadata,file_map)

    #initialize feature vector (keys will be tuples made from the primary keys from the metadata)
    feature_dict={}
    

    #loop through items in metadata and extract features
    computingCount=1
    for key in metadata.keys():

        print 'Extracting features for item '+str(key)+': '+str(computingCount)+' of '+str(len(metadata))
        computingCount+=1

        #initialize empty feature dict
        feature_dict[key]={}
        
        #Load file using the file map
        if key not in file_map:
            print 'File not found for key '+str(key)
            del metadata[key]
            del feature_dict[key]
            computingCount-=1
            continue

        text_filename=data_dir+'text/'+file_map[key]
        raw_text = dfe.load_file(text_filename)
        
        #parse string into words
        words = wordpunct_tokenize(raw_text)
        words = [w.lower() for w in words]

        #wordlist=raw_text.translate(string.maketrans("",""),string.punctuation)
        #^^^this is an alternate way of getting rid of punctuation, you can try using this instead of the nltk tokenizer

        #now have raw_text and lowercase words
        #THIS IS WHERE YOU PUT IN ALL THE FEATURES YOU WANT TO EXTRACT
        #EDIT extract_features.py TO FIT YOUR NEEDS
        #note that a function which extracts one feature should be keyed like avg_sent_len is here
        #a function which extracts multiple features should use dict.update, and the function should return a dictionary of features with no higher-level keys.
        try:
            # Leo: commented here to add only LIWC features
            #feature_dict[key]['avg_sent_len']=dfe.avg_sentence_length(raw_text)
            #feature_dict[key]['word_count']=dfe.word_count(words)
            feature_dict[key].update(dfe.count_pennebaker_words(words))
        except:
            print 'Failed extracting features from file: '+text_filename
            print "Unexpected error:", sys.exc_info()[0]
            del feature_dict[key]
            del metadata[key]#this is pruning metadata such that it will no longer contain entries which do not parse properly
            computingCount-=1
            
    if len(feature_dict) != len(metadata):
        print 'Warning: length of text features not same length as metadata'
    else:
        print 'Length of text features is the same length as metadata! This is good!'

    #Dump metadata features to working directory
    pickle1_filename = working_dir+'text_features.p'
    pickle2_filename = working_dir+'pruned_metadata_features.p'
    
    d = os.path.dirname(pickle1_filename)

    if not os.path.exists(d):#Make sure the folder exists
        os.makedirs(d)

    pickle.dump(feature_dict,open(pickle1_filename,'wb'))
    pickle.dump(metadata,open(pickle2_filename,'wb'))
    
    #return results
    return feature_dict,metadata
