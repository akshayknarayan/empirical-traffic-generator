#!/usr/bin/python3

import argparse
import random
import subprocess as sh
import sys
import time

parser = argparse.ArgumentParser(description="Run empirical traffic generator experiment")
parser.add_argument('--ip', type=str, dest='ip')
parser.add_argument('--cdf', type=str, dest='cdf')
parser.add_argument('--clients', type=int, dest='clients')
parser.add_argument('--load', type=str, dest='load')
parser.add_argument('--reqs', type=int, dest='reqs')
parser.add_argument('--outdir', type=str, dest='outdir')

def server_line(ip, i):
    return "server {} {}".format(ip, 5000 + i)

args = parser.parse_args()
with open('client.conf', 'w') as f:
    for i in range(args.clients):
        f.write(server_line(args.ip, i) + '\n')
    f.write('req_size_dist {}\n'.format(args.cdf))
    f.write('fanout 1 100\n')
    f.write('load {}\n'.format(args.load))
    f.write('num_reqs {}\n'.format(args.reqs))

sh.Popen('ssh {} "cd ~/empirical-traffic-gen && ./run-servers.py {} &"'.format(args.ip, args.clients), shell=True)
print('started servers')
time.sleep(2)
print('starting clients')
sh.run('./bin/client -c client.conf -l {} -s {}'.format(args.outdir, int(random.random() * 1000)), shell=True)

print('done')
sh.run('ssh {} "killall server"'.format(args.ip), shell=True)
>>>>>>> 13931b3... experiment script
