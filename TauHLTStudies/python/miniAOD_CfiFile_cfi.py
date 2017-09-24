import FWCore.ParameterSet.Config as cms

tauMiniAODHLTStudies = cms.EDAnalyzer("TauHLTStudiesMiniAODAnalyzer",
    hadronSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    tauElectronSrc = cms.InputTag("tauGenJetsSelectorElectrons"),
    tauMuonSrc = cms.InputTag("tauGenJetsSelectorMuons"),
    puSrc = cms.InputTag("addPileupInfo"),
    tauSrc = cms.InputTag("slimmedTaus","","RECO"),
    muonSrc = cms.InputTag("slimmedMuons","","RECO"),
    electronSrc = cms.InputTag("slimmedElectrons","","RECO"),
    jetSrc = cms.InputTag("slimmedJets"),
    metSrc = cms.InputTag("slimmedMETs","","RECO"),
    pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices"),
    triggerSrc = cms.InputTag("TriggerResults","","HLT"),
    triggerObjectsSrc = cms.InputTag("slimmedPatTrigger"),
    stage2TauSrc = cms.InputTag("caloStage2Digis","Tau","RECO"),
    genSrc = cms.InputTag("genParticles","","HLT"),
)
