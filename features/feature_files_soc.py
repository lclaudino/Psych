import os.path, csv, glob, gzip, argparse
#from nltk.tokenize import wordpunct_tokenize
from operator import itemgetter
from liwc import LIWC
#from lda import LDA
from feature_files import FeatureFiles

# def create_mallet_string(dict_data):
#     
#     dict_str={}
#     for ii in dict_data.iterkeys():
#         
#         list_year = dict_data[ii]
#         dict_str[ii] = '\n'.join([jj[0]['uid'] + '\tnone\t' + \
#                                   ' '.join(wordpunct_tokenize(jj[2].lower())) for jj in list_year])
#             
#     return dict_str


class FeatureFilesSoc(FeatureFiles):

    def __init__(self, feat_name='soc'):
        FeatureFiles.__init__(self, 'soc')
        self.dict_feats={}

    # creates one vw file per label in the big-5 including the liwc features and lda, if posterior file passed
    def create_vw_string(self, dict_liwc, dict_lda):
    
        dict_str={}
        for ii in dict_liwc.iterkeys():
            
            dict_str[ii]={}
            
            list_liwc = dict_liwc[ii]
            list_lda  = dict_lda[ii]
    
            neuro_str=''
            extra_str=''
            open_str=''
            agree_str=''
            consc_str=''
            
            for jj, ll in zip(list_liwc, list_lda): # subjects
                liwc_str = ' '.join([kk+':'+ str(jj[1][kk]) for kk in jj[1].iterkeys()])
                lda_str=''
                lda_str += ' |mallet ' + ' '.join(['topic_' + str(kk[0]) + ':' + str(kk[1]) \
                                                   for kk in sorted(ll, key=itemgetter(0))]) 
    
                neuro_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['neuro']) + ' |liwc ' + liwc_str + lda_str + '\n'
                extra_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['extra']) + ' |liwc ' + liwc_str + lda_str + '\n'
                open_str   +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['open'])  + ' |liwc ' + liwc_str + lda_str + '\n'
                agree_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['agree']) + ' |liwc ' + liwc_str + lda_str + '\n'
                consc_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['consc']) + ' |liwc ' + liwc_str + lda_str + '\n'
                
            dict_str[ii]['neuro'] = neuro_str
            dict_str[ii]['extra'] = extra_str
            dict_str[ii]['open'] = open_str
            dict_str[ii]['agree'] = agree_str
            dict_str[ii]['consc'] = consc_str
            
        return dict_str   


