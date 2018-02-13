# For HPS-enabled trigger testing

To get the hlt configuration files and correct set up see: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Running_the_HLT_with_CMSSW_10_0

```
cmsrel CMSSW_10_0_1
cd CMSSW_10_0_1/src
cmsenv
git cms-addpkg HLTrigger/Configuration

# Dependencies and Compilation
git cms-checkdeps -A -a
scram b -j 6
```



