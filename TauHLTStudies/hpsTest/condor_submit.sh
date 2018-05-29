


###    --resubmit-failed-jobs \
### OLD ###
#########


DATE=20180527_eff_singleMuon
INPUT_FILES=singleMuon_may27.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=10 \
    --input-file-list=condorFileLists/${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    --input-basenames-not-unique \
    hps_condor_${DATE} $CMSSW_BASE condor_prompt_hps_DATA-miniAOD_cfg.py
    #hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA-RECO_cfg.py



