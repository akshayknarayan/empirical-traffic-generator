#!/bin/bash

# $1 : start port
# $2 : num servers
# $3 : cong alg

for i in `seq 0 $2`; do
    ./empiricial-traffic-gen/bin/etgServer -t $3 -p $(($1 + $i)) >> /dev/null &
done
