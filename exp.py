import math
import numpy as np
import sys
import time
from matplotlib import pyplot as plt
import subprocess

algo=[["ccp","1"], ["reno", "2"], ["vegas","2"]]
load=[["48Mbps","2000", "VL2_CDF"], ["48Mbps", "100000", "CAIDA_CDF"]]
nS = 200

for a in algo:
    for l in load:
        f = open('run-multiple-server.sh','w')
        f.write("#!/bin/bash\n\n")
        for i in range(nS):
            f.write("./bin/server -t cubic -p "+str(5000+i)+" >> /dev/null &\n")
        for i in range(int(a[1])):
            f.write("./bin/server -t "+a[0]+" -p "+str(5000+nS+i)+" >> /dev/null &")
            if i!=int(a[1])-1:
                f.write("\n")
        f.close()

        f = open('mahimahiConfig', 'w')
        for i in range(nS+int(a[1])):
            f.write("server 100.64.0.1 "+str(5000+i)+"\n")
        f.write("req_size_dist "+l[2]+"\n")
        f.write("fanout 1 100\n")
        f.write("load "+l[0]+"\n")
        f.write("num_reqs "+l[1]+"\n")
        f.write("persistent_servers "+a[1])
        f.close()
        if a[0]=="ccp":
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)
            subprocess.call("sudo ./../ccp/ccpl --datapath=kernel --congAlg=nimbus useSwitching=true uest=96 bwEstMode=false flowMode=XTCP 2>&1 | tee "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-switch.log &",shell=True)
            subprocess.call("./exp-help.sh "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-switch",shell=True)
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)
            time.sleep(20)
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)
            subprocess.call("sudo ./../ccp/ccpl --datapath=kernel --congAlg=nimbus useSwitching=false uest=96 bwEstMode=false flowMode=XTCP 2>&1 | tee "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-XTCP.log &",shell=True)
            subprocess.call("./exp-help.sh "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-XTCP",shell=True)
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)

            time.sleep(20)
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)            
            subprocess.call("sudo ./../ccp/ccpl --datapath=kernel --congAlg=nimbus useSwitching=false uest=96 bwEstMode=false flowMode=DELAY 2>&1 | tee "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-DELAY.log &",shell=True)
            subprocess.call("./exp-help.sh "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2]+"-DELAY",shell=True)
            subprocess.call("sudo killall ccpl",shell=True)
            subprocess.call("sudo rm -rf /tmp/ccp*",shell=True)
            time.sleep(20)
        else:
            subprocess.call("./exp-help.sh "+a[0]+"-"+a[1]+"-"+l[0]+"-"+l[1]+"-"+l[2],shell=True)
