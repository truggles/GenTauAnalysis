from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3ConfigurationFile

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName      = 'Analysis'
config.JobType.maxMemoryMB     = 3500
config.JobType.priority        = 2
# Testing EventAwareLumiBased
config.Data.splitting      = 'FileBased'
config.Data.unitsPerJob    = 5
#config.Data.totalUnits         = 100 # For small tests
config.Data.publication        = True


config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T2_BE_IIHE',] # Needed to remove this to process the VBF H125 sample & HLTPhysics, & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
### FOR EFFICIENCY & OTHER MC STUDIES ###
# dasgoclient --query="dataset dataset=/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/*"
# dasgoclient --query="dataset dataset=/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/*"
# dasgoclient --query="dataset dataset=/*TauTau*/RunIISummer17*-NZSFlatPU28to62_*_upgrade2017_realistic*/*"

dataMap[ 'SingleMuon_2018A-v1' ] = '/SingleMuon/Run2018A-PromptReco-v1/MINIAOD'
dataMap[ 'SingleMuon_2018A-v2' ] = '/SingleMuon/Run2018A-PromptReco-v2/MINIAOD'

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
    for k in dataMap.keys() :
        config.General.requestName = '%s_hps_1011_may29_prompReco_DCSOnly_v1' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = dataMap[ k ]
        config.JobType.maxMemoryMB = 3500
        config.JobType.psetName    = 'crab_prompt_hps_DATA-miniAOD_cfg.py'
        config.Data.lumiMask       = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'
        print 'submitting config:'
        print config
        submit(config)


