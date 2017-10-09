
import FWCore.ParameterSet.Config as cms

process = cms.Process("AnalyzeRunBData")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'root://cms-xrd-global.cern.ch//store/data/Run2017D/SingleMuon/MINIAOD/PromptReco-v1/000/302/663/00000/685AA9C4-469A-E711-86D9-02163E01A217.root',
    )
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v9')



process.load("THRAnalysis.TauHLTStudies.miniAOD_CfiFile_cfi")
process.tauMiniAODHLTStudies.isData = cms.untracked.bool(True)
process.tauMiniAODHLTStudies.requireMediumTauMVA = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
        fileName = cms.string('outfile.root')
    )


process.p = cms.Path(
            #process.hltFilter*
            process.tauMiniAODHLTStudies)

#print process.dumpPython()

