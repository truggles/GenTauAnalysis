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

config.JobType.numCores        = 4

config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T2_BE_IIHE',] # Needed to remove this to process the VBF H125 sample & HLTPhysics, & DYJets
#config.Site.blacklist          = ['T2_BE_UCL',] # Needed for DYJets?
config.Site.ignoreGlobalBlacklist = True # Needed to add this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_US_Wisconsin',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets
#config.Site.whitelist          = ['T2_IT_Rome',] # Needed to remove this to process the VBF H125 sample & HLTPhysics & DYJets

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
### FOR EFFICIENCY & OTHER MC STUDIES ###
dataMap['qqH125'] = {
        'child' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
        'grandparent' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW',
    }
#dataMap['ggH125'] = {
#        'child' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
#        'grandparent' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_HIG06_92X_upgrade2017_realistic_v10-v2/GEN-SIM-RAW',
#    }
#dataMap['Zprime1500'] = {
#        'child' : '/ZprimeToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/MINIAODSIM',
#        'grandparent' : '/ZprimeToTauTau_M-1500_TuneCUETP8M1_13TeV-pythia8-tauola/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10-v1/GEN-SIM-RAW',
#    }
#dataMap['DataSingleMuonF'] = {
#        'child' : '/SingleMuon/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/SingleMuon/Run2017F-v1/RAW',
#    }
#dataMap['DataTauF'] = {
#        'child' : '/Tau/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/Tau/Run2017F-v1/RAW',
#    }

### FOR RATE STUDIES ###
#dataMap['hltPhysicsV1'] = {
#        'child' : '/EphemeralHLTPhysics1/Run2017F-PromptReco-v1/MINIAOD',
#        'grandparent' : '/EphemeralHLTPhysics1/Run2017F-v1/RAW',
#    }



#dataMap['DYJets'] = {
#        'child' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM',
#        'grandparent' : '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17DRStdmix-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/GEN-SIM-RAW',
#    }
#dataMap['DataSingleMuonBv1'] = {
#        'child' : '/SingleMuon/Run2018B-PromptReco-v1/MINIAOD',
#        'grandparent' : '/SingleMuon/Run2018B-v1/RAW',
#    }
##dataMap['DataSingleMuonAv1'] = {
##        'child' : '/SingleMuon/Run2018A-PromptReco-v1/MINIAOD',
##        'grandparent' : '/SingleMuon/Run2018A-v1/RAW',
##    }
##dataMap['DataSingleMuonAv2'] = {
##        'child' : '/SingleMuon/Run2018A-PromptReco-v2/MINIAOD',
##        'grandparent' : '/SingleMuon/Run2018A-v1/RAW',
##    }
#dataMap['DataSingleMuonAv3'] = {
#        'child' : '/SingleMuon/Run2018A-PromptReco-v3/MINIAOD',
#        'grandparent' : '/SingleMuon/Run2018A-v1/RAW',
#    }

#dataMap['DataMuTauSkimB'] = { # B and C not available on disk
#        'child' : '/SingleMuon/Run2018B-MuTau-PromptReco-v1/USER',
#    }


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
        config.General.requestName = '%s_ultraLegacy_10_1_10_oct29_v5' % k
        config.Data.outputDatasetTag   = config.General.requestName
        if not 'hltPhysics' in k and not 'Data' in k :
            config.JobType.psetName        = 'ultra_legacy_cfg_v2.py'
            config.Data.inputDataset = dataMap[ k ][ 'child' ]
            config.Data.secondaryInputDataset = dataMap[ k ][ 'grandparent' ]
            # ZPrime Test
            config.JobType.maxMemoryMB     = 2500
            config.Data.splitting          = 'EventAwareLumiBased'
            #config.Data.unitsPerJob        = 2000 # events / job when using EventAwareLumiBased
            config.Data.unitsPerJob        = 100 # events / job when using EventAwareLumiBased
            #config.Data.unitsPerJob        = 4000 # events / job when using EventAwareLumiBased
            config.Data.totalUnits         = 10000 # for tests
            #config.Data.totalUnits         = 4000000 # for tests
        elif 'hltPhysics' in k :
            config.Data.inputDataset = dataMap[ k ][ 'grandparent' ]
            config.JobType.maxMemoryMB = 2500
            config.Data.splitting      = 'FileBased'
            config.Data.unitsPerJob    = 5
            config.JobType.psetName    = 'hlt_DATA_10_1_7_6Paths.py'
            config.Data.lumiMask       = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
            #config.Data.totalUnits         = 45 # for small tests
        elif 'MuTauSkim' in k :
            config.Data.splitting          = 'FileBased'
            config.Data.unitsPerJob        = 1 # files when FileBased
            config.Data.inputDataset = dataMap[ k ][ 'child' ]
            config.JobType.maxMemoryMB = 2500
            config.JobType.psetName    = 'hlt_DATA_10_1_7_6Paths.py'
            config.Data.lumiMask       = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'
            config.Data.totalUnits         = 20 # Total files when FileBased
        elif 'Data' in k :
            config.Data.splitting          = 'EventAwareLumiBased'
            config.Data.unitsPerJob        = 3000 # events / job when using EventAwareLumiBased
            config.Data.inputDataset = dataMap[ k ][ 'child' ]
            config.Data.secondaryInputDataset = dataMap[ k ][ 'grandparent' ]
            config.JobType.maxMemoryMB = 3500
            config.JobType.psetName    = 'hlt_DATA_10_1_7_6Paths.py'
            config.Data.lumiMask       = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/DCSOnly/json_DCSONLY.txt'
            #config.Data.totalUnits         = 100000 # 1 mil was far too low for efficiency
            config.Data.totalUnits         = 25000000 # For small tests # events when using EventAwareLumiBased
        print 'submitting config:'
        print config
        submit(config)


