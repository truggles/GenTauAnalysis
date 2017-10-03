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
#config.Site.blacklist          = ['T1_US_FNAL']
#config.Site.whitelist          = []

config.User.voGroup            = 'uscms'

dataMap = {
    'dataSingleMuonBv1' : '/SingleMuon/Run2017B-PromptReco-v1/MINIAOD',
    'dataSingleMuonBv2' : '/SingleMuon/Run2017B-PromptReco-v2/MINIAOD',
    'dataSingleMuonCv1' : '/SingleMuon/Run2017C-PromptReco-v1/MINIAOD',
    'dataSingleMuonCv2' : '/SingleMuon/Run2017C-PromptReco-v2/MINIAOD',
    'dataSingleMuonCv3' : '/SingleMuon/Run2017C-PromptReco-v3/MINIAOD',
    'dataSingleMuonDv1' : '/SingleMuon/Run2017D-PromptReco-v1/MINIAOD',
    'dataSingleMuonEv1' : '/SingleMuon/Run2017E-PromptReco-v1/MINIAOD',
    'ggH125' : '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
    'qqH125' : '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIISummer17MiniAOD-92X_upgrade2017_realistic_v10-v2/MINIAODSIM',
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
        if 'data' in k :
            # JSON files: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2017Analysis
            config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-302663_13TeV_PromptReco_Collisions17_JSON.txt' # 18.26/fb
            config.JobType.psetName        = 'tauHLT_forPromptRecoData_cfg.py'
        else :
            config.JobType.psetName        = 'tauHLT_forMiniAODSIM_cfg.py'
        config.General.requestName = '%s_oct03v1' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = v
        print 'submitting config:'
        print config
        submit(config)

