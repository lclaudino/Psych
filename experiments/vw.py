import argparse, os, sys, random, math
from subprocess import Popen, PIPE

class VW:
    
    def __init__(self, vw_bin_path, model_name, holdout_every, flag_feats, out_folder):

        self.add_option=" "
        if len(flag_feats) > 0:
            self.add_option += flag_feats + " "
        print 'VW feature options: %s\n'%(flag_feats)


        self.train_cmd = (vw_bin_path + " --nn 100 -c -l 10 --passes 100" + self.add_option +
           "--invert_hash " + out_folder + model_name + 
           ".model.read -f "+ out_folder + model_name + '.model').split(" ")

        self.vw_bin_path=vw_bin_path
        self.model_read = out_folder + model_name +'.model.read'
        self.model_bin = out_folder + model_name +'.model'

    def train(self, vw_train_stream):
        p = Popen(self.train_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=1, close_fds=True)
        self.out_train = p.communicate(input=vw_train_stream)
    
    def test(self, vw_test_stream):
        self.test_cmd = (self.vw_bin_path + " -i " + self.model_bin + self.add_option + "-p /dev/stdout").split(" ")
        p = Popen(self.test_cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1)
        self.out_test = p.communicate(input=vw_test_stream)
        
    def leave_one_out(self, vw_file):
        data = open(vw_file).readlines()
        y=[]
        yr=[]
        for ii in enumerate(data):
            selected=data.pop(ii[0])
            self.train(''.join(data))
            print self.out_train[0]
            print self.out_train[1]
            self.test(selected)
            print self.out_test
            print self.out_test[0]
            print self.out_test[1]
            y.append(float(selected.split()[1]))
            yr.append(float(self.out_test[0]))
        # Will return here the Pearson score?
        return yr, y

    def k_fold(self, vw_file, k=3):
        data = open(vw_file).readlines()
        random.seed=11109
        random.shuffle(data)

        yr={}
        y={}
        len_part=int(math.ceil(len(data)/float(k)))
        for ii in range(k):
            test  = data[ii*len_part:ii*len_part+len_part]
            train = [jj for jj in data if jj not in test]
            self.train(''.join(train))
            print self.out_train[0]
            print self.out_train[1]
            self.test(''.join(test))
            print self.out_test[0]
            print self.out_test[1]
            yr[ii] = self.out_test[0].split('\n')[:-1]
            y[ii]=[jj.split()[0] for jj in test]
        
        return yr, y    

          
if __name__ == '__main__':
    
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    
    parser = argparse.ArgumentParser( description = 'Trainer' )
    parser.add_argument( '--out_folder', type = str, dest = 'out_folder', default='./', 
                         help = 'Folder where outputs will be dumped')
    parser.add_argument( '--model_name', type = str, dest = 'model_name', default='./', 
                         help = 'Name of the model being saved')
    parser.add_argument( '--vw_bin_path', type = str, dest = 'vw_bin_path', default='vw', 
                         help = 'Path to Vowpal Wabbit binary')
    parser.add_argument( '--flag_feats', type = str, dest = 'flag_feats', default='', 
                         help = ' Pattern that will tell Vowpal Wabbit extra options on features')
    parser.add_argument( '--holdout_every', type = int, dest = 'holdout_every', default=5, 
                         help = 'Frequency of holdout validation samples')
    parser.add_argument( '--vw_exp_file', type = str, dest = 'vw_exp_file', 
                         help = 'VW file to run experiment')

    args = parser.parse_args()
    vw = VW(args.vw_bin_path, args.model_name, args.holdout_every, args.flag_feats, args.out_folder)
    #vw.leave_one_out(args.vw_exp_file)
    [yr, y]=vw.k_fold(args.vw_exp_file)
    print 'Okay, done!'
    
    