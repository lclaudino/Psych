import os.path, csv, glob, gzip, argparse, cStringIO, codecs, numpy as np, cPickle as pickle
from operator import itemgetter
from feature_files import FeatureFiles

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")
    

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
        
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]
        
    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)



class FeatureFilesCasl(FeatureFiles):

    def __init__(self, feat_name='casl'):
        FeatureFiles.__init__(self, 'casl')
        self.dict_feats={}

    def create_data_matrices(self, dict_sent):
    
        dict_data = {}
        for ii in dict_sent.iterkeys():
            list_sent = dict_sent[ii]
            d_X, d_y, d_text = zip(*list_sent)
            X = [jj.values() for jj in d_X]
            text = [jj for jj in d_text]
            y = [jj.values()  for jj in d_y]
            X_names = [jj.keys()  for jj in d_X]
            y_names = [jj.keys()  for jj in d_y]
            
            dict_data[ii] = (np.asmatrix(X,np.float), y, text, X_names, y_names)

        return dict_data


    # creates one vw file per label in the big-5 including the liwc features and lda, if posterior file passed
    def create_vw_string(self, dict_human_feats, dict_lda):
    
        dict_str={}
        for ii in dict_human_feats.iterkeys():
            
            dict_str[ii]={}
            
            list_sent = dict_human_feats[ii]
            list_lda  = dict_lda[ii]
    
            sent_str=''
            
            for jj, ll in zip(list_sent, list_lda): # subjects
                score_str = ' '.join([kk+':'+ str(jj[1][kk]) for kk in jj[1].iterkeys()])
                lda_str=''
                lda_str += ' |mallet ' + ' '.join(['topic_' + str(kk[0]) + ':' + str(kk[1]) for kk in sorted(ll, key=itemgetter(0))]) 
                sent_str  +=  str(jj[0]['uid']) + " 1 " + str(jj[0]['sent']) + ' |lda ' + score_str + lda_str + '\n'
                
            dict_str[ii]['sent'] = sent_str
    
        return dict_str   

    # This is to use the features that were annotated by humans: 
    # religious_boolean - {0,1} to whether tweet contains a religious expression in any religion.
    # abusive_boolean - {0, 1} to whether tweet contains abusive language (e.g. racism).
    # profanity_boolean - {0, 1} to whether tweet contains profanity.
    # national_role_boolean - {0, 1} to whether tweet calls upon a national role, a WMD-specific sociocultural feature.
    
    def get_feats(self, args):
        
        d={}

        for ii in glob.iglob(args.input_tsv_folder + '/*.tsv.filt'):
            print '\n--> Adding casl data from file: %s'%(ii)
            if os.path.basename(ii) == 'gz':
                csvobj = UnicodeReader(gzip.open(ii), delimiter=',')   
            else:
                csvobj = UnicodeReader(open(ii, 'rb'), delimiter=',')
    
            header=csvobj.next()
            ind_sent=header.index('sent')
            ind_text=header.index('text')   
            ind_uid=header.index('id')
            ind_religious=header.index('religious')
            ind_abusive=header.index('abusive')
            ind_profanity=header.index('profanity')
            ind_national=header.index('national')
            
            for jj in csvobj:
                try:
                    # Sentiment score/label
                    sent=jj[ind_sent].strip()

                    # Text
                    text=jj[ind_text].strip()

                    # Features
                    d_feats={}
                    d_feats['uid']=jj[ind_uid].strip()
                    d_feats['relig']=jj[ind_religious].strip()
                    d_feats['abus']=jj[ind_abusive].strip()
                    d_feats['prof']=jj[ind_profanity].strip()
                    d_feats['nat']=jj[ind_national].strip()
                    
                    # ii is treated as an individual dataset
                    if not d.has_key(os.path.basename(ii)):
                        d[os.path.basename(ii)] = []
                    d[os.path.basename(ii)].append((d_feats, {'sent': sent}, text))
                except:
                    print 'Whoops'
                    continue
        return d

if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = 'Generate feature files for classification' )
    parser.add_argument( '--input_tsv_folder', type = str, dest = 'input_tsv_folder', 
                         help = 'Folder with essays of each subject')
    parser.add_argument( '--feat_folder', type = str, dest = 'feat_folder', default='./', 
                         help = 'Folder where features will be dumped')
    args = parser.parse_args()

    ffc = FeatureFilesCasl()
    dict_feats = ffc.get_feats(args)
    dict_data_matrices = ffc.create_data_matrices(dict_feats)
    for ii in dict_data_matrices.iterkeys():
        pickle.dump(dict_data_matrices[ii], open(args.feat_folder + '/soc-' + ii + '.sent.pkl','wb'))

    #dict_lda_str = ffc.create_lda_string(dict_feats, 2)

    #for ii in dict_lda_str.iterkeys(): # NOT WORKING
    #    open(args.feat_folder + '/casl-' + ii + '.mallet','wt').write(dict_lda_str[ii].encode('utf-8'))

# WILL CREATE NEW INPUT FILES WITH ARABIC ALREADY TOKENIZED BY PETER SCRIPTS

