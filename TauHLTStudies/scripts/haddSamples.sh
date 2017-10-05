#!/bin/bash

echo "New crab files being hadded ${1}"

echo "New /data/${USER}/hltTaus_${1} directory"
mkdir -p /data/${USER}/hltTaus_${1}

for SAMPLE in DYJets GluGluHToTauTau_M125 VBFHToTauTau_M125 SingleMuon; do
    hadd /data/${USER}/hltTaus_${1}/${SAMPLE}.root /hdfs/store/user/${USER}/${SAMPLE}*/*_${1}/*/*/outfile_*.root

done
