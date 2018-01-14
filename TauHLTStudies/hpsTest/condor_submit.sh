



DATE=20180114v2_default
INPUT_FILES=condorFileLists/ggH125_jan14_default.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=30 \
    --input-file-list=${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py



