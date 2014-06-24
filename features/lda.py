import argparse

class LDA:

    def __init__(self, posterior_filename):
        
        # re-create dict without truncated keys
        self.posterior_filename = posterior_filename
        f = open(posterior_filename,'rt').readlines()

        self.dict_feats={}
        for ii in f[1:]:
            entries=ii.split()
            topic_keys=entries[3:][0::2]
            topic_feats=entries[3:][1::2]
            self.dict_feats[entries[2]]=[]
            for jj,kk in zip (topic_keys,topic_feats):
                self.dict_feats[entries[2]].append((int(jj), float(kk)))

    def posterior_feats(self, key):
        return self.dict_feats[key]


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = 'Prepare file to train Mallet LDA model' )
    parser.add_argument( '--input_csv_folder', type = str, dest = 'input_csv_folder', 
                         help = 'Folder with essays of each subject')
    parser.add_argument( '--feat_folder', type = str, dest = 'feat_folder', default='./', 
                         help = 'Folder where features will be dumped')

