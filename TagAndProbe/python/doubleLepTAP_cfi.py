import FWCore.ParameterSet.Config as cms

DoubleLeptonTAPStudies = cms.EDAnalyzer("DoubleLeptonTAP",
    puSrc = cms.InputTag("slimmedAddPileupInfo"),
    tauSrc = cms.InputTag("slimmedTaus"),
    muonSrc = cms.InputTag("slimmedMuons"),
    electronSrc = cms.InputTag("slimmedElectrons"),
    jetSrc = cms.InputTag("slimmedJets"),
    metSrc = cms.InputTag("slimmedMETs"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    triggerSrc = cms.InputTag("TriggerResults","","HLT"),
    triggerObjectsSrc = cms.InputTag("selectedPatTrigger"),
)
