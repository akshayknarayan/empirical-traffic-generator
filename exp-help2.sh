#!/bin/bash

sleep 1
x=$(ifconfig | grep delay | awk '{print $1}'| sed 's/://g') && sudo tc qdisc add dev $x root fq && echo $x
