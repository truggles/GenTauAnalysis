import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:/afs/cern.ch/work/t/truggles/Z_to_tautau/dyjets_76x.root'
        'root://eoscms//eos/cms/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/002ABFCA-A0B9-E511-B9BA-0CC47A57CD6A.root',
    )
)

process.tauGenJets = cms.EDProducer(
    "TauGenJetProducer",
    GenParticles =  cms.InputTag('prunedGenParticles'),
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

process.load("THRAnalysis.TagAndProbe.CfiFile_cfi")
#process.load("TagAndProbe.TagAndProbeAnalyzer.CfiFile_cfi")

process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('ttree.root')
                                   )


#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('myOutputFile.root')
#    ,outputCommands = cms.untracked.vstring('drop *',
#      #"keep *_myProducerLabel_*_*",
#      #"keep *_slimmedMuons_*_*",
#      "keep *_*_*_Demo",
#        )
#)

process.p = cms.Path(process.tauGenJets*
            process.tauGenJetsSelectorAllHadrons*
            process.tauGenJetsSelectorElectrons*
            process.tauGenJetsSelectorMuons*
            process.tagAndProbe)

#process.e = cms.EndPath(process.out)
