#!/usr/bin/python3

import shlex
import sys
import subprocess as sh

procs = [sh.Popen(shlex.split('./bin/server -t reno -p {}'.format(5000 + i))) for i in range(int(sys.argv[1]))]
for p in procs:
    p.wait()

