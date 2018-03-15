from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName      = 'Analysis'
config.JobType.maxMemoryMB     = 3500
config.JobType.priority        = 2
config.Data.splitting          = 'FileBased'
config.Data.unitsPerJob        = 5
#config.Data.totalUnits         = 10 # For small tests

config.Site.storageSite        = 'T2_US_Wisconsin'
config.Site.blacklist          = ['T2_BE_IIHE',]
#config.Site.whitelist          = []

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()
#dataMap['ggH125'] = '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM'
#dataMap['qqH125'] = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM'
#dataMap['DYJets'] = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v7-v1/MINIAODSIM'

dataMap['DYJetsExt1v1'] = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM'
dataMap['DYJetsExt1v2'] = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10_ext1-v2/MINIAODSIM'
dataMap['dataSingleMuonBv1'] = '/SingleMuon/Run2017B-PromptReco-v1/MINIAOD'
dataMap['dataSingleMuonBv2'] = '/SingleMuon/Run2017B-PromptReco-v2/MINIAOD'
dataMap['dataSingleMuonCv1'] = '/SingleMuon/Run2017C-PromptReco-v1/MINIAOD'
dataMap['dataSingleMuonCv2'] = '/SingleMuon/Run2017C-PromptReco-v2/MINIAOD'
dataMap['dataSingleMuonCv3'] = '/SingleMuon/Run2017C-PromptReco-v3/MINIAOD'
dataMap['dataSingleMuonDv1'] = '/SingleMuon/Run2017D-PromptReco-v1/MINIAOD'
dataMap['dataSingleMuonEv1'] = '/SingleMuon/Run2017E-PromptReco-v1/MINIAOD'
dataMap['dataSingleMuonFv1'] = '/SingleMuon/Run2017F-PromptReco-v1/MINIAOD'

# dasgoclient --query="dataset dataset=/SingleMuon/Run2017*-PromptReco-v*/MINIAOD" | sort

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
        if 'data' in k :
            # JSON files: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis
            config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt' # 41.15 /fb
            config.JobType.psetName        = 'tauHLT_forPromptRecoData_cfg.py'
            config.Data.unitsPerJob        = 5
        else :
            config.Data.unitsPerJob        = 2
            config.JobType.psetName        = 'tauHLT_forMiniAODSIM_cfg.py'
        config.General.requestName = '%s_nov28forSyncV1' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = v
        print 'submitting config:'
        print config
        submit(config)

