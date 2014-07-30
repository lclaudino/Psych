"""
Adds LDA features to the text features dictionary.

MUST run run_mallet.py with this working directory BEFORE running this or the doc-topics file will not exist.

Takes in text_features.p and creates text_features_LDA.p.
"""
import cPickle as pickle
import sys
import LDA.load_doc_topics as ldt

#Change this to your working directory as appropriate
#MUST RUN run_mallet.py with this working directory BEFORE running this or the doc-topics file will not exist
def main(working_dir, mallet_dir, file_map,output_pickle):
    LDA_dict=ldt.load_file(working_dir,mallet_dir,file_map)
    text_features_dict=pickle.load(open(working_dir+'text_features.p','rb'))

    matchcount=0
    for key in LDA_dict:
        if key in text_features_dict:
            matchcount+=1
            for topic in LDA_dict[key]:
                text_features_dict[key][topic]=LDA_dict[key][topic]


    print str(matchcount) + ' of ' + str(len(text_features_dict)) + ' with LDA data'


    pickle.dump(text_features_dict,open(output_pickle,'wb'))


if __name__=="__main__":
    if len(sys.argv)!=5:
        print 'Usage: exec <working_dir> <mallet_dir> <file_map> <output_pickle>'
        sys.exit(1)
        

    working_dir=sys.argv[1]
    mallet_dir=sys.argv[2]
    file_map=sys.argv[3]
    output_pickle=sys.argv[4]
    main(working_dir,mallet_dir,file_map,output_pickle)
        
