

import FWCore.ParameterSet.Config as cms

def getCrabSecondaryFiles( child ) :
    import json, os
    base = os.getenv("CMSSW_BASE")
    jFile = open(base+'/src/THRAnalysis/TauHLTStudies/data/aod_map.json')
    j = json.load( jFile )
    parents = j[ child ]
    jFile.close()
    p = cms.untracked.vstring( parents )
    return p

def setCrabSourceFiles( process ) :
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(),
        secondaryFileNames = cms.untracked.vstring()
    )

    return process

def setSourceFiles( process ) :

    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/021FA4A0-6D11-E711-AD9D-FA163ED9BE5A.root', # Defaul ones child
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/AODSIM/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/0018A939-3D2F-E711-9DA6-549F3525C318.root',
        ),
        secondaryFileNames = cms.untracked.vstring(
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/AE8721E0-5F11-E711-BEFF-FA163E35EC22.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/C6FCF1D8-5911-E711-93BA-FA163E613555.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/4CA177D8-5411-E711-8EFE-FA163E4FCBAC.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/76979FAA-6211-E711-9BB7-FA163E30EA14.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/AEDFC268-5B11-E711-8A12-02163E013E78.root', 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1C5A314D-2F2F-E711-BCFF-549F3525DDFC.root', 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1E200A0E-2D2F-E711-9D06-782BCB53A3A6.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/24EA3BFD-2C2F-E711-9AF8-001C23C0B673.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/5EA04778-2E2F-E711-A95B-141877410B85.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/722A19C7-242F-E711-B6C5-1866DAEEB358.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C61F0036-302F-E711-91AC-1866DAEB3370.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C8A77762-2F2F-E711-A824-549F3525C318.root', 
        )
    )

    return process


def customizeInput( _customInfo ) :

    # This is the input to the reHLT process, so is actuall the "secondary" files from above
    _customInfo['inputFile' ]=  [
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/AE8721E0-5F11-E711-BEFF-FA163E35EC22.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/C6FCF1D8-5911-E711-93BA-FA163E613555.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/4CA177D8-5411-E711-8EFE-FA163E4FCBAC.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/76979FAA-6211-E711-9BB7-FA163E30EA14.root',
            'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/AEDFC268-5B11-E711-8A12-02163E013E78.root' 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1C5A314D-2F2F-E711-BCFF-549F3525DDFC.root', 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1E200A0E-2D2F-E711-9D06-782BCB53A3A6.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/24EA3BFD-2C2F-E711-9AF8-001C23C0B673.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/5EA04778-2E2F-E711-A95B-141877410B85.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/722A19C7-242F-E711-B6C5-1866DAEEB358.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C61F0036-302F-E711-91AC-1866DAEB3370.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C8A77762-2F2F-E711-A824-549F3525C318.root'
            ]
    _customInfo['maxEvents' ]=  200

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
        fileName = cms.untracked.string( "output.root" ),
        fastCloning = cms.untracked.bool( False ),
        dataset = cms.untracked.PSet(
            filterName = cms.untracked.string(''),
            dataTier = cms.untracked.string('GEN-SIM-RAW-AOD')
        ),
        outputCommands = cms.untracked.vstring(
                        "drop *",
                        "keep *_TriggerResults_*_MYHLT",
                        "keep *_hltGtStage2Digis_Tau_MYHLT",
                        "keep *_hltGtStage2Digis_Muon_MYHLT",
                        "keep *_addPileupInfo_*_*",
                        "keep recoPFTaus_hpsPFTauProducer__RECO",
                        "keep recoPFTauDiscriminator_*_*_RECO",
                        "keep *_hpsPFTauTransverseImpactParameters__RECO",
                        "keep recoMuons_muons__RECO",
                        "keep *_offlinePrimaryVertices_*_*",
                        #"keep *_selectedPatTrigger_*_*", # Not in AODSIM
                        "keep *_gtStage2Digis_Tau_RECO",
                        "keep recoGenParticles_genParticles_*_HLT",
                        )
    )
    
    process.end = cms.EndPath( process.Out )

    return process


