
import FWCore.ParameterSet.Config as cms

process = cms.Process("LOCALHPS")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer17MiniAOD-NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/MINIAODSIM"
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring()
    #fileNames = cms.untracked.vstring(
    #    #'file:root://cmsxrootd.fnal.gov///store/mc/RunIISummer17MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/NZSFlatPU28to62_92X_upgrade2017_realistic_v10_ext1-v1/80000/680BCA4A-1208-E811-9684-0025905A60D2.root',
    #    'file:root://cmsxrootd.fnal.gov///store/mc/RunIIFall17MiniAODv2/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/20000/B4F852F4-8244-E811-AE69-B499BAAC0270.root',
    #)
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '101X_mc2017_realistic_TSG_2018_04_09_20_43_53') # 92X MC in 10_1_7
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v13') # 94X MC 94X_mc2017_realistic_v13


#
# Set up electron ID (VID framework)
#

from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
dataFormat = DataFormat.MiniAOD

switchOnVIDElectronIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_GeneralPurpose_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring16_HZZ_V1_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)



### Gen Taus ###
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



process.load("THRAnalysis.TauHLTStudies.hps_CfiFile_cfi")
#process.hpsTauHLTStudies.verbose = cms.untracked.bool(True)

#process.hpsTauHLTStudies.doMuTau = cms.untracked.bool(True)
#process.hpsTauHLTStudies.doETau = cms.untracked.bool(True)
process.hpsTauHLTStudies.doTauTau = cms.untracked.bool(True)

process.hpsTauHLTStudies.requireMediumTauMVA = cms.untracked.bool(True)

process.hpsTauHLTStudies.doTriggerMatching = cms.untracked.bool(True)
process.hpsTauHLTStudies.triggerSrc = cms.InputTag("TriggerResults","","HLT")
process.hpsTauHLTStudies.triggerObjectsSrc = cms.InputTag("slimmedPatTrigger","","PAT")


process.TFileService = cms.Service("TFileService",
        fileName = cms.string('outfile.root')
)



process.p = cms.Path(
            process.egmGsfElectronIDSequence*
            process.tauGenJets*
            process.tauGenJetsSelectorAllHadrons*
            process.tauGenJetsSelectorElectrons*
            process.tauGenJetsSelectorMuons*
            process.hpsTauHLTStudies
)

#print process.dumpPython()

