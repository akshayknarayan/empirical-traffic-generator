import math
import sys
import time
import subprocess

algo=[['reno'],['ccp']]
#load=[["48Mbps","2000", "VL2_CDF"], ["48Mbps", "100000", "CAIDA_CDF"]]
load=[["72Mbps", "100000", "CAIDA_CDF"],]
nS = 50

for it in range(10):
    for a in algo:
        for l in load:
            f = open('run-multiple-server.sh','w')
            f.write("#!/bin/bash\n\n")
            for i in range(nS):
                f.write("./bin/server -t {} -p ".format(a[0])+str(5000+i)+" >> /dev/null &\n")
            f.close()

            f = open('mahimahiConfig', 'w')
            for i in range(nS):
                f.write("server 100.64.0.1 "+str(5000+i)+"\n")
            f.write("req_size_dist "+l[2]+"\n")
            f.write("fanout 1 100\n")
            f.write("load "+l[0]+"\n")
            f.write("num_reqs "+l[1]+"\n")
            f.close()
            subprocess.call("bash exp-help.sh {}-{}-{}-{}-{}".format('reno-'+a[0] if 'ccp' in a[0] else a[0], it, l[0], l[1], l[2]), shell=True)