# def get_lda(args):
# 
#     d={}
#     for ii in glob.iglob(args.input_big5_folder + '/*.csv'):
#         print '\n--> Adding lda data from file: %s'%(ii)
#         if os.path.basename(ii) == 'gz':
#             csvobj = csv.reader(gzip.open(ii), delimiter=',')   
#         else:
#             csvobj = csv.reader(open(ii, 'rb'), delimiter=',')
# 
#         header=csvobj.next()
#         ind_year=header.index('year')
#         ind_uid=header.index('id')
#         
#         for jj in csvobj:
#             try:
#                 year=jj[ind_year].strip()
#                 if not d.has_key(year):
#                     d[year]=[]
#                     lda = LDA(args.feat_folder+'/' + 'lda-' + args.num_topics + '.soc-' + year + '.post')
#                 
#                 uid=jj[ind_uid].strip()
#                 d[year].append(lda.posterior_feats(uid))
#                 print uid
#             except:
#                 continue
#     return d


    def get_feats(self, args):
        
        liwc = LIWC(args.penne_dict_filename)
        # Dict with big 5 scores
        #d[year][ (f1, f2, f3, f4, f5), ..., (f1, f2, f3, f4, f5) ]
        for ii in glob.iglob(args.input_big5_folder + '/*.csv'):
            print '\n--> Adding liwc data from file: %s'%(ii)
            if os.path.basename(ii) == 'gz':
                csvobj = csv.reader(gzip.open(ii), delimiter=',')   
            else:
                csvobj = csv.reader(open(ii, 'rb'), delimiter=',')
    
            header=csvobj.next()
            ind_year=header.index('year')
            ind_id=header.index('id')
            ind_neuro=header.index('neuro')
            ind_extra=header.index('extra')
            ind_open=header.index('open')
            ind_agree=header.index('agree')
            ind_consc=header.index('consc')
            
            for jj in csvobj:
                try:
                    year=jj[ind_year].strip()
                    uid=jj[ind_id].strip()
                    neuro=jj[ind_neuro].strip()
                    extra=jj[ind_extra].strip()
                    opn=jj[ind_open].strip()
                    agree=jj[ind_agree].strip()
                    consc=jj[ind_consc].strip()
                    
                    # Big-5 scores/labels
                    d_feats={}
                    d_feats['uid'] = uid
                    d_feats['neuro'] = neuro
                    d_feats['extra'] = extra
                    d_feats['open'] = opn
                    d_feats['agree'] = agree
                    d_feats['consc'] = consc
    
                    if not self.dict_feats.has_key(year):
                        self.dict_feats[year] = []
                    
                    if len(year) > 0 and len(uid) > 0 and len(neuro) > 0 \
                    and len(extra) > 0 and len(opn) > 0 and len(agree) > 0 and len(consc) > 0 \
                    and os.path.exists(args.input_essay_folder+'/'+year+'_'+uid+'.txt'):
                        words = open(args.input_essay_folder+'/'+year+'_'+uid+'.txt').read()
                        liwc_feats = liwc.count_pennebaker_words(words)
                        # filename, doc entry
                        self.dict_feats[year].append((d_feats, liwc_feats, words))
                    else:
                        print 'Not found:' + year+'_'+uid
                except:
                    print 'Whoops'
                    continue
    
        return self.dict_feats

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser( description = 'Features for stream of consciousness experiments' )
    parser.add_argument( '--create_vw_files', action='store_true', help = 'Create files to train vowpal wabbit')
    parser.add_argument( '--input_big5_folder', type = str, dest = 'input_big5_folder', 
                          help = 'Folder with essays of each subject')
    parser.add_argument( '--penne_dict_filename', type = str, dest = 'penne_dict_filename', 
                          help = 'Pickle with Pennebaker dictionary')
    parser.add_argument( '--input_essay_folder', type = str, dest = 'input_essay_folder', 
                         help = 'Folder with essays of each subject')
    parser.add_argument( '--feat_folder', type = str, dest = 'feat_folder', default='./', 
                         help = 'Folder where features will be dumped')
    parser.add_argument( '--num_topics', type = str, dest = 'num_topics', help = 'Number of topics')


    args = parser.parse_args()
    ffs = FeatureFilesSoc()
    dict_feats = ffs.get_feats(args)
    dict_lda_str = ffs.create_lda_string(dict_feats, 2)

    for ii in dict_lda_str.iterkeys():
        open(args.feat_folder + '/soc-' + ii + '.mallet','wt').write(dict_lda_str[ii])
        
    # You must run lda and compute posterior features before doing this
    if args.create_vw_files:
        
        dict_lda = ffs.get_lda_feats(args, 'year', 'id')
        dict_vw_str = ffs.create_vw_string(dict_feats, dict_lda)

        for ii in dict_vw_str.iterkeys():
            open(args.feat_folder + '/soc-' + ii + '.liwc.neuro.vw','wt').write(dict_vw_str[ii]['neuro'])
            open(args.feat_folder + '/soc-' + ii + '.liwc.extra.vw','wt').write(dict_vw_str[ii]['extra'])
            open(args.feat_folder + '/soc-' + ii + '.liwc.open.vw','wt').write(dict_vw_str[ii]['open'])
            open(args.feat_folder + '/soc-' + ii + '.liwc.agree.vw','wt').write(dict_vw_str[ii]['agree'])
            open(args.feat_folder + '/soc-' + ii + '.liwc.consc.vw','wt').write(dict_vw_str[ii]['consc'])


#
# 
#     parser = argparse.ArgumentParser( description = 'Generate feature files for classification' )
#     parser.add_argument( '--input_big5_folder', type = str, dest = 'input_big5_folder', 
#                          help = 'Folder with essays of each subject')
#     parser.add_argument( '--input_essay_folder', type = str, dest = 'input_essay_folder', 
#                          help = 'Folder with csv files containing the big 5 scores of each subject')
#     parser.add_argument( '--feat_folder', type = str, dest = 'feat_folder', default='./', 
#                          help = 'Folder where features will be dumped')
#     #parser.add_argument( '--num_topics', type = str, dest = 'num_topics', default='./', 
#     #                     help = 'Folder where outputs will be dumped')
#     parser.add_argument( '--penne_dict_filename', type = str, dest = 'penne_dict_filename', 
#                          help = 'Pickle with Pennebaker dictionary')
#     args = parser.parse_args()
# 
#     # Compute features    
#     d_lda = get_lda(args)
#     d_liwc = get_liwc(args)
# 
#     # Create feature files accordingly
#     dict_vw_str = create_vw_string(d_liwc, d_lda)
#     #dict_lda_str = create_mallet_string(d_liwc)
# 
#     for ii in dict_vw_str.iterkeys():
#         #open(args.feat_folder + '/soc-' + ii + '.mallet','wt').write(dict_lda_str[ii])
#         open(args.feat_folder + '/soc-' + ii + '.liwc.neuro.vw','wt').write(dict_vw_str[ii]['neuro'])
#         open(args.feat_folder + '/soc-' + ii + '.liwc.extra.vw','wt').write(dict_vw_str[ii]['extra'])
#         open(args.feat_folder + '/soc-' + ii + '.liwc.open.vw','wt').write(dict_vw_str[ii]['open'])
#         open(args.feat_folder + '/soc-' + ii + '.liwc.agree.vw','wt').write(dict_vw_str[ii]['agree'])
#         open(args.feat_folder + '/soc-' + ii + '.liwc.consc.vw','wt').write(dict_vw_str[ii]['consc'])

