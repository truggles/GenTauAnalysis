
import FWCore.ParameterSet.Config as cms

process = cms.Process("AnalyzeRunBData")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    # Load files below with load_files
    fileNames = cms.untracked.vstring(
        #"root://cms-xrd-global.cern.ch///store/data/Run2017B/Tau/RAW/v1/000/297/179/00000/0A4B1BD5-9455-E711-99E1-02163E013649.root",
    )
)

# Load all files HERE
from THRAnalysis.TauHLTStudies.load_files import load_files
process = load_files( process, 'Tau', 'RAW' )


from THRAnalysis.TauHLTStudies.tauHLTStudies import simpleDataFromRAW
process = simpleDataFromRAW( process )
process.tauHLTStudies.isData = cms.untracked.bool(True)
process.tauHLTStudies.isRAW = cms.untracked.bool(True)
process.tauHLTStudies.triggerSrc = cms.InputTag("TriggerResults","","HLT")
process.tauHLTStudies.stage2TauSrc = cms.InputTag("hltGtStage2Digis","Tau","HLT")

process.TFileService.fileName = cms.string('runB_singleM_data_ttree.root')
#print process.dumpPython()

