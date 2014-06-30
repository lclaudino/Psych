import argparse, os, sys, cPickle as pickle, numpy as np
from sklearn.svm import SVR
from sklearn.cross_validation import KFold
from sklearn import preprocessing
from glob import iglob
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
#from gensim.models import LdaModel
from gensim.models.ldamallet import LdaMallet
from gensim import corpora

def to_tokenized(text_list, dictionary, stoplist):
    
    ret = RegexpTokenizer('[\w\d]+') 
    texts = [[word.encode('utf-8') for word in ret.tokenize(document.lower()) 
              if word not in stoplist and len(word) >= 3] for document in text_list]

#     texts = [[word.encode('utf-8','ignore') for word in ret.tokenize(document.lower()) 
#               if word not in stoplist and len(word) >= 3] for document in text_list]

    
    return [dictionary.doc2bow(jj) for jj in texts]



def to_corpus(text_list, stoplist):
    
    ret = RegexpTokenizer('[\w\d]+') 
    texts = [[word.encode('utf-8') for word in ret.tokenize(document.lower()) 
              if word not in stoplist and len(word) >= 3] for document in text_list]

    # remove words that appear only once
#     all_tokens = sum(texts, [])
#     tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
#     texts = [[word for word in text if word not in tokens_once]
#              for text in texts]

    dictionary = corpora.Dictionary(texts)
    return dictionary

def run_lda(pkl_exp_file, stoplist, num_topics, k, feat_folder):

    dict_lda = {}
    skf={}
    for ii in iglob(args.pkl_exp_file):

        dict_data = pickle.load(open(ii))
        texts=dict_data[2]
        dic = to_corpus(texts, stoplist) 
        
        skf[ii] = KFold(len(texts), k)
        if not dict_lda.has_key(ii):
            dict_lda[ii]={}
        
        #for train_index in skf:
        for ind,(train_index,_) in enumerate (skf[ii]):

            # train
            train_text = [dict_data[2][jj] for jj in train_index]
            train_corpus = to_tokenized(train_text, dic, stoplist)
            dict_lda[ii][ind] = LdaMallet(args.mallet_bin, train_corpus, num_topics, id2word=dic)
            #X_train_lda = lda[train_corpus]
            #X_train_lda = [zip(*jj)[1] for jj in X_train_lda]
    
            # test
            #test_text =  [dict_data[2][jj] for jj in test_index]
            #test_corpus = to_tokenized(test_text, dic, stoplist)
            #X_test_lda = lda[test_corpus]
            #X_test_lda = [zip(*jj)[1] for jj in X_test_lda]
            
    pickle.dump([dict_lda, skf], open(feat_folder + '/mallet.lda.topics_' + str(num_topics) + 
                                      '_k_' + str(k) + '.pkl', 'wb'))
            

          
if __name__ == '__main__':
    
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    
    parser = argparse.ArgumentParser( description = 'Experiment' )
    parser.add_argument( '--out_folder', type = str, dest = 'out_folder', default='./', 
                         help = 'Folder where outputs will be dumped')
    parser.add_argument( '--feat_folder', type = str, dest = 'feat_folder', default='./', 
                         help = 'Folder where features will be dumped')
    parser.add_argument( '--pkl_exp_file', type = str, dest = 'pkl_exp_file', 
                         help = 'Pickle file to run experiment')
    parser.add_argument( '--big5_var', type = str, dest = 'big5_var', 
                         help = 'Pickle which variable to experiment on: neuro, extra, consc, open, agree')
    parser.add_argument( '--num_topics', type = int, dest = 'num_topics', 
                         help = 'Number of topics to be used')
    parser.add_argument( '--mallet_bin', type = str, dest = 'mallet_bin', 
                         help = 'Path to Mallet LDA')
    parser.add_argument( '--k', type = int, dest = 'k', 
                         help = 'Number of folds to do k-fold with')

    stoplist = stopwords.words('english') + ['ive', 'id', \
                                             'doesn','didn', 'isn', \
                                             'aren', 'don', 'won', 'like', 'really']
    stoplist = [word.replace('\'','') for word in stoplist]

    args = parser.parse_args()

    # Run all LDA stuff at once
    lda_file=args.feat_folder + '/mallet.lda.topics_' + str(args.num_topics) +'_k_' + str(args.k) + '.pkl'
    if not os.path.exists(lda_file):
        dict_lda, skf = run_lda(args.pkl_exp_file, stoplist, args.num_topics, args.k, args.feat_folder)
    else:
        dict_lda, skf = pickle.load(open(lda_file,'rb'))

    r={}
    for ii in iglob(args.pkl_exp_file):
        #  Create the SVM regressor   
        svr = SVR(kernel='linear')
        
        dict_data = pickle.load(open(ii))
        var = dict_data[4][0].index(args.big5_var)
        
        X = preprocessing.scale(dict_data[0])
        y = np.asarray(zip(*dict_data[1])[var],np.float)
        texts=dict_data[2]
        dic = to_corpus(texts, stoplist) 
        
        #skf = KFold(len(y), args.k)
        r_X=[]
        r_lda=[]
        r_X_lda=[]
        for ind, (train_index, test_index) in enumerate(skf[ii]):

            lda=dict_lda[ii][ind]
            
            # Add the context features
            X_train, X_test = X[train_index], X[test_index]
            y_train, yt = y[train_index], y[test_index]

            # Compute LDA on training set and add features to both train and test
            # Train
            train_text = [dict_data[2][jj] for jj in train_index]
            train_corpus = to_tokenized(train_text, dic, stoplist)
            #lda = LdaMallet(args.mallet_bin, train_corpus, num_topics=20, id2word=dic)
            X_train_lda = lda[train_corpus]
            X_train_lda = [zip(*jj)[1] for jj in X_train_lda]

            # Test
            test_text =  [dict_data[2][jj] for jj in test_index]
            test_corpus = to_tokenized(test_text, dic, stoplist)
            X_test_lda = lda[test_corpus]
            X_test_lda = [zip(*jj)[1] for jj in X_test_lda]
            
            # Fit linear models for each case
            # X only
            svr.fit(X_train,y_train)
            y_X = svr.predict(X_test)

            # LDA only
            svr.fit(X_train_lda,y_train)
            y_lda = svr.predict(X_test_lda)
            
            # X + LDA
            svr.fit(np.concatenate((X_train, X_train_lda),axis=1),y_train)
            y_X_lda = svr.predict(np.concatenate((X_test, X_test_lda),axis=1))

            r_X.append(np.corrcoef(y_X-np.mean(y_X), yt-np.mean(yt))[0,1])
            r_lda.append(np.corrcoef(y_lda-np.mean(y_lda), yt-np.mean(yt))[0,1])
            r_X_lda.append(np.corrcoef(y_X_lda-np.mean(y_X_lda), yt-np.mean(yt))[0,1])

        # Will compute the average correlation coefficient per folder
        r[ii]=(np.mean(np.array(r_X)), np.mean(np.array(r_lda)), np.mean(np.array(r_X_lda)))
        
    # Print correlation coefficients
    pickle.dump(r,open(args.out_folder + '/'+args.big5_var+'.results.topics_' + str(args.num_topics) +
                       '_k_' + str(args.k) + '.pkl', 'wb'))
    #for ii in r:
    #    print ii, r[ii]
    #print np.mean(r.values())

    # SAME THING WITH ARABIC, BUT WITHOUT TOPICS (HUMAN ANNOTATED FEATURES)
    
    
    print 'Okay, done!'
    
    