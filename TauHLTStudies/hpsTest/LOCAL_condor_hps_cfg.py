
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing


process = cms.Process("LOCALHPS")

process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_hps_1003_april09_test_v1/180409_072416/0000/output_8.root'
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_hps_1003_april09_test_v2/180409_152132/0000/output_9.root'
        #'file:root://cmsxrootd.fnal.gov//store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_april09_v3/180409_195545/0003/output_3000.root'
        #'file:root://cmsxrootd.fnal.gov//store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may01_v1/180501_070223/0000/output_1.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may01_v1/180501_070223/0000/output_4.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_1.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_10.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_11.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_13.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_14.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_18.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_22.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_24.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_3.root',
        #'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_4.root',
        'file:/hdfs/store/user/truggles/VBFHToTauTau_M125_13TeV_powheg_pythia8/qqH125_L2p5_1003_may02_v1/180502_130922/0000/output_8.root',
    )
)


# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '92X_upgrade2017_realistic_v10')
process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_TSG_2017_12_19_13_49_40')

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


# Try to redo L2p5 iso calculation offline
process.load("THRAnalysis.TauHLTStudies.hltL2TauPixelIsoTagProducer_cfi")
process.load("THRAnalysis.TauHLTStudies.newHltL2TauPixelIsoTagProducer_cfi")
process.new2HltL2TauPixelIsoTagProducer = process.newHltL2TauPixelIsoTagProducer.clone()
process.new2HltL2TauPixelIsoTagProducer.TrackPVMaxDZ = cms.double( 0.005 )


process.load("THRAnalysis.TauHLTStudies.hps_CfiFile_cfi")
process.hpsTauHLTStudies.isData = cms.untracked.bool(False)
#process.hpsTauHLTStudies.verbose = cms.untracked.bool(True)
#process.hpsTauHLTStudies.requireMediumTauMVA = cms.untracked.bool(True)


process.TFileService = cms.Service("TFileService",
        fileName = cms.string("outputFileName.root")
    )


process.p = cms.Path(
            #process.hltFilter*
            process.egmGsfElectronIDSequence*
            process.tauGenJets*
            process.tauGenJetsSelectorAllHadrons*
            process.tauGenJetsSelectorElectrons*
            process.tauGenJetsSelectorMuons*
            process.hltL2TauPixelIsoTagProducer*
            process.newHltL2TauPixelIsoTagProducer*
            process.new2HltL2TauPixelIsoTagProducer*
            process.hpsTauHLTStudies)

#print process.dumpPython()

