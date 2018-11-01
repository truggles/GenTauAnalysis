import FWCore.ParameterSet.Config as cms

genMass = 340

process = cms.Process("genMass")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:/afs/cern.ch/work/t/truggles/Z_to_tautau/dyjets_76x.root'
        #'root://eoscms//eos/cms/store/mc/RunIIFall15MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/70000/002ABFCA-A0B9-E511-B9BA-0CC47A57CD6A.root',
    )
)

if genMass == 220 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/8A590B2F-DDD0-E611-83A6-002590D9D8C2.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/C2A1DF0D-F0D0-E611-A81D-0CC47A57CD6A.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/5422AB4D-4FD1-E611-996A-0025907D2502.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/70EBD819-52D1-E611-BBCB-00259048A8F0.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/D60EBDF0-A3D1-E611-AC78-002590812700.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/5AD479ED-DCD1-E611-AEA3-0CC47A57CC42.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/E4916C4F-4FD2-E611-9A0E-0CC47A57CE00.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/4A6A2883-90D1-E611-8A8C-001E67444EAC.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/22BF017A-01D2-E611-81AC-0CC47A706D18.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-220_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/00C4A14D-46D2-E611-91C1-0CC47AC08C1A.root',
    )
if genMass == 240 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/D237B277-C5B9-E611-99AE-008CFA110AB4.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/AC965A51-E3B8-E611-A05A-0CC47A78A41C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/3CDD3C47-F3B8-E611-ADE3-0025905A60C6.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/709782D3-23B9-E611-9942-0CC47A4D76C8.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/FC06ED62-29B9-E611-A778-0025905A611E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/946093B7-2DB9-E611-8E8C-0025905A611E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/68751176-30B9-E611-826A-0CC47A4C8E7E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/FED94321-3AB9-E611-A017-0CC47A78A41C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-240_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/8A7012EE-3AB9-E611-AA91-0025905A6090.root',
    )
if genMass == 260 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/90000/7EA0D754-98C5-E611-A008-842B2B76832A.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/72F986BD-14C6-E611-B88F-002590D9D8D4.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/5A5B79B8-14C6-E611-B1C4-B083FED42C03.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/0CA27E4E-17C6-E611-954D-D4AE526A33F5.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/D854AF3D-05C6-E611-BE82-0CC47AA992B2.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/1816E6D0-07C6-E611-851C-0025901D08B8.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/FEDC3C0F-0CC6-E611-B3B6-00259048B754.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/F4E463C9-13C6-E611-A03E-0025901D08B8.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-260_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/90000/1A48539F-98C5-E611-84ED-0CC47A6C0758.root',
    )
if genMass == 280 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/100000/DA2A925F-84D8-E611-AEB9-02163E00E5BA.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/100000/B2A4E66E-83D8-E611-B1FB-0CC47A4C8E2E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/100000/20DDB38C-83D8-E611-BA2B-0025905A6126.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/40A7BDF3-5FD8-E611-906B-001E674DA83D.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/A410EADE-7FD8-E611-A0B0-001E67397DF5.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/DEBE3ED0-6FD8-E611-B4FE-0CC47A0AD6AA.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/A07F1742-7FD8-E611-B66D-001517F7F950.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/3680B88B-80D8-E611-8677-782BCB1F0729.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/E404A531-7FD8-E611-9502-A0369F301924.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/8E675CC6-6CD8-E611-BB81-0CC47AA9906E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/583C783F-7FD8-E611-BE12-0CC47AD99044.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-280_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/60000/EA2112E9-5FD8-E611-871B-A0000420FE80.root',
    )
if genMass == 300 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/1C128121-2AE5-E611-BFBD-28924A38DC1E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/4A21C55E-2FE5-E611-AEB0-0023AEEEB226.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/F808E661-2FE5-E611-9431-28924A33BBAA.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/C6A86A9B-1CE5-E611-9FF4-FA163E54C5AC.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/BA2FBEC2-1CE5-E611-AEEF-02163E00CA2D.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/4085A626-1DE5-E611-8219-0025904A90CA.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/0EF04163-2FE5-E611-9FAD-FA163E30BC70.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/C46E3932-2FE5-E611-8B70-FA163ED4BB59.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-300_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/70000/865B1E9E-2FE5-E611-90A0-6CC2173BC120.root',
    )
if genMass == 320 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/D8927726-3BC4-E611-A4E5-001E6739C801.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/0A05DD78-52C4-E611-8207-000101000026.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/1C22AAB2-6CC4-E611-8596-001E673D13C9.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/6E7BB7A3-7CC4-E611-A8D6-001E6739C801.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/666CD16E-95C4-E611-9690-00010100008C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/B6F88200-A8C4-E611-B3DD-001E673D0C31.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/FAD32D03-C2C4-E611-ABE9-001E673D0C31.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/1C5DDC5F-D9C4-E611-8025-000101000089.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-320_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/A8ABFD7E-EBC4-E611-92AF-001E673D0C31.root',
    )
if genMass == 340 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/1C5025FA-9ABE-E611-B244-B083FECF83AB.root', 
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/265A8008-9BBE-E611-B09B-0CC47A78A426.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/50E767FA-69BE-E611-A987-90E6BA693E13.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/5626AC84-97BE-E611-93EF-0242AC130005.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/5A913800-94BE-E611-899C-0242AC130003.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/64841C04-9BBE-E611-8387-A0000420FE80.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/6C5A8620-9BBE-E611-AC87-0242AC130002.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/7E43C8E9-76BE-E611-B44A-D067E5F910F5.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/9E5B2F5D-50BE-E611-892F-0CC47A13CC7A.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/A400D601-9BBE-E611-92FA-002590FD5A48.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/E444700B-9BBE-E611-84F1-FA163E1304E1.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/E80DE946-92BE-E611-BC47-D067E5F914D3.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-340_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/F4CB4C0B-9BBE-E611-A2C7-0CC47A4C8E26.root',
    )
if genMass == 350 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/92DA7DAA-85C0-E611-9345-20CF3027A570.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/A8D88453-85C0-E611-B0AC-002590200840.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/AE4BD1D9-7FC0-E611-85B5-00259073E488.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/6EDD114C-85C0-E611-B130-0025907B4F08.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/DEC19AEC-84C0-E611-982E-44A842240F8D.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/7010BA32-85C0-E611-BE17-002590791D60.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/74E902A3-76C0-E611-8C81-0CC47ABB517C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/AED782D7-7BC0-E611-97B9-0CC47ABB517C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/AE65E50C-7EC0-E611-99A5-0CC47A1E048A.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/DAD0E607-81C0-E611-8126-002590E7D7DE.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/E694ECB5-7FC0-E611-A2B7-0CC47ABB517C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/06007362-85C0-E611-A746-0CC47ABB517C.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/B026C8C9-84C0-E611-9BCB-001E674FB063.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/E411C372-85C0-E611-B8AD-002590494E94.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/A80F3562-85C0-E611-952D-02163E013833.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/8A641D57-85C0-E611-978E-00266CFFBF38.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-350_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/80000/B670207A-9FC0-E611-B963-001E67DFF4F6.root',
    )
if genMass == 400 :
    process.source.fileNames = cms.untracked.vstring(
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/94F9DE80-44C7-E611-A22B-0CC47A4D769E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/B46F93CC-3AC7-E611-9600-90B11C06954E.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/AAA9FECC-3AC7-E611-9108-001E67DFF735.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/642355C1-A7C7-E611-88C7-90B11C064B50.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/3C832E87-44C7-E611-BF86-A0000420FE80.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/0A084E92-44C7-E611-8DA3-0CC47AD98A9A.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/7AE43086-44C7-E611-A230-001E673476AA.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/868AB619-42C7-E611-BB72-ECF4BBE16230.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/4C691587-44C7-E611-B711-141877410EC1.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/B03C0CD5-2CC7-E611-B139-3417EBE706C3.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/2CB62F04-3FC7-E611-A8F6-3417EBE706ED.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/DCBBDCCD-44C7-E611-BDBD-002590DE38C8.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/FE489994-44C7-E611-A368-FA163E351C17.root',
        'file:root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/AToZhToLLTauTau_M-400_13TeV_madgraph_4f_LO/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/120000/E037BE5D-44C7-E611-A520-FA163E5CBD23.root',
    )

process.load("THRAnalysis.GenAnalysis.genMass_cfi")

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('azh%s.root' % genMass)
)


#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('myOutputFile.root')
#    ,outputCommands = cms.untracked.vstring('drop *',
#      #"keep *_myProducerLabel_*_*",
#      #"keep *_slimmedMuons_*_*",
#      "keep *_*_*_Demo",
#        )
#)

process.p = cms.Path(
            process.genMass)

#process.e = cms.EndPath(process.out)
