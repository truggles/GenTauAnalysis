# For HPS-enabled trigger testing

To get the hlt configuration files and correct set up see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Running_the_HLT_with_CMSSW_10_0

# CMSSW_10_1_X (2018 data-taking release)

2018 Run-2 development HLT menus: GRun for pp (25ns), HIon for PbPb, PRef for pp5TeVref, and PIon for pPb. 

```
setenv SCRAM_ARCH slc6_amd64_gcc630
cmsrel CMSSW_10_1_1
cd CMSSW_10_1_1/src
cmsenv

git cms-addpkg HLTrigger/Configuration

scram build -j 4
cd HLTrigger/Configuration/test
```



