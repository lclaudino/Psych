import os.path, csv, glob, gzip, argparse
from nltk.tokenize import wordpunct_tokenize
from liwc import LIWC

def create_mallet_string(dict_data):
    
    dict_str={}
    for ii in dict_data.iterkeys():
        
        list_year = dict_data[ii]
        dict_str[ii] = '\n'.join([jj[0]['uid']+ ' none ' + \
                                  ' '.join(wordpunct_tokenize(jj[2].lower())) for jj in list_year])
            
    return dict_str

# creates one vw file per label in the big-5
def create_vw_string(dict_data):
    dict_str={}
    for ii in dict_data.iterkeys():
        
        dict_str[ii]={}
        
        list_year = dict_data[ii]
        neuro_str=''
        extra_str=''
        open_str=''
        agree_str=''
        consc_str=''
        for jj in list_year: # subjects
            liwc_str = ' '.join([kk+':'+ str(jj[1][kk]) for kk in jj[1].iterkeys()])
            neuro_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['neuro']) + ' |liwc ' + liwc_str +'\n'
            extra_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['extra']) + ' |liwc ' + liwc_str +'\n'
            open_str   +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['open'])  + ' |liwc ' + liwc_str +'\n'
            agree_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['agree']) + ' |liwc ' + liwc_str +'\n'
            consc_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['consc']) + ' |liwc ' + liwc_str +'\n'
        dict_str[ii]['neuro'] = neuro_str
        dict_str[ii]['extra'] = extra_str
        dict_str[ii]['open'] = open_str
        dict_str[ii]['agree'] = agree_str
        dict_str[ii]['consc'] = consc_str
        
    return dict_str   


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = 'Generate feature files for classification' )
    parser.add_argument( '--input_big5_folder', type = str, dest = 'input_big5_folder', 
                         help = 'Folder with essays of each subject')
    parser.add_argument( '--input_essay_folder', type = str, dest = 'input_essay_folder', 
                         help = 'Folder with csv files containing the big 5 scores of each subject')
    parser.add_argument( '--out_folder', type = str, dest = 'out_folder', default='./', 
                         help = 'Folder where outputs will be dumped')
    parser.add_argument( '--penne_dict_filename', type = str, dest = 'penne_dict_filename', 
                         help = 'Pickle with Pennebaker dictionary')
    
    args = parser.parse_args()

    liwc = LIWC(args.penne_dict_filename)
    d={}
    # Dict with big 5 scores
    #d[year][ (f1, f2, f3, f4, f5), ..., (f1, f2, f3, f4, f5) ]
    for ii in glob.iglob(args.input_big5_folder + '/*.csv'):
        print '\n--> Adding data from file: %s'%(ii)
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
                
                d_feats={}
                d_feats['uid'] = uid
                d_feats['neuro'] = neuro
                d_feats['extra'] = extra
                d_feats['open'] = opn
                d_feats['agree'] = agree
                d_feats['consc'] = consc

                if not d.has_key(year):
                    d[year] = []
                
                if len(year) > 0 and len(uid) > 0 and len(neuro) > 0 \
                and len(extra) > 0 and len(opn) > 0 and len(agree) > 0 and len(consc) > 0 \
                and os.path.exists(args.input_essay_folder+'/'+year+'_'+uid+'.txt'):
                    words = open(args.input_essay_folder+'/'+year+'_'+uid+'.txt').read()
                    liwc_feats = liwc.count_pennebaker_words(words)
                    d[year].append((d_feats, liwc_feats, words))
                else:
                    print 'Not found:' + year+'_'+uid
            except:
                continue
            
    # VW        
    dict_vw_str = create_vw_string(d)
    # LDA Mallet
    dict_mallet_str = create_mallet_string(d)
    for ii in dict_vw_str.iterkeys():
        open(args.out_folder + '/' + ii + '.mallet','wt').write(dict_mallet_str[ii])
        open(args.out_folder + '/' + ii + '-neuro.vw','wt').write(dict_vw_str[ii]['neuro'])
        open(args.out_folder + '/' + ii + '-extra.vw','wt').write(dict_vw_str[ii]['extra'])
        open(args.out_folder + '/' + ii + '-open.vw','wt').write(dict_vw_str[ii]['open'])
        open(args.out_folder + '/' + ii + '-agree.vw','wt').write(dict_vw_str[ii]['agree'])
        open(args.out_folder + '/' + ii + '-consc.vw','wt').write(dict_vw_str[ii]['consc'])

