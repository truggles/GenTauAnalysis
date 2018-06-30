
## running on 92X MC files with 101X:
#hltGetConfiguration /dev/CMSSW_10_1_0/HLT/V138 \
#  --globaltag 101X_mc2017_realistic_TSG_2018_04_09_20_43_53 \
#  --path HLTriggerFirstPath,HLT_IsoMu27_v16,HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v12,HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg_v12,HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v3,HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v3,HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v12,HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v3,HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v12,HLTriggerFinalPath,HLTAnalyzerEndpath \
#  --input root://cms-xrd-global.cern.ch//store/mc/RunIISummer17DRStdmix/VBFHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/NZSFlatPU28to62_HIG07_92X_upgrade2017_realistic_v10-v1/710000/484235CE-E0A2-E711-AEA2-0242AC130002.root \
#  --mc --process MYHLT --full --offline \
#  --setup /dev/CMSSW_10_0_0/GRun \
#  --l1-emulator uGT \
#  --l1 L1Menu_Collisions2018_v1_0_0-d1_xml \
#  --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking \
#  --prescale 2.0e34 --max-events 10 --output none > hlt_MC_10_1_7_6Paths.py
#
#  cmsRun hlt_MC_10_1_7_6Paths.py &> mcLog.out &

# For 2018 data files
hltGetConfiguration /dev/CMSSW_10_1_0/HLT/V138 \
  --globaltag 101X_dataRun2_HLT_v7 \
  --path HLTriggerFirstPath,HLT_IsoMu27_v16,HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v12,HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg_v12,HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v3,HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v3,HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v12,HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v3,HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v12,HLTriggerFinalPath,HLTAnalyzerEndpath \
  --input root://cms-xrd-global.cern.ch//store/data/Run2018B/SingleMuon/RAW/v1/000/318/877/00000/FEC582EE-1E7B-E811-84B9-FA163E34467F.root \
  --data --process MYHLT --full --offline \
  --setup /dev/CMSSW_10_0_0/GRun \
  --l1-emulator uGT \
  --l1 L1Menu_Collisions2018_v1_0_0-d1_xml \
  --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2017DtUnpacking \
  --prescale 2.0e34 --max-events 10 --output none > hlt_DATA_10_1_7_6PathsX.py

  cmsRun hlt_DATA_10_1_7_6Paths.py &> dataLog.out &
