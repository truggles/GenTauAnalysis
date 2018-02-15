


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

#DATE=20180129v1_dyj_V7
#INPUT_FILES=dyJets_V7.txt
#
#farmoutAnalysisJobs \
#    --resubmit-failed-jobs \
#    --output-dir=. \
#    --input-files-per-job=30 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py

#DATE=20180128v1_ggH_V7
#INPUT_FILES=ggH125_jan28_V7.txt
#
#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=15 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py

#XXX DATE=20180213_feb13_v3
#XXX INPUT_FILES=efficiency_qqH_feb13_v2.txt
#XXX 
#XXX farmoutAnalysisJobs \
#XXX     --output-dir=. \
#XXX     --input-files-per-job=15 \
#XXX     --input-file-list=condorFileLists/${INPUT_FILES} \
#XXX     --site-requirements='OpSysAndVer == "SL6"' \
#XXX     hps_condor_${DATE} $CMSSW_BASE condor_hps_cfg.py


DATE=20180214_rate_jan13_v9_v1
INPUT_FILES=rate_jan13_v9.txt

farmoutAnalysisJobs \
    --output-dir=. \
    --input-files-per-job=10 \
    --input-file-list=condorFileLists/${INPUT_FILES} \
    --site-requirements='OpSysAndVer == "SL6"' \
    --input-basenames-not-unique \
    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA_cfg.py


#DATE=20180130v2_Tau_V7
#INPUT_FILES=tau_jan30_V7_v9.txt
#
#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=5 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    --input-basenames-not-unique \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA-RECO_cfg.py
#
#
#DATE=20180130v2_SingleMuon_V7
#INPUT_FILES=singleMuon_jan30_V7_v9.txt
#
#farmoutAnalysisJobs \
#    --output-dir=. \
#    --input-files-per-job=5 \
#    --input-file-list=condorFileLists/${INPUT_FILES} \
#    --site-requirements='OpSysAndVer == "SL6"' \
#    --input-basenames-not-unique \
#    hps_condor_${DATE} $CMSSW_BASE condor_hps_DATA-RECO_cfg.py



