from subprocess import call
import os.path
import sys

#Change to local installation of MALLET


def main(num_topics, malletcmd, input_dirs,working_dir):
    print 'Input directory: '+str(input_dirs)

    mallet_working_dir=working_dir+'mallet_LDA_'+str(num_topics)+'/'
    if not os.path.exists(mallet_working_dir):#Make sure the directory exists, if not, create it
        os.makedirs(mallet_working_dir)

    flags=[]
    flags.append("import-dir")
    flags.append("--input")
    for directory in input_dirs:
        flags.append(directory)
    flags.append("--output")
    flags.append(mallet_working_dir+"topic-input.mallet")
    flags.append("--keep-sequence")
    flags.append("--remove-stopwords")

    cmd=malletcmd+flags

    print str(cmd)
    call(cmd)

    #Now have mallet topics imported to file topic-input.mallet
    #Time to build the topic model

    flags=[]
    flags.append("train-topics")
    flags.append("--input")
    flags.append(mallet_working_dir+"topic-input.mallet")
    flags.append("--num-topics")
    flags.append(str(num_topics))
    flags.append("--output-state")
    flags.append(mallet_working_dir+"topic-state.gz")
    flags.append("--output-topic-keys")
    flags.append(mallet_working_dir+"topic-keys.mallet")
    flags.append("--output-doc-topics")
    flags.append(mallet_working_dir+"doc-topics.mallet")

    cmd=malletcmd+flags
    call(cmd)

if __name__=="__main__":
    if len(sys.argv) < 4:
        print 'Usage: exec <num_topics> <input_dir1> ... <input_dirN> <working_dir>'
        sys.exit(0)

    num_topics=int(sys.argv[1])
    malletcmd = [sys.argv[2]]
    input_dirs=[]
    for i in range(3, len(sys.argv)-1):
        input_dirs.append(sys.argv[i])
    working_dir=sys.argv[len(sys.argv)-1]
    main(num_topics,malletcmd, input_dirs,working_dir)
