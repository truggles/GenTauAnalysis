#!/bin/bash

jobNum=2

#farmoutAnalysisJobs \
#    --input-file-list=singleMuonB_MINIAOD.txt \
#    --input-files-per-job=3 \
#    hlt_studies_muon_${jobNum} $CMSSW_BASE condor_muon_MiniAOD_cfg.py

farmoutAnalysisJobs \
    --input-file-list=tauB_MINIAOD.txt \
    --input-files-per-job=3 \
    hlt_studies_tau_${jobNum} $CMSSW_BASE condor_tau_MiniAOD_cfg.py
