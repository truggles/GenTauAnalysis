import FWCore.ParameterSet.Config as cms

genMass = cms.EDAnalyzer('GenMassAnalyzer',
    puSrc = cms.InputTag('slimmedAddPileupInfo'),
    lheSrc = cms.InputTag('externalLHEProducer')
)
