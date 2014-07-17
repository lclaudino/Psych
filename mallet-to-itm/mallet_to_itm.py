import argparse, os.path
from shutil import copyfile
from mallet_state_to_itm import export_mallet_states_to_itm
from export_mallet import export_mallet_topics_to_itm
from fake_lhood_file import fake_lhood_file
#from subprocess import Popen

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description = 'Create ITM files from Mallet LDA topic model' )
    parser.add_argument('--path_itm', type = str, dest = 'path_itm')
    parser.add_argument('--itm_output_folder', type = str, dest = 'itm_output_folder')
    parser.add_argument('--mallet_state_file', type = str, dest = 'mallet_state_file')
    parser.add_argument('--mallet_topic_file', type = str, dest = 'mallet_topic_file')
    parser.add_argument('--mallet_weight_file', type = str, dest = 'mallet_weight_file')
    parser.add_argument('--mallet_key_file', type = str, dest = 'mallet_key_file')
    parser.add_argument('--mallet_doc_file', type = str, dest = 'mallet_doc_file')
    parser.add_argument('--mallet_input_file', type = str, dest = 'mallet_input_file')
    parser.add_argument('--num_ite', type = int, dest = 'num_ite')
    parser.add_argument('--num_topics', type = int, dest = 'num_topics')
    parser.add_argument('--dataset', type=str, dest='dataset')

    args = parser.parse_args()
    init_folder = '%s/%s/output/T%d/init/'%(args.itm_output_folder, args.dataset, args.num_topics) 
    input_folder= '%s/%s/input/'%(args.itm_output_folder, args.dataset)
    if not os.path.exists(init_folder):
        os.makedirs(input_folder)
        os.makedirs(init_folder)
    
    # Copy mallet doc file
    docfile = '%s/model.docs'%(init_folder)
    copyfile(args.mallet_doc_file, docfile)
    # Copy mallet input file
    inputfile = '%s/%s-topic-input.mallet'%(input_folder,args.dataset)
    copyfile(args.mallet_input_file, inputfile)

    export_mallet_topics_to_itm(args.mallet_key_file, args.mallet_weight_file, init_folder)
    fake_lhood_file(args.num_ite, init_folder)

    # Save states
    [s, vocab] = export_mallet_states_to_itm(args.mallet_state_file)
    itm_input=open(init_folder+'/model.states','w')
    itm_input.write(s.strip())
    itm_input.close()

    # Save vocab
    itm_vocab=open('%s/%s.voc'%(input_folder, args.dataset),'w')
    itm_vocab.write('\n'.join(vocab))
    itm_input.close()


    #CHANGE TO CREATE AN INIT FOLDER WITH ESSENTIAL FILES. SHOULD INCLUDE THE DOCTOPICS FROM MALLET AS MODEL.DOCS
    #DATASET/OUTPUT/T#TOPICS/INIT/MODEL.*

    #MAY HAVE TO SETUP INPUT AS WELL with DATASET.VOC, DATASET.URL DATASET.TOPIC-INPUT-MALLET AND TREE_HYPERPARAMS

    #cmd='/usr/bin/java -cp %s/tree-TM/class:%s/tree-TM/lib/* '\
    #    'cc.mallet.topics.tui.GenerateTree --vocab %s/vocab.txt '\
    #    '--tree %s/tree_r1.wn'%(args.path_itm, args.path_itm, args.itm_output_folder, args.itm_output_folder)
     
    #Popen(cmd,shell=True).communicate()

    