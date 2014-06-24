import csv, os.path, gzip, glob
from lda import LDA
from nltk.tokenize import wordpunct_tokenize

class FeatureFiles:

    def __init__(self, feat_name):
        self.feat_name=feat_name

    def create_vw_string(self, dict_feats, dict_lda):
        pass
    
    def create_lda_string(self, dict_data, ind_text):
        dict_str={}
        for ii in dict_data.iterkeys():
            list_ii = dict_data[ii]
            dict_str[ii] = '\n'.join([jj[0]['uid'] + '\tnone\t' + \
                                      ' '.join(wordpunct_tokenize(jj[ind_text].lower())) for jj in list_ii])
                
        return dict_str
    
    def get_feats(self, args):
        pass
    
    # Get dictionary with LDA posteriori info
    def get_lda_feats(self, args, group_key, indiv_key):
        d={}
        for ii in glob.iglob(args.input_big5_folder + '/*.csv'):
            print '\n--> Adding lda data from file: %s'%(ii)
            if os.path.basename(ii) == 'gz':
                csvobj = csv.reader(gzip.open(ii), delimiter=',')   
            else:
                csvobj = csv.reader(open(ii, 'rb'), delimiter=',')
    
            header=csvobj.next()
            ind_group=header.index(group_key) # year
            ind_indiv=header.index(indiv_key) # id
            
            for jj in csvobj:
                try:
                    group=jj[ind_group].strip()
                    if not d.has_key(group):
                        d[group]=[]
                        ldaa = LDA(args.feat_folder+'/' + 'lda-' + args.num_topics + 
                                  '.'+self.feat_name+'-' + group + '.post')
                    
                    indiv=jj[ind_indiv].strip()
                    d[group].append(ldaa.posterior_feats(indiv))
                    print indiv
                except:
                    continue
        return d
