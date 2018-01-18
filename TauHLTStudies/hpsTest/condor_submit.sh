


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
#########

DATE=20180117v1_Menu_V6
INPUT_FILES=ggH125_jan17_hps_Menu_V6.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=15 \
    --input-file-list=condorFileLists/${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py




