
import FWCore.ParameterSet.Config as cms

process = cms.Process("AnalyzeRunBData")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
)


process.load("THRAnalysis.TauHLTStudies.miniAOD_CfiFile_cfi")
process.tauMiniAODHLTStudies.isData = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
        fileName = cms.string("outpu.root")
    )


process.p = cms.Path(
            #process.hltFilter*
            process.tauMiniAODHLTStudies)

#print process.dumpPython()

