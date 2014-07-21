import argparse, os.path, csv_with_encoding as csvwe, codecs
#, re
from shutil import copyfile
from mallet_state_to_itm import export_mallet_states_to_itm
from export_mallet import export_mallet_topics_to_itm
from fake_lhood_file import fake_lhood_file
#from subprocess import Popen

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description = 'Create ITM files from Mallet LDA topic model' )
    parser.add_argument('--path_itm', type = str, dest = 'path_itm')
    parser.add_argument('--itm_release_folder', type = str, dest = 'itm_release_folder')
    parser.add_argument('--mallet_state_file', type = str, dest = 'mallet_state_file')
    parser.add_argument('--mallet_topic_file', type = str, dest = 'mallet_topic_file')
    parser.add_argument('--mallet_weight_file', type = str, dest = 'mallet_weight_file')
    parser.add_argument('--mallet_doc_file', type = str, dest = 'mallet_doc_file')
    parser.add_argument('--mallet_input_file', type = str, dest = 'mallet_input_file')
    parser.add_argument('--doc_ids', type = str, dest = 'doc_ids')
    parser.add_argument('--real_docs', type = str, dest = 'real_docs')
    parser.add_argument('--num_ite', type = int, dest = 'num_ite')
    parser.add_argument('--num_topics', type = int, dest = 'num_topics')
    parser.add_argument('--dataset', type=str, dest='dataset')

    args = parser.parse_args()
    init_folder = '%s/results/%s/output/T%d/init/'%(args.itm_release_folder, args.dataset, args.num_topics) 
    input_folder= '%s/results/%s/input/'%(args.itm_release_folder, args.dataset)
    data_folder = '%s/data/'%(args.itm_release_folder)
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(init_folder):
        os.makedirs(init_folder)
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    # Doc ids list the ids of the texts to be used
    doc_ids = [ii.strip() for ii in open(args.doc_ids,'r').readlines()]

    # csvobj has tuples obtained from the original documents csv
    csvobj = csvwe.UnicodeReader(open(args.real_docs,'r'), delimiter=',')
    header = csvobj.next()
    ind_text=header.index('text')   
    ind_uid=header.index('id')
    html_str=[]
    # Update html template file with documents and ids --> this is very inefficient!
    # Will include only the documents with the given doc_ids
    for ii in csvobj:
        if ii[ind_uid] in doc_ids:
            html_str.append('<div class="segment" id="%s"><p>%s</p></div>'%(ii[ind_uid],ii[ind_text]))
    html_str='\n'.join(html_str)
    html_str+='\n</body>\n</html>\n'

    # Write .html file
    html_str=open('template.html').read()+html_str
    codecs.open('%s/%s.html'%(data_folder,args.dataset),'w','utf-8').write(html_str)   

    # Read Mallet documents file here and replace second column with given ids
    doc_topic_rows = open(args.mallet_doc_file,'r').readlines()
    doc_topics_str=[]
    for ind, ii in enumerate(doc_topic_rows[1:]):
        rows=ii.split()
        rows[1] = doc_ids[ind]
        doc_topics_str.append(' '.join(rows))
    doc_topics_str = '\n'.join(doc_topics_str)
    itm_docs=open(init_folder+'/model.docs','w')
    itm_docs.write('#doc source topic proportion ...\n' +  doc_topics_str)    

    # Create .url file
    url = ['%s /data/%s.html#%s'%(ii,args.dataset,ii) for ii in doc_ids]
    urlfile = '%s/%s.url'%(input_folder,args.dataset) 
    open(urlfile,'w').write('\n'.join(url))    
    
    # Copy mallet input file
    inputfile = '%s/%s-topic-input.mallet'%(input_folder,args.dataset)
    copyfile(args.mallet_input_file, inputfile)

    # Convert topic list format from Mallet to ITM
    export_mallet_topics_to_itm(args.mallet_weight_file, 100, init_folder)

    # Create empty likelihood entries for the initial iterations run with Mallet
    fake_lhood_file(args.num_ite, init_folder)

    # Convert state files from Mallet to ITM
    [s, vocab] = export_mallet_states_to_itm(args.mallet_state_file)
    itm_states=open(init_folder+'/model.states','w')
    itm_states.write(s.strip())
    itm_states.close()

    # Save converted vocabulary
    itm_vocab=open('%s/%s.voc'%(input_folder, args.dataset),'w')
    itm_vocab.write('\n'.join(vocab))
    itm_vocab.close()
    
    # Write file with hyperparameters
    hyperparam_file=open('%s/tree_hyperparams'%(input_folder),'w')
    hyperparam_file.write('DEFAULT_ 0.01\nNL_ 0.01\nML_ 100\nCL_ 0.00000000001')
    hyperparam_file.close()


    #CHANGE TO CREATE AN INIT FOLDER WITH ESSENTIAL FILES. SHOULD INCLUDE THE DOCTOPICS FROM MALLET AS MODEL.DOCS
    #DATASET/OUTPUT/T#TOPICS/INIT/MODEL.*

    #MAY HAVE TO SETUP INPUT AS WELL with DATASET.VOC, DATASET.URL DATASET.TOPIC-INPUT-MALLET AND TREE_HYPERPARAMS

    #cmd='/usr/bin/java -cp %s/tree-TM/class:%s/tree-TM/lib/* '\
    #    'cc.mallet.topics.tui.GenerateTree --vocab %s/vocab.txt '\
    #    '--tree %s/tree_r1.wn'%(args.path_itm, args.path_itm, args.itm_release_folder, args.itm_release_folder)
     
    #Popen(cmd,shell=True).communicate()

    