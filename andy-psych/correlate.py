from scipy import stats
import cPickle as pickle
import ast
#import rpy2.robjects as robjects
import os, os.path

#Set plotting = True if you want to see a plot of attribute one against attribute two.
#Send in a second feature name as prodAttr if you want to compare attr1 against the product of attr2 and prodAttr.
#I have no idea why I implemented that.
def correlateDicts(d1,d2,attr1,attr2,plotting=False,prodAttr=None,corr_fnct='s'):
    ordered_keys=[]
    l1=[]
    l2=[]
    for key in d1:
        year=key[0]
        ID=key[1]
        
        val1=float(d1[key][attr1])

        val2=float(d2[key][attr2])

        l1.append(val1)
       #We are correlating with a product of two features from the second dictionary if this is true 
        if not prodAttr==None:
            val2*=float(d2[key][prodAttr])

        l2.append(val2)
    
    if plotting:
        plotLists(l1,l2,attr1,attr2)

    if corr_fnct=='s':
        return stats.spearmanr(l1,l2)
    elif corr_fnct=='p':
        return stats.pearsonr(l1,l2)
    else:
        print 'Correlation function '+str(corr_fnct)+' not recognized, returning spearman R'
        return stats.spearmanr(l1,l2)
"""
def plotLists(l1,l2,attr1,attr2):   
    rlist1=robjects.FloatVector(l1)
    rlist2=robjects.FloatVector(l2)
    robjects.r["plot"](l1,l2,xlab=attr1,ylab=attr2)
    raw_input()
"""
#returns a sorted list based on the correlation score
def dict_to_sorted_list(dct):
    lst=[]
    for key in dct:
        lst.append((key,float(dct[key][0])))

    return sorted(lst, key = lambda tup: tup[1],reverse=True)#switch to reverse = false for ascending order

#Takes two dictionaries with the same keys and outputs a list with pairs of keys and correlations between them
#if metadata_features_list is None, then it will correlate all feature pairs
def correlateFeatures(d1,d2,working_dir,result_file,metadata_features_list=None):
    result_dct={}

    #If they don't specify a metadata feature list, then we will correlate all the feature pairs
    if metadata_features_list == None:
        metadata_features_list=d1[d1.keys()[0]]

    for metadata_feature in metadata_features_list:
        print str('Computing correlations for '+metadata_feature)
        for key in d2[d2.keys()[0]]:#just want to loop through what the keys are for a given ID in the text features, this is an arbitrary one
            result_dct[(metadata_feature,key)]=correlateDicts(d1,d2,metadata_feature,key,plotting=False)

    #Sort the results dictionary
    sorted_results=dict_to_sorted_list(result_dct)

    pickle_filename=working_dir+'sorted_results.p'
    d = os.path.dirname(pickle_filename)
    if not os.path.exists(d):#Make sure the directory exists, if not, create it
        os.makedirs(d)

    #dump pickle to working directory
    pickle.dump(sorted_results,open(pickle_filename,'wb'))    

    #output sorted results to file
    output_filename=result_file
    out_file=open(output_filename,'w')
    for key,val in sorted_results:
        out_file.write(str(key)+'\t'+str(val)+'\n')
    out_file.close()

    return sorted_results
