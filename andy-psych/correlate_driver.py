"""
Correlates features from text with those from metadata.
This uses the feature dictionary pickles produced using
extract_driver.py.
"""

import sys
import cPickle as pickle
import correlate as corr

def main(working_dir, text_features_pickle,result_file):
	#load metadata features
	metadata_features=pickle.load(open(working_dir+'pruned_metadata_features.p','rb'))

	#load text features
	text_features=pickle.load(open(text_features_pickle,'rb'))

	for key in metadata_features:
		if key not in text_features:
			print str(key) + ' in metadata_features but not in text_features'

	for key in text_features:
		if key not in metadata_features:
			print str(key) + ' in text_features but not in metadata_features'


	sorted_results=corr.correlateFeatures(metadata_features,text_features,working_dir,result_file)


if __name__=="__main__":
	if len(sys.argv)!= 4:
		print 'Usage: exec <working_dir> <text_features_pickle> <result_file.tsv>'
		sys.exit()
	working_dir=sys.argv[1]
	text_features_pickle=sys.argv[2]
	result_file=sys.argv[3]
	main(working_dir,text_features_pickle,result_file)
