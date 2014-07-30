"""
Loads the metadata into a dictionary with specified primary keys and the values are dictionaries where the keys are attributes and the values are the attribute values.
NOTE: YOUR CSVS MUST BE STANDARDIZED

Meaning: all the same delimiter... order of attributes doesn't matter, but if an entry in a CSV is missing ANY of the attributes which are requested, it is
NOT returned in the metadata features dictionary.
""" 

import sys
import os, os.path
import cPickle as pickle


#Loads a CSV into a dict with keys as the primary key and features from the given features list
def load_CSV(filename,delimiter,primary_key,features_to_extract):
    print 'Attempting to load file: '+filename
    stripCount=0#this is the number of entries we do not return in the file dictionary
    
    #initialize blank dictionary
    file_dict={}

    #open file for reading
    in_csv=open(filename,'r')

    #read in the ordered set of attributes
    attributes=[]
    firstline=in_csv.readline()
    attr_names=firstline.split(delimiter)
    for attr in attr_names:
        attributes.append(attr.split('\r\n')[0])#may have to edit this by corpus

    #get primary key indices
    primary_key_indices={}
    for key in primary_key:
        try:
            primary_key_indices[key]=attributes.index(key)
        except:
            print 'Unable to find primary key '+str(key)
            return -1
        
    
    #this is used to figure out which feature is which in the csv
    feature_indices={}
    for feature in features_to_extract:
        try:
            feature_indices[feature]=attributes.index(feature)
        except:
            print 'Feature '+str(feature)+' not found in file '+filename
            print "Unexpected error:", sys.exc_info()[0]
            return {},0
    
    #read in each line
    for line in in_csv.readlines():
        
        #split line into parts
        line_attributes=line.split(delimiter)

        #extract primary key
        primary_key_list=[]#this will be cast as a tuple and used to key the dict
        for key in primary_key:
            primary_key_list.append(line_attributes[primary_key_indices[key]])

        #cast primary key list as tuple
        primary_key_tuple=tuple(primary_key_list)

        #Make sure this primary key is not in the dictionary already
        if primary_key_tuple in file_dict:
            print 'Primary key '+str(primary_key_tuple)+' found more than once.'
            raise
        
        features_dict={}
        #extract attributes we care about
        for feature in features_to_extract:
            #EDIT HERE TO GET RID OF CSV ARTIFACTS (Like \n etc)
            curFeature=line_attributes[feature_indices[feature]]
            curFeature_stripped=curFeature.split('\r\n')[0]
            features_dict[feature]=curFeature_stripped

        #make sure this entry has a complete primary key and feature set
        good=1
        for key in primary_key_tuple:
            stripped=key.replace(" ","")
            if stripped=="":
                good=0

        for feature in features_dict:
            stripped=features_dict[feature].replace(" ","")
            if stripped=="":
                good=0

        #PLACE ADDITIONAL FILTERS HERE
#        if good==1 and float(features_dict['bdi']) < 2:
 #           good=0
        
        #add them to the dict if they were properly formed
        if good==1:
            file_dict[primary_key_tuple]={}
            for feature in features_to_extract:
                file_dict[primary_key_tuple][feature]=features_dict[feature]
        else:
            stripCount+=1


    return file_dict,stripCount
        
#Given the directory where the data is, loops through the directory and loads each file, updating a global dict with that information
def load_all_CSVs(data_dir,delimiter,primary_key,features_to_extract,working_dir):
    numStripped=0
    all_dict={}#This is where the result metadata ends up

    for file_in_dir in os.listdir(data_dir):
        filename=data_dir+file_in_dir
        
        res=load_CSV(filename,delimiter,primary_key,features_to_extract)
        print res
        file_dict=res[0]
        numStripped+=res[1]

        
        #update new dictionary if none of the new keys are in it already
        for key in file_dict:
            if key in all_dict:
                print 'key '+str(key)+' found in more than one CSV'
                return -1
            
        all_dict.update(file_dict)

    #Print info about extraction
    print 'Total stripped entries: '+str(numStripped)
    print 'Final count of entries in feature dictionary: '+str(len(all_dict))
    
    #Dump metadata features to working directory 
    pickle_filename = working_dir+'metadata_features.p'
    d = os.path.dirname(pickle_filename)

    if not os.path.exists(d):#Make sure the folder exists
        os.makedirs(d)

    pickle.dump(all_dict,open(pickle_filename,'wb'))
    
    #return result
    return all_dict
