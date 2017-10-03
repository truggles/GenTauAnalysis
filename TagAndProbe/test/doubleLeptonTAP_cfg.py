
import FWCore.ParameterSet.Config as cms

process = cms.Process("doubleLepTAP")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/DoubleMuon/MINIAOD/03Feb2017-v1/100000/00182C13-EEEA-E611-8897-001E675A6C2A.root',
#'root://cms-xrd-global.cern.ch//store/data/Run2016G/DoubleEG/MINIAOD/03Feb2017-v1/100000/002F14FF-D0EA-E611-952E-008CFA197AF4.root',
#'root://cms-xrd-global.cern.ch//store/mc/RunIISummer16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext2-v1/100000/00099D43-77ED-E611-8889-5065F381E1A1.root',
    )
)


process.load("THRAnalysis.TagAndProbe.doubleLepTAP_cfi")
#process.DoubleLeptonTAPStudies.isData = cms.untracked.bool(True)
#process.DoubleLeptonTAPStudies.doDoubleMu = cms.untracked.bool(True)
#process.DoubleLeptonTAPStudies.doDoubleE = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
        fileName = cms.string('outfile.root')
    )


process.p = cms.Path(
            #process.hltFilter*
            process.DoubleLeptonTAPStudies)

#print process.dumpPython()

