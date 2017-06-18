

import FWCore.ParameterSet.Config as cms

def setSourceFiles( process ) :

    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            'root://eoscms.cern.ch//eos/cms/store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/AODSIM/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/0018A939-3D2F-E711-9DA6-549F3525C318.root',
            #'root://eoscms.cern.ch//eos/cms/store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/021FA4A0-6D11-E711-AD9D-FA163ED9BE5A.root', # Defaul ones child
        ),
        secondaryFileNames = cms.untracked.vstring(
            #'root://eoscms.cern.ch//eos/cms/store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/BE521173-FD10-E711-A3FE-02163E0176C2.root', # Default one
            'root://eoscms.cern.ch//eos/cms/store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/00095E3E-382F-E711-AE89-008CFA111200.root',
        )
    )

    return process

def customizeInputFiles( _customInfo ) :

    _customInfo['inputFile' ]=  [
            #'root://eoscms.cern.ch//eos/cms/store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/BE521173-FD10-E711-A3FE-02163E0176C2.root']
            'root://eoscms.cern.ch//eos/cms/store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/00095E3E-382F-E711-AE89-008CFA111200.root']

    return _customInfo


def buildGenTausAndMore( process ) :

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

    return process


def setOutputFile( process) :
    process.Out = cms.OutputModule( "PoolOutputModule",
        fileName = cms.untracked.string( "tt_test_secondary.root" ),
        fastCloning = cms.untracked.bool( False ),
        outputCommands = cms.untracked.vstring(
                        "drop *",
                        "keep *_TriggerResults_*_MYHLT",
                        "keep *_hltGtStage2Digis_Tau_MYHLT",
                        "keep *_hltGtStage2Digis_Muon_MYHLT",
                        "keep *_addPileupInfo_*_*",
                        "keep *_hpsPFTauProducer_*_RECO",
                        "keep *_muons_*_RECO",
                        "keep *_offlinePrimaryVertices_*_*",
                        "keep *_selectedPatTrigger_*_*",
                        "keep *_gtStage2Digis_Tau_RECO",
                        "keep *_genParticles_*_HLT",
                        )
    )
    
    process.end = cms.EndPath( process.Out )

    return process
