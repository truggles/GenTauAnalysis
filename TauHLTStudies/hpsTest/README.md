# For HPS-enabled trigger testing

To get the hlt configuration files and correct set up see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Running_the_HLT_with_CMSSW_10_0

```
cmsrel CMSSW_10_0_3
cd CMSSW_10_0_3/src
cmsenv
git cms-addpkg HLTrigger/Configuration
git cms-merge-topic 22360

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 6
```


# For L2p5 Tau Studies

Added a few L2p5 collections to the re-run HLT files including
   * hltL2TausForPixelIsolation
   * hltL2TauPixelIsoTagProducer
   * hltOnlineBeamSpot
   * hltPixelTracksMergedRegL1TauSeeded
   * hltPixelVerticesRegL1TauSeeded
   * hltL2TausForPixelIsolationL1TauSeeded
   * hltL2TauJetsL1TauSeeded
   * hltL2TauJetsIsoL1TauSeeded

The section of code being setup to study the isolation is in `plugins/HPSTauHLTStudiesAnalyzer.cc`
search for `L2.5 Tau Studies`, or see here: https://github.com/truggles/THRAnalysis/blob/hlt_l2p5_tracks/TauHLTStudies/plugins/HPSTauHLTStudiesAnalyzer.cc#L1138


# Path to some processed files
A few user processed samples are located at `T2_US_Wisconsin`.

    dasgoclient --query="dataset dataset=/VBFHToTauTau_M125_13TeV_powheg_pythia8/truggles*/USER instance=prod/phys03"

To get the file list for one of the example samples:

    dasgoclient --query="file dataset=/VBFHToTauTau_M125_13TeV_powheg_pythia8/truggles-qqH125_hps_1003_april09_test_v1-91efddd5d6f4f859dbb0d7cc1618939f/USER instance=prod/phys03"



# To-do:
   * store variables in the output TTree for study
   * make some initial distributions of dZ, dXY for L2p5 tracks

