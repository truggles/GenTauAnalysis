
import FWCore.ParameterSet.Config as cms

process = cms.Process("AnalyzeRunBData")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2800000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )
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
process = load_files( process, 'SingleMuon', 'MINIAOD' )
#process = load_files( process, 'Tau', 'MINIAOD' )


process.load("THRAnalysis.TauHLTStudies.miniAOD_CfiFile_cfi")
process.tauMiniAODHLTStudies.isData = cms.untracked.bool(True)
#process.tauMiniAODHLTStudies.doTauTau = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('ttree.root')
                                   )


process.p = cms.Path(
            #process.hltFilter*
            process.tauMiniAODHLTStudies)

#process.TFileService.fileName = cms.string('runB_tau2_data_ttree_miniaod.root')
process.TFileService.fileName = cms.string('runB_singleMuon2_data_ttree_miniaod.root')
#print process.dumpPython()

