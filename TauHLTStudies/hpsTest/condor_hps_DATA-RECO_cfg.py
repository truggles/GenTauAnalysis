
import FWCore.ParameterSet.Config as cms

process = cms.Process("LOCALHPS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring($inputFileNames)
    #fileNames = cms.untracked.vstring(
    #    'file:/hdfs/store/user/truggles/SingleMuon/DataSingleMuonF_hps_10x_feb17_finalCfg/180217_103918/0000/output_10.root')
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '101X_dataRun2_HLT_v7')


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


process.TFileService = cms.Service("TFileService",
        fileName = cms.string("$outputFileName")
        #fileName = cms.string("outputFileName.root")
    )


process.p = cms.Path(
            #process.hltFilter*
            process.egmGsfElectronIDSequence*
            process.hpsTauHLTStudies)

#print process.dumpPython()

