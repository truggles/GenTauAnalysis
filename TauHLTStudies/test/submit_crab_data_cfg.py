from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName      = 'Analysis'
config.JobType.maxMemoryMB     = 2500
config.JobType.priority        = 2
config.Data.splitting          = 'FileBased'
config.Data.unitsPerJob        = 5
#config.Data.totalUnits         = 10 # For small tests

# JSON files:
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/DCSOnly/json_DCSONLY.txt'
#config.Data.runRange = '297179,297176,297175,297114,297113,297101,297100,297099,297057,297056,297050' # My original runs from June 27 work
config.Data.runRange = '297474,297469,297433,297432,297430,297429,297425,297411,297359,297308,297296,297293,297292,297293,297296,297308,297359,297411,297424,297425,297426,297429,297430,297431,297432,297433,297434,297435,297467,297468,297469,297474,297483,297484,297485,297486,297488,297503,297504,297505,297557,297558,297562,297563,297598,297603,297606,297620,297656,297659,297660,297665,297666,297670,297674,297675,297678,297722,297723' # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis case-2 - HV=200 7 July 2017

config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T1_US_FNAL']
#config.Site.whitelist          = []

config.User.voGroup            = 'uscms'

dataMap = {
    'tau' : '/Tau/Run2017B-PromptReco-v1/MINIAOD',
    'muon' : '/SingleMuon/Run2017B-PromptReco-v1/MINIAOD',
}

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    datasets = OrderedDict()
   
    base = os.getenv("CMSSW_BASE")
    print "Base: ",base
    for k, v in dataMap.iteritems() :
        config.General.requestName = 'data_%s_july09' % k
        config.JobType.psetName        = 'crab_%s_MiniAOD_cfg.py' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = v
        print 'submitting config:'
        print config
        submit(config)


