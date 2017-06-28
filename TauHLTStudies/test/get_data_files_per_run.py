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

allRuns = open('tauB_MINIAOD.txt', 'w')
outMap = {}

import subprocess

for run in runs :
    #toCall = ['das_client', '--query="file dataset=/Tau/Run2017B-v1/RAW run=%s"' % run, '--limit=5000']
    #toCall = ['das_client', '--query="file dataset=/SingleMuon/Run2017B-PromptReco-v1/AOD run=%s"' % run, '--limit=5000']
    toCall = ['das_client', '--query="file dataset=/Tau/Run2017B-PromptReco-v1/MINIAOD run=%s"' % run, '--limit=5000']
    print " ".join(toCall)
    files = subprocess.Popen(" ".join(toCall), shell=True, stdout=subprocess.PIPE).stdout
    print run
    outMap["%s" % run] = []
    for file in files :
        if not 'Run2017B' in file : continue
        print ' --- ',file.strip()
        allRuns.write( '"root://cms-xrd-global.cern.ch/%s",\n' % file.strip() )
        outMap["root://cms-xrd-global.cern.ch/%s" % run].append("%s" % file.strip() )
allRuns.close()

import json
with open('tauB_MINIAOD.json', 'w') as outFile :
    json.dump( outMap, outFile, indent=2 )
    outFile.close()

