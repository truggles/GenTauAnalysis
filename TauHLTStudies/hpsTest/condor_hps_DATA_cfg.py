
import FWCore.ParameterSet.Config as cms

process = cms.Process("LOCALHPS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring($inputFileNames)
    #fileNames = cms.untracked.vstring(
    #    'file:/hdfs/store/user/truggles/EphemeralHLTPhysics1/hltPhysicsV1_jan21_hps_Menu_V6_rate_v3xx//180121_170952/0000/output_99.root')
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')





process.load("THRAnalysis.TauHLTStudies.hps_CfiFile_cfi")
#process.hpsTauHLTStudies.verbose = cms.untracked.bool(True)
process.hpsTauHLTStudies.isRAW = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
        fileName = cms.string("$outputFileName")
        #fileName = cms.string("outputFileName.root")
    )


process.p = cms.Path(
            #process.hltFilter*
            process.hpsTauHLTStudies)

#print process.dumpPython()

