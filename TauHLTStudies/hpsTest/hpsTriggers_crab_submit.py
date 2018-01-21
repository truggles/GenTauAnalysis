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
config.Data.splitting          = 'EventAwareLumiBased'
config.Data.unitsPerJob        = 3000 # events / job when using EventAwareLumiBased
#config.Data.totalUnits         = 10 # For small tests
config.JobType.numCores        = 4

config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T2_BE_IIHE',] # Needed to remove this to process the VBF H125 sample & HLTPhysics
config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
### FOR EFFICIENCY & OTHER MC STUDIES ###
#dataMap['qqH125'] = {
#        'child' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
#        'grandparent' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW',
#    }
#dataMap['ggH125'] = {
#        'child' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
#        'grandparent' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW',
#    }

### FOR RATE STUDIES ###
dataMap['hltPhysicsV1'] = {
        'child' : '/EphemeralHLTPhysics1/Run2017F-PromptReco-v1/MINIAOD',
        'grandparent' : '/EphemeralHLTPhysics1/Run2017F-v1/RAW',
    }
#dataMap['hltPhysicsV2'] = {
#        'child' : '/EphemeralHLTPhysics2/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics2/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV3'] = {
#        'child' : '/EphemeralHLTPhysics3/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics3/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV4'] = {
#        'child' : '/EphemeralHLTPhysics4/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics4/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV5'] = {
#        'child' : '/EphemeralHLTPhysics5/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics5/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV6'] = {
#        'child' : '/EphemeralHLTPhysics6/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics6/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV7'] = {
#        'child' : '/EphemeralHLTPhysics7/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics7/Run2017F-v1/RAW',
#    }
#dataMap['hltPhysicsV8'] = {
#        'child' : '/EphemeralHLTPhysics8/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics8/Run2017F-v1/RAW',
#    }

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
        #config.JobType.psetName        = 'hps_cfg_strebler_v13_hlt.py'
        config.JobType.psetName        = 'hps_cfg_truggles_V6_hlt.py'
        config.General.requestName = '%s_jan21_hps_Menu_V6_rate_v3' % k
        config.Data.outputDatasetTag   = config.General.requestName
        if not 'hltPhysics' in k :
            config.Data.inputDataset = dataMap[ k ][ 'child' ]
            config.Data.secondaryInputDataset = dataMap[ k ][ 'grandparent' ]
        if 'hltPhysics' in k :
            config.Data.inputDataset = dataMap[ k ][ 'grandparent' ]
            config.JobType.maxMemoryMB = 2500
            config.Data.splitting      = 'FileBased'
            config.Data.unitsPerJob    = 12
            config.JobType.psetName    = 'hps_cfg_truggles_V6_hlt_DATA.py'
            config.Data.lumiMask       = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
        print 'submitting config:'
        print config
        submit(config)

