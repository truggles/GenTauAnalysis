import FWCore.ParameterSet.Config as cms

# Directly from HLT cfg
# Used to rerun and try to duplicate results offline for quick tests
newHltL2TauPixelIsoTagProducer = cms.EDProducer( "NewL2TauPixelIsoTagProducer",
    TrackSrc = cms.InputTag( "" ),
    BeamSpotSrc = cms.InputTag( "hltOnlineBeamSpot","","MYHLT" ),
    TrackMaxNChi2 = cms.double( 1000.0 ),
    TrackMinNHits = cms.int32( 3 ),
    TrackMinPt = cms.double( 0.9 ),
    IsoConeMax = cms.double( 0.4 ),
    TrackPVMaxDZ = cms.double( 99.9 ),
    IsoConeMin = cms.double( 0.15 ),
    VertexSrc = cms.InputTag( "hltPixelVerticesRegL1TauSeeded","","MYHLT" ),
    #JetSrc = cms.InputTag( "hltL2TausForPixelIsolationL1TauSeeded","","MYHLT" ),
    JetSrc = cms.InputTag( "hltL2TauJetsL1TauSeeded","","MYHLT" ),
    TrackMaxDxy = cms.double( 0.2 ),
    MaxNumberPV = cms.int32( 1 )
)
