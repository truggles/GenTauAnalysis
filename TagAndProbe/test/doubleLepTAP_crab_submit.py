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
config.Data.unitsPerJob        = 10
#config.Data.totalUnits         = 10 # For small tests

config.Site.storageSite        = 'T2_US_Wisconsin'
#config.Site.blacklist          = ['T1_US_FNAL']
#config.Site.whitelist          = []

config.User.voGroup            = 'uscms'

dataMap = OrderedDict()

dataMap['DYJetsExt1'] = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM' # 477 files
dataMap['DYJetsExt2'] = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/MINIAODSIM' # 837 files
#
#dataMap['dataDoubleMuBv1'] = '/DoubleMuon/Run2016B-03Feb2017_ver1-v1/MINIAOD'
#dataMap['dataDoubleMuBv2'] = '/DoubleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD'
#dataMap['dataDoubleMuCv1'] = '/DoubleMuon/Run2016C-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleMuDv1'] = '/DoubleMuon/Run2016D-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleMuEv1'] = '/DoubleMuon/Run2016E-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleMuFv1'] = '/DoubleMuon/Run2016F-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleMuGv1'] = '/DoubleMuon/Run2016G-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleMuHv2'] = '/DoubleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD'
#dataMap['dataDoubleMuHv3'] = '/DoubleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD'
#
#dataMap['dataDoubleElecBv1'] = '/DoubleEG/Run2016B-03Feb2017_ver1-v1/MINIAOD'
#dataMap['dataDoubleElecBv2'] = '/DoubleEG/Run2016B-03Feb2017_ver2-v2/MINIAOD'
#dataMap['dataDoubleElecCv1'] = '/DoubleEG/Run2016C-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleElecDv1'] = '/DoubleEG/Run2016D-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleElecEv1'] = '/DoubleEG/Run2016E-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleElecFv1'] = '/DoubleEG/Run2016F-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleElecGv1'] = '/DoubleEG/Run2016G-03Feb2017-v1/MINIAOD'
#dataMap['dataDoubleElecHv2'] = '/DoubleEG/Run2016H-03Feb2017_ver2-v1/MINIAOD'
#dataMap['dataDoubleElecHv3'] = '/DoubleEG/Run2016H-03Feb2017_ver3-v1/MINIAOD'

dataMap['dataSingleMuonBv1'] = '/SingleMuon/Run2016B-03Feb2017_ver1-v1/MINIAOD'
dataMap['dataSingleMuonBv2'] = '/SingleMuon/Run2016B-03Feb2017_ver2-v2/MINIAOD'
dataMap['dataSingleMuonCv1'] = '/SingleMuon/Run2016C-03Feb2017-v1/MINIAOD'
dataMap['dataSingleMuonDv1'] = '/SingleMuon/Run2016D-03Feb2017-v1/MINIAOD'
dataMap['dataSingleMuonEv1'] = '/SingleMuon/Run2016E-03Feb2017-v1/MINIAOD'
dataMap['dataSingleMuonFv1'] = '/SingleMuon/Run2016F-03Feb2017-v1/MINIAOD'
dataMap['dataSingleMuonGv1'] = '/SingleMuon/Run2016G-03Feb2017-v1/MINIAOD'
dataMap['dataSingleMuonHv2'] = '/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD'
dataMap['dataSingleMuonHv3'] = '/SingleMuon/Run2016H-03Feb2017_ver3-v1/MINIAOD'

dataMap['dataSingleElectronBv1'] = '/SingleElectron/Run2016B-03Feb2017_ver1-v1/MINIAOD'
dataMap['dataSingleElectronBv2'] = '/SingleElectron/Run2016B-03Feb2017_ver2-v2/MINIAOD'
dataMap['dataSingleElectronCv1'] = '/SingleElectron/Run2016C-03Feb2017-v1/MINIAOD'
dataMap['dataSingleElectronDv1'] = '/SingleElectron/Run2016D-03Feb2017-v1/MINIAOD'
dataMap['dataSingleElectronEv1'] = '/SingleElectron/Run2016E-03Feb2017-v1/MINIAOD'
dataMap['dataSingleElectronFv1'] = '/SingleElectron/Run2016F-03Feb2017-v1/MINIAOD'
dataMap['dataSingleElectronGv1'] = '/SingleElectron/Run2016G-03Feb2017-v1/MINIAOD'
dataMap['dataSingleElectronHv2'] = '/SingleElectron/Run2016H-03Feb2017_ver2-v1/MINIAOD'
dataMap['dataSingleElectronHv3'] = '/SingleElectron/Run2016H-03Feb2017_ver3-v1/MINIAOD'


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
            # JSON files: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmV2016Analysis
            config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt' # 36.814 / fb 
            config.Data.unitsPerJob        = 20
        else :
            config.Data.unitsPerJob        = 4 # Some DY jobs had trouble, trying smaller size
        config.JobType.psetName        = 'doubleLeptonTAP_cfg.py'
        config.General.requestName = '%s_nov08' % k
        config.Data.outputDatasetTag   = config.General.requestName
        config.Data.inputDataset = v
        print 'submitting config:'
        print config
        submit(config)

