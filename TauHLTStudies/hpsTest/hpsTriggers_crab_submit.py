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
#config.Data.splitting          = 'FileBased'
#config.Data.unitsPerJob        = 1
# Testing EventAwareLumiBased
config.Data.splitting          = 'EventAwareLumiBased'
config.Data.unitsPerJob        = 3000 # events / job when using EventAwareLumiBased
#config.Data.totalUnits         = 10 # For small tests
config.JobType.numCores        = 4

config.Site.storageSite        = 'T2_US_Wisconsin'
config.Site.blacklist          = ['T2_BE_IIHE',]
config.Site.whitelist          = ['T2_US_Wisconsin',]

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
#dataMap['qqH125'] = {
#        'child' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
#        'grandparent' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW',
#    }
dataMap['ggH125'] = {
        'child' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
        'grandparent' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW',
    }

# dasgoclient --query="dataset dataset=/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/*"
# dasgoclient --query="dataset dataset=/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/*"

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
        #config.JobType.psetName        = 'hps_test_cfg.py'
        config.JobType.psetName        = 'hps_cfg_strebler_v13_hlt.py'
        config.General.requestName = '%s_jan14_hps_v2' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = dataMap[ k ][ 'child' ]
        config.Data.secondaryInputDataset = dataMap[ k ][ 'grandparent' ]
        print 'submitting config:'
        print config
        submit(config)

