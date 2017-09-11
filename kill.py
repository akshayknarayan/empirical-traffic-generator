#import os
import subprocess
f = open("a.txt","r")
lines = f.readlines()
f.close()
lines = lines[0].strip()
for line in lines.split():
    #print line
    subprocess.Popen("kill -9 "+line,shell=True)
