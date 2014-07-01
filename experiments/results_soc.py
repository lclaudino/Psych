import argparse, os, sys, cPickle as pickle, numpy as np

if __name__ == '__main__':
    
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    
    parser = argparse.ArgumentParser( description = 'Results' )
    parser.add_argument( '--pkl_file', type = str, dest = 'pkl_file')
    
    args = parser.parse_args()
    r = pickle.load(open(args.pkl_file,'rb'))
    
    liwc, lda, liwc_lda = zip(*r.values())
    
    print 'LIWC: %.4f +- %.4f'%(np.mean(liwc), np.std(liwc))
    print 'LDA: %.4f +- %.4f'%(np.mean(lda), np.std(lda))
    print 'LDA+LIWC: %.4f +- %.4f'%(np.mean(liwc_lda), np.std(liwc_lda))
    
    #for ii in r:
    #    print ii, r[ii]