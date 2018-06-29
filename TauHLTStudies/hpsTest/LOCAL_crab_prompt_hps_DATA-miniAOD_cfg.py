
import FWCore.ParameterSet.Config as cms

process = cms.Process("LOCALHPS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20000) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring()
    fileNames = cms.untracked.vstring(
        #'file:root://cmsxrootd.fnal.gov///store/data/Run2018A/SingleMuon/MINIAOD/PromptReco-v2/000/316/928/00000/2ECA847E-0D62-E811-A6ED-FA163EC42C83.root'
        #'file:root://cmsxrootd.fnal.gov///store/data/Run2018A/EGamma/MINIAOD/PromptReco-v2/000/316/455/00000/8248C195-205B-E811-A107-02163E017FBF.root'
        #'file:root://cmsxrootd.fnal.gov///store/data/Run2018B/EGamma/MINIAOD/PromptReco-v1/000/317/696/00000/FCEAC88F-8D70-E811-AB51-FA163EAF352F.root'
        #'file:root://cmsxrootd.fnal.gov///store/data/Run2018B/Tau/MINIAOD/PromptReco-v1/000/317/696/00000/56C2A8DF-7770-E811-A475-FA163EE835E3.root'

        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_1.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_10.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_100.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_101.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_102.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_103.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_104.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_105.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_106.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_107.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_108.root',
        'file:/hdfs/store/user/truggles/SingleMuon/SingleMuon_2018A-v1_hps_1011_may25_prompReco_DCSOnly_v4/180525_072119/0000/outfile_109.root',
    )
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_hlt_GRun')


#
# Set up electron ID (VID framework)
#

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)





process.load("THRAnalysis.TauHLTStudies.hps_CfiFile_cfi")
#process.hpsTauHLTStudies.verbose = cms.untracked.bool(True)
#process.hpsTauHLTStudies.isRAW = cms.untracked.bool(True)
process.hpsTauHLTStudies.isData = cms.untracked.bool(True)
process.hpsTauHLTStudies.doMuTau = cms.untracked.bool(True)
#process.hpsTauHLTStudies.doETau = cms.untracked.bool(True)
#process.hpsTauHLTStudies.doTauTau = cms.untracked.bool(True)
process.hpsTauHLTStudies.triggerSrc = cms.InputTag("TriggerResults","","HLT")
process.hpsTauHLTStudies.triggerObjectsSrc = cms.InputTag("slimmedPatTrigger","","RECO")


process.TFileService = cms.Service("TFileService",
        fileName = cms.string('outfile.root')
)



process.p = cms.Path(
            process.egmGsfElectronIDSequence*
            process.hpsTauHLTStudies
)

#print process.dumpPython()

