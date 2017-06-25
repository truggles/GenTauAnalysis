#das_client --query="file dataset=/Tau/Run2017B-v1/RAW run=297039" --limit 2000

# Good runs from 2017 RunB
# https://hypernews.cern.ch/HyperNews/CMS/get/commissioning/7158.html
runs = [
    297179,
    297176,
    297175,
    297114,
    297113,
    297101,
    297100,
    297099,
    297057,
    297056,
    297050,
]

allRuns = open('allRunFiles.txt', 'w')
outMap = {}

import subprocess

for run in runs :
    toCall = ['das_client', '--query="file dataset=/Tau/Run2017B-v1/RAW run=%s"' % run, '--limit=5000']
    print " ".join(toCall)
    files = subprocess.Popen(" ".join(toCall), shell=True, stdout=subprocess.PIPE).stdout
    print run
    outMap["%s" % run] = []
    for file in files :
        if not 'Run2017B' in file : continue
        print ' --- ',file.strip()
        allRuns.write( '"%s",\n' % file.strip() )
        outMap["%s" % run].append("%s" % file.strip() )
allRuns.close()

import json
with open('files_per_run.json', 'w') as outFile :
    json.dump( outMap, outFile, indent=2 )
    outFile.close()

