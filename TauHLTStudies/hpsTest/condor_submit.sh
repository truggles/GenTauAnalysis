


#    --resubmit-failed-jobs \

### OLD ###
### DATE=20180115v2_ptRes
### INPUT_FILES=ggH125_jan15_ptRes2.txt
### DATE=20180115v2_iso20PerInc
### INPUT_FILES=ggH125_jan15_ptRes_iso20PerInc2.txt
### DATE=20180116v1_0p5PtAdjIso60
### INPUT_FILES=ggH125_jan16_0p5PtAdjIso60PerInc.txt
### DATE=20180116v1_0p5PtAdjIso40
### INPUT_FILES=ggH125_jan16_0p5PtAdjIso40PerInc.txt
### DATE=20180117v1_Menu_V6
### INPUT_FILES=ggH125_jan17_hps_Menu_V6.txt
### DATE=20180118v1_TS_Def
### INPUT_FILES=qqH_strebler.txt # Didn't work well
### DATE=20180119v2_qqH_reqMed
### INPUT_FILES=qqH125_jan18_hps_Menu_V6.txt
### DATE=20180121v2_hltPhysicsAll
### INPUT_FILES=jan21_hltPhysicsAll.txt
### DATE=20180123v2_hltPhysicsAll_crgIso3p7
### INPUT_FILES=jan22_hltPhysicsAll_crgIso3p7.txt
### DATE=20180128v1_hltPhysicsAll_V7
### INPUT_FILES=jan28_V7_rate.txt
#########

#DATE=20180218_feb17_finalCfg
#INPUT_FILES=eff_feb17_finalCfg.txt
#
#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=15 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py



#DATE=20180218_feb17_all
#INPUT_FILES=rate_feb17_all.txt
#
#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=10 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    --input-basenames-not-unique \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA_cfg.py
#

DATE=20180218_eff_singleMuon_feb18
INPUT_FILES=eff_singleMuon_feb18.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=25 \
    --input-file-list=condorFileLists/${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    --input-basenames-not-unique \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA-RECO_cfg.py



