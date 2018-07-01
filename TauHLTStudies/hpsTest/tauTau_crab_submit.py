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
config.Data.publication        = True
#config.Data.allowNonValidInputDataset = True # Temporary for DYJets M-50


config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T2_BE_IIHE',] # Needed to remove this to process the VBF H125 sample & HLTPhysics, & DYJets
#config.Site.blacklist          = ['T2_BE_UCL',] # Needed for DYJets?
config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
### FOR EFFICIENCY & OTHER MC STUDIES ###
#dataMap['qqH125'] = {
#        'child' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
#        'grandparent' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW',
#    }
##dataMap['ggH125'] = {
##        'child' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
##        'grandparent' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW',
##    }
#dataMap['DYJets'] = {
#        'child' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM',
#        'grandparent' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/GEN-SIM-RAW',
#    }
dataMap['DYJetsMCv2'] = {
        'child' : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
    }
dataMap['DYJetsMCv2_ext1'] = {
        'child' : '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM',
    }

#/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM
#/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/MINIAODSIM


# dasgoclient --query="dataset dataset=/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/*"
# dasgoclient --query="dataset dataset=/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17*-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/*"
# dasgoclient --query="dataset dataset=/*TauTau*/RunIISummer17*-NZSFlatPU28to62_*_upgrade2017_realistic*/*"

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
        config.General.requestName = '%s_tauTau_10_1_7_94X_june30_v2' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.JobType.psetName        = 'zLOCAL_crab_prompt_hps_MC-miniAOD_cfg.py'
        config.Data.inputDataset = dataMap[ k ][ 'child' ]
        config.JobType.maxMemoryMB     = 2500
        config.Data.splitting      = 'FileBased'
        config.Data.unitsPerJob    = 20
        print 'submitting config:'
        print config
        submit(config)


