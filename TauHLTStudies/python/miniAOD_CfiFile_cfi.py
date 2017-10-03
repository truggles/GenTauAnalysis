import FWCore.ParameterSet.Config as cms

tauMiniAODHLTStudies = cms.EDAnalyzer("TauHLTStudiesMiniAODAnalyzer",
    hadronSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    tauElectronSrc = cms.InputTag("tauGenJetsSelectorElectrons"),
    tauMuonSrc = cms.InputTag("tauGenJetsSelectorMuons"),
    puSrc = cms.InputTag("slimmedAddPileupInfo"),
    tauSrc = cms.InputTag("slimmedTaus"),
    muonSrc = cms.InputTag("slimmedMuons"),
    electronSrc = cms.InputTag("slimmedElectrons"),
    jetSrc = cms.InputTag("slimmedJets"),
    metSrc = cms.InputTag("slimmedMETs"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    triggerSrc = cms.InputTag("TriggerResults","","HLT"),
    triggerObjectsSrc = cms.InputTag("slimmedPatTrigger"),
    stage2TauSrc = cms.InputTag("caloStage2Digis","Tau","RECO"),
    genSrc = cms.InputTag("prunedGenParticles","","PAT"),
)
