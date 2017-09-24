import FWCore.ParameterSet.Config as cms

process = cms.Process("TagAndProbe")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:ttbar10evtsAOD.root',
    )
    #),
    #secondaryFileNames = cms.untracked.vstring(
    #    'file:ttbar10evtsMYHLT.root',
    #)
)



#import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
#process.hltFilter = hlt.triggerResultsFilter.clone( 
#        hltResults = cms.InputTag( "TriggerResults","","HLT2"), 
#        triggerConditions = ( 'HLT_IsoMu20_v*', 'HLT_IsoMu22_v*',\
#            'HLT_IsoMu24_v*', 'HLT_IsoMu27_v*'),
#        l1tResults = '', 
#        throw = False 
#        )



process.tauGenJets = cms.EDProducer(
    "TauGenJetProducer",
    GenParticles =  cms.InputTag('genParticles'),
    includeNeutrinos = cms.bool( False ),
    verbose = cms.untracked.bool( False )
    )



process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('oneProng0Pi0', 
                          'oneProng1Pi0', 
                          'oneProng2Pi0', 
                          'oneProngOther',
                          'threeProng0Pi0', 
                          'threeProng1Pi0', 
                          'threeProngOther', 
                          'rare'),
     filter = cms.bool(False)
)



process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('electron'), 
     filter = cms.bool(False)
)



process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('muon'), 
     filter = cms.bool(False)
)




process.load("THRAnalysis.TauHLTStudies.CfiFile_cfi")




process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('ttree.root')
                                   )



process.p = cms.Path(
            #process.hltFilter*
            process.tauGenJets*
            process.tauGenJetsSelectorAllHadrons*
            process.tauGenJetsSelectorElectrons*
            process.tauGenJetsSelectorMuons*
            process.tauHLTStudies)

#process.e = cms.EndPath(process.out)

#print process.dumpPython()



