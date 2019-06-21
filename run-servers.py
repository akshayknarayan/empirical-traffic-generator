#!/usr/bin/python3

import shlex
import sys
import subprocess as sh

start_port = int(sys.argv[1])
num_procs = int(sys.argv[2])
cong_alg = sys.argv[3]

procs = [sh.Popen(shlex.split('./bin/etgServer -t {} -p {}'.format(cong_alg, start_port + i))) for i in range(num_procs)]
for p in procs:
    p.wait()

