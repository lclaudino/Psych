
def export_mallet_topics_to_itm (keys, weights, out_folder):

	print 'Reading topic word weights'
	# Create tuples grouped by topic
	f=open(weights).readlines()
	d={}
	for ii in f:
		w=ii.split('\t')
		w[1] = w[1].strip()
		if not d.has_key(w[0]):
			d[w[0]] = {}

		if not d[w[0]].has_key(w[1]):
			d[w[0]][w[1]]={}
		
		d[w[0]][w[1]]=w[2]	

	print 'Reading topic key words and creating string'
	f=open(keys).readlines()
	s ='\n'
	for kk in f:

		t = kk.split('\t')
		topic=t[0]
		words=t[2].split(' ')[:-1]
		
		print topic[0]

		s += '--------------\nTopic ' + topic + '\n------------------------\n'
		for ii in words:
			s += d[topic][ii].strip() + '\t' + ii + '\n'
		
		
	print 'Writing file'

	f=open(out_folder + '/model.topics', 'w')
	f.write(s)
	f.close()
				
	
