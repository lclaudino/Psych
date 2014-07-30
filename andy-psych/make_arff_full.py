"""
Creates a WEKA .arff file to load data
"""
import sys
import cPickle as pickle



"""updates d1 with d2's data"""
def join_dicts(d1,d2):
    for key in d1:
        if key not in d2:
            print 'fail'
            raise
    for key in d2:
        if key not in d1:
            print 'fail'
            raise

    #dicts have same keys
    for key in d2:
        d1[key].update(d2[key])
        
    return d1

def load_LIWC_map(map_file):
    LIWC_map={}
    infile=open(map_file,'r')
    for line in infile:
        toks=line.split()
        cat=toks[0]
        name=toks[1]
        LIWC_map[cat]=name

    return LIWC_map
    

def output_arff(feature_dict,arff_file):

    #Create attributes list
    attrs=[]
    arbitraryMember=feature_dict[feature_dict.keys()[0]]
    for attr in arbitraryMember:
        attrs.append(attr)
        

    #output header
    outfile=open(arff_file,'w')
    outfile.write('@RELATION\tstudent\n\n')
    for attr in attrs:
        outfile.write('@ATTRIBUTE\t'+str(attr)+'\tNUMERIC\n')
    outfile.write('\n\n@DATA\n')

    for key in feature_dict:
        for attr in attrs[0:len(attrs)-1]:
            outfile.write(str(feature_dict[key][attr])+',')
        outfile.write(str(feature_dict[key][attrs[len(attrs)-1]])+'\n')





if __name__=="__main__":
    if len(sys.argv) < 5:
        print 'Usage: exec <metadata_dict> <feature_dict> <lda_dict> <output_file> <map_file>'
        sys.exit(1)

    metadata_filename=sys.argv[1]
    text_feature_filename=sys.argv[2]
    map_file = sys.argv[3]
    output_filename=sys.argv[4]
        
    metadata_dict=pickle.load(open(metadata_filename,'rb'))
    text_features_dict=pickle.load(open(text_feature_filename,'rb'))
    LIWC_map=load_LIWC_map(map_file)

    joined=join_dicts(metadata_dict,text_features_dict)
    
    #transform into LIWC names
    for key in joined:
        for attr in joined[key].keys():
            if attr in LIWC_map:
                joined[key][LIWC_map[attr]]=joined[key][attr]
                del joined[key][attr]

                """
    print len(joined)
    for key in joined:
        print str(joined[key].keys())
        """
    
    
    output_arff(joined,output_filename)
    
    
        
