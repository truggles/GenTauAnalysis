
import FWCore.ParameterSet.Config as cms

process = cms.Process("TagAndProbe")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:tt_test_secondary3.root',
    )
)


from THRAnalysis.TauHLTStudies.tauHLTStudies import buildGenTausAndMore
process = buildGenTausAndMore( process )

#print process.dumpPython()

