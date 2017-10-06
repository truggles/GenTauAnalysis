# Tau HLT Studies
Current HLT studies require rerunning the HLT menue on trigger studies samples. The code in THRAnalysis/TauHLTStudies is being set up for this purpose. WORK IN PROGRESS.

See where the instructions produce the vast majority of TauHLTStudies/python/rerunningHLT_cfg.py:
    https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT#Running_the_HLT_with_CMSSW_9_2_0


This commit has been mentioned as necessary (edit by hand if desired): 
    https://github.com/cms-sw/cmssw/pull/19211
    https://github.com/cms-sw/cmssw/pull/19211/commits/b09d26ccc4a41c197255a384398eeee9a41ee897
```
git cms-addpkg  DataFormats/PatCandidates
vi DataFormats/PatCandidates/src/TriggerObjectStandAlone.cc
```

```
cd TauHLTStudies
cmsRun python/rerunningHLT_cfg.py
```


# Tau and Electrons and Muons Tag and Probe
Get previous HLT_doubleTau35 work (only necessary if you want to compare
to Riccardo's 2016 results)

```
cd TagAndProbe
source setup.sh
```

For Elec + Muon triggers:
EDAnalyzer is here: TagAndProbe/plugins/DoubleLeptonTAP.cc
Run via crab submissions here: TagAndProbe/test/doubleLepTAP_crab_submit.py
Then hadd the output files, transport locally
Add puWeight terms using: puWeights/addPUReweight.py which is set to use 2016 Moriond17 MC and full 2016 35.9/fb data nTruePU
Then make the scalefactor output file and plots using: TagAndProbe/python/plot_doubleLep_efficiencies.py




# GenTauAnalysis

`cd GenAnalysis`

Package used to calculate acceptance values for Z->TauTau analysis

To operate:
1. run the analyzer over the DYJets sample file provided

`cmsRun python/ConfFile_cfg.py`

2. add pileup reweighting distribution

`cd puWeights`
`python addPUReweight.py`
`cd ..`

3. print out initial and fiducal cut yields for each channel

`python printWeights.py`

4. for detailed efficiency calculations print out file with all events for each channel passing fiducal cuts + another list with passing genMass window.  This list will be compared to the events in the final signal region

`python genEventInfo.py`

5. copy over your selected final cut based analysis tree to the main directory here (AcceptanceAnalyzer)

`cp .......root .`

6. compare analysis selected events to the gen selected events and dump results to output file

`python recoEventInfo.py > dump.txt`

7. print results of the above dump.  Not sure why I chose this route.

`python finalResults.py`
