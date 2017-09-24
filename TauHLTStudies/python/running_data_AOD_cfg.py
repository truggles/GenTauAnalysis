
import FWCore.ParameterSet.Config as cms

process = cms.Process("AnalyzeRunBData")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2800000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    # Load files below with load_files
    fileNames = cms.untracked.vstring(
        #"root://cms-xrd-global.cern.ch///store/data/Run2017B/SingleMuon/MINIAOD/PromptReco-v1/000/297/179/00000/685BFA09-EC58-E711-A140-02163E019CF3.root"
    )
)

# Load all files HERE
from THRAnalysis.TauHLTStudies.load_files import load_files
process = load_files( process, 'SingleMuon', 'AOD' )


from THRAnalysis.TauHLTStudies.tauHLTStudies import simpleDataFromRAW
process = simpleDataFromRAW( process )
process.tauHLTStudies.isData = cms.untracked.bool(True)
process.tauHLTStudies.triggerSrc = cms.InputTag("TriggerResults","","HLT")
process.tauHLTStudies.stage2TauSrc = cms.InputTag("caloStage2Digis","Tau","RECO")

process.TFileService.fileName = cms.string('runB_singleM_data_ttree_tmp.root')
#print process.dumpPython()

