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



