from subprocess import call

#python extract_driver.py ../Data/BDI_slices/BDI_slice2/test/ working/slices/slice2/

for i in range(3,10):
    cmd=[]
    cmd.append('python')
    cmd.append('extract_driver.py')
    cmd.append('../Data/BDI_slices/BDI_slice'+str(i)+'/test/')
    cmd.append('working/slices/slice'+str(i)+'/')
    
    print 'Running command: '+str(cmd)
    call(cmd)
