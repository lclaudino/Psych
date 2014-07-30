"""
Runs the whole process from start to finish

1. extract metadata from csv directory
2. extract features from text
3. correlate metadata features with text features
"""

import extract_metadata_features as emf
import extract_text_features as etf
import correlate as corr
import sys
import os,os.path
from optparse import *

def main():
    #Change this to your data directory. Expects that to have three things: a 'metadata' directory full of CSVs, a 'text' directory
    #full of text, and a file_map.txt which is a tsv

    parser = OptionParser()
    parser.add_option("--data-dir",dest="data_dir")
    parser.add_option("--working-dir",dest="working_dir")
    parser.add_option("--primary-key",dest="primary_key")#comma separated
    parser.add_option("--extract-features",dest="extract_features")#comma separated

    (options,args)=parser.parse_args()

    if not options.data_dir:
        parser.error("Provide data directory (--data-dir)")
    if not options.working_dir:	
        parser.error("Provide working directory (--working-dir)")
    if not options.primary_key:
        parser.error("Provide primary key --primary-key (comma separated)")
    if not options.extract_features:
        parser.error("Provide features to extract --extract-features (comma separated)")

    working_dir=options.working_dir
    #Create working directory if it doesn't exist
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)


    #extract metadata features
    data_dir=options.data_dir
    csv_dir=data_dir+'metadata/'
    primary_key=options.primary_key.split(',')
    features_to_extract=options.extract_features.split(',')
    print 'Primary key: %s',primary_key
    print 'Features to extract: %s',features_to_extract
    delimiter=','
    metadata=emf.load_all_CSVs(csv_dir,delimiter,primary_key,features_to_extract,working_dir)

    #extract document-level text features
    text_features,metadata=etf.extract(metadata,data_dir,working_dir)

    print 'Length of text features in driver: '+str(len(text_features))
    print 'Length of metadata featurees in driver: '+str(len(metadata))


if __name__=="__main__":
    
    main()
