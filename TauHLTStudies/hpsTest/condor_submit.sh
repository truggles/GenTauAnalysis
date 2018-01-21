


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
#########

DATE=20180119v2_qqH_reqMed
INPUT_FILES=qqH125_jan18_hps_Menu_V6.txt

#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=15 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py


DATE=20180121v1_hltPhysics1
INPUT_FILES=jan21_hltPhysics1.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=15 \
    --input-file-list=condorFileLists/${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA_cfg.py




