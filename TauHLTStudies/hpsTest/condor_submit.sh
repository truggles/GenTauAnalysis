



DATE=20171128v1

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=15 \
    --input-file-list=condorFileLists/firstTry.txt \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py
