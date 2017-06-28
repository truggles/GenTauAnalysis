

import FWCore.ParameterSet.Config as cms

def getCrabSecondaryFiles( child ) :
    import json, os
    base = os.getenv("CMSSW_BASE")
    jFile = open(base+'/src/THRAnalysis/TauHLTStudies/data/aod_map.json')
    j = json.load( jFile )
    parents = j[ child ]
    jFile.close()
    p = cms.untracked.vstring( parents )
    return p

def setCrabSourceFiles( process ) :
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(),
        secondaryFileNames = cms.untracked.vstring()
    )

    return process



def setSourceFiles( process ) :

    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/307B752F-0B11-E711-932E-24BE05CEECD1.root",
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/A059715B-5811-E711-A56B-E0071B7A8550.root",
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/B823DD9D-DB11-E711-909B-FA163EE6D403.root",


            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/8811279D-2A11-E711-8F6C-70106F4A46B8.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/98823559-D114-E711-97BF-0025905A610C.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/E858AF6B-9511-E711-94A9-FA163E4A5929.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/5E1A04A1-1F11-E711-B8FA-0242AC130003.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/BE394222-DB11-E711-A657-02163E013006.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/FE225DDD-5411-E711-9B1C-A0000420FE80.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/8EDD91EA-2112-E711-BE62-0CC47A57CD88.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/982EEBE2-8C13-E711-B7DA-002590FD5A48.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/8E088AF2-3C12-E711-8B82-7845C4FC359F.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/78FACBE2-4311-E711-8810-1866DA89035E.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/A0500125-C814-E711-A462-0025905A6110.root",
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/F0642738-DF14-E711-9BAD-FA163E11CA5A.root",


            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/021FA4A0-6D11-E711-AD9D-FA163ED9BE5A.root', # Defaul ones child
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/AODSIM/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/0018A939-3D2F-E711-9DA6-549F3525C318.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/VBFHToTauTau_M125_13TeV_powheg_pythia8/AODSIM/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/120000/0026E972-9810-E711-B5D5-0CC47A57CB8E.root',
        ),
        secondaryFileNames = cms.untracked.vstring(
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/DC3FC620-0311-E711-BB61-24BE05C618F1.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/729A7075-FA10-E711-BB08-E0071B74AC10.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E21F78DC-EB10-E711-8CF4-5065F3812201.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E8CF7064-EC10-E711-AA9F-E0071B7AF7C0.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/32F2827D-FF10-E711-B5A6-E0071B7AC700.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/3CD8B21D-0311-E711-B01B-5065F37D7121.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/52CE68CA-0211-E711-AB11-A0000420FE80.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/908B6F90-0311-E711-858C-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/A857625E-FF10-E711-A1A2-24BE05CECDD1.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/DC168120-0311-E711-9364-24BE05C6E561.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/1036BAB1-EF10-E711-BB95-A0000420FE80.root"
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/08F0C3C8-0D11-E711-9B33-E0071B7A8570.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/0AFE5B0B-1911-E711-9B5D-5065F381C251.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/68F1B5EA-1A11-E711-B33B-A0000420FE80.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/941FC8CA-2D11-E711-BF80-5065F3815241.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C0E80F75-1911-E711-A68D-5065F382C211.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C8428C69-3211-E711-BCDE-B8CA3A70BAC8.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/D4C1C5BA-2B11-E711-A667-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/E079D08B-2C11-E711-B2EB-5065F3816201.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/F288F879-2711-E711-8BF6-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/F89D288C-2411-E711-B05E-E0071B73B6F0.root"


            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/1E1AE55B-0912-E711-8E2C-002590D9D8A4.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/389F800B-0B12-E711-A027-0CC47A57D1F8.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/4C0EFCA7-1A12-E711-BA80-0CC47AB0B704.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/58583968-EF11-E711-BE4F-0CC47A0AD498.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/D2A3D603-1A11-E711-9036-E0071B7AC7C0.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/FC98CF66-1711-E711-ADCF-24BE05C3EC61.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/022957F0-1511-E711-8947-24BE05CEADD1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/1603A0BB-0911-E711-A668-24BE05C6E7E1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/6811AC7B-1411-E711-9797-24BE05CEADD1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/AE68DAB3-0611-E711-84D6-E0071B7AC710.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/BA2ED90F-0711-E711-8073-24BE05C6E7E1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/CE0D9275-0911-E711-8FC8-A0000420FE80.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/FA0D4589-0711-E711-BB3C-24BE05C666B1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/1CCCACB9-2011-E711-80BC-E0071B7AC700.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/D053A652-2011-E711-89FA-A0000420FE80.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/30BD8373-C611-E711-9F3F-FA163E33E238.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/481B4CFC-D111-E711-937C-FA163E33C411.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/8CE2517B-D311-E711-9BA4-FA163E33C411.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/B8DF852D-D311-E711-BE1B-FA163EAF2DA0.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/E6518402-C411-E711-97C0-FA163E18FE3D.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/7879B722-CF12-E711-8C7A-0025901AC3FE.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/16E0F73F-0A11-E711-AE09-0242AC130003.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/30A62CDD-0711-E711-9B06-0242AC130005.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/3CECB7F0-0711-E711-8BF8-0242AC130005.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/686DDF6B-0811-E711-B1CC-0242AC130005.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/A67D5DF1-0B11-E711-901D-0242AC130005.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/AEC09835-0A11-E711-8B09-0242AC130005.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/C62735E0-0711-E711-9FF8-0242AC130003.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/CAE45BFF-0A11-E711-8F6C-0242AC130002.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/E6701717-0311-E711-9854-0242AC130002.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/EC56AD8A-8A11-E711-9FF3-FA163E131D1F.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90002/2E7B40C0-4211-E711-8EB4-002590495240.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/50A70179-8911-E711-B4CB-FA163EDD96EE.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/7A6E3E7B-8B11-E711-A2E2-FA163EE4230D.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/B6F7A65A-8811-E711-9A6C-02163E00B156.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90003/EE9A5F48-8911-E711-9B00-FA163EDD96EE.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/00E6928C-C514-E711-B247-003048FFCBB2.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/046B8966-C614-E711-8B00-0025905A612E.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/0C1E1569-C314-E711-86B6-0CC47A7C3636.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/14423324-C314-E711-A58F-0025905B85AA.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/18B7733B-C514-E711-A024-0CC47A4D76B8.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/66D8909E-C614-E711-934F-003048FFCBB8.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/78E9864F-C514-E711-BD26-0CC47A78A45A.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/9625A7E5-C314-E711-8110-003048FFCBB2.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/AC8BF19E-C614-E711-82E4-0025905A6068.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/ACBDF025-C314-E711-96F3-0025905A60BE.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C280C153-2111-E711-8939-70106F4D2364.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/FE8ADF3E-2211-E711-B571-0CC47A7DFD16.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/0EC072EF-2011-E711-820F-047D7BD6DED2.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/3E39DA06-2111-E711-A2B7-0CC47A7E6BDE.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/06FB685A-B911-E711-8D19-02163E012EF2.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/423551B7-AD11-E711-9289-02163E011475.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/48211468-BB11-E711-9DA5-FA163EEE2FD1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/72A9DEA1-BE11-E711-98F5-FA163E1AD6E1.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/A2A1F802-C111-E711-A89B-FA163E9D9193.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/B4D262C3-6711-E711-AC40-7845C4FC35BD.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/0AFA3870-2611-E711-B3BB-D4AE526A0A9A.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/327B3198-2F11-E711-ACEE-D4AE526A1654.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C6D5A1C5-2A11-E711-A59C-842B2B766242.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/FE608230-3511-E711-BCE8-D4AE526A0AB5.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/0697A443-BE14-E711-A0CE-0025905A6094.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/24655CEC-BC14-E711-A3C9-0CC47A4D767A.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/5A69E09B-BD14-E711-B5A6-0025905A60C6.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/982314EE-BC14-E711-89B8-0025905A60C6.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/A857F0A2-BA14-E711-82A2-003048FFD722.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/D64157B0-BA14-E711-988D-0025905A60C6.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E8266DB0-BC14-E711-AA32-0025905A6094.root"
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/3E1570CD-D514-E711-BFE5-FA163EFE8B90.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/80EE2587-D714-E711-A5BA-FA163EE0B622.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/C6AD4D46-D214-E711-B25B-FA163EA4F3B3.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/D855C8BB-D214-E711-BF7F-FA163EC292D8.root", 
            #"root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E017E936-D114-E711-9920-FA163EA4F3B3.root"



            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/AE8721E0-5F11-E711-BEFF-FA163E35EC22.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/C6FCF1D8-5911-E711-93BA-FA163E613555.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/4CA177D8-5411-E711-8EFE-FA163E4FCBAC.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/76979FAA-6211-E711-9BB7-FA163E30EA14.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/AEDFC268-5B11-E711-8A12-02163E013E78.root', 

            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1C5A314D-2F2F-E711-BCFF-549F3525DDFC.root', 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1E200A0E-2D2F-E711-9D06-782BCB53A3A6.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/24EA3BFD-2C2F-E711-9AF8-001C23C0B673.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/5EA04778-2E2F-E711-A95B-141877410B85.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/722A19C7-242F-E711-B6C5-1866DAEEB358.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C61F0036-302F-E711-91AC-1866DAEB3370.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C8A77762-2F2F-E711-A824-549F3525C318.root', 

            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/1E218178-721B-E711-950C-0242AC130002.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/9688E2B3-5A1B-E711-AFE9-003048FF265A.root',
        )
    )

    return process


def customizeInput( _customInfo ) :

    # This is the input to the reHLT process, so is actuall the "secondary" files from above
    _customInfo['inputFile' ]=  [
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/DC3FC620-0311-E711-BB61-24BE05C618F1.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/729A7075-FA10-E711-BB08-E0071B74AC10.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E21F78DC-EB10-E711-8CF4-5065F3812201.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/E8CF7064-EC10-E711-AA9F-E0071B7AF7C0.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/32F2827D-FF10-E711-B5A6-E0071B7AC700.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/3CD8B21D-0311-E711-B01B-5065F37D7121.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/52CE68CA-0211-E711-AB11-A0000420FE80.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/908B6F90-0311-E711-858C-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/A857625E-FF10-E711-A1A2-24BE05CECDD1.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/DC168120-0311-E711-9364-24BE05C6E561.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/1036BAB1-EF10-E711-BB95-A0000420FE80.root"
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90000/08F0C3C8-0D11-E711-9B33-E0071B7A8570.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/0AFE5B0B-1911-E711-9B5D-5065F381C251.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/68F1B5EA-1A11-E711-B33B-A0000420FE80.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/941FC8CA-2D11-E711-BF80-5065F3815241.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C0E80F75-1911-E711-A68D-5065F382C211.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/C8428C69-3211-E711-BCDE-B8CA3A70BAC8.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/D4C1C5BA-2B11-E711-A667-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/E079D08B-2C11-E711-B2EB-5065F3816201.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/F288F879-2711-E711-8BF6-E0071B7A9810.root", 
            "root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/90001/F89D288C-2411-E711-B05E-E0071B73B6F0.root"



            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130000/AE8721E0-5F11-E711-BEFF-FA163E35EC22.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130001/C6FCF1D8-5911-E711-93BA-FA163E613555.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/4CA177D8-5411-E711-8EFE-FA163E4FCBAC.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/76979FAA-6211-E711-9BB7-FA163E30EA14.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16DR/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/130002/AEDFC268-5B11-E711-8A12-02163E013E78.root' 

            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1C5A314D-2F2F-E711-BCFF-549F3525DDFC.root', 
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/1E200A0E-2D2F-E711-9D06-782BCB53A3A6.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/24EA3BFD-2C2F-E711-9AF8-001C23C0B673.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/5EA04778-2E2F-E711-A95B-141877410B85.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/722A19C7-242F-E711-B6C5-1866DAEEB358.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C61F0036-302F-E711-91AC-1866DAEB3370.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseISpring17DR/GluGluHToTauTau_M125_13TeV_powheg_pythia8/GEN-SIM-RAW/FlatPU28to62HcalNZSRAW_HIG06_90X_upgrade2017_realistic_v20-v1/60000/C8A77762-2F2F-E711-A824-549F3525C318.root'

            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/1E218178-721B-E711-950C-0242AC130002.root',
            #'root://cms-xrd-global.cern.ch///store/mc/PhaseIFall16MiniAOD/VBFHToTauTau_M125_13TeV_powheg_pythia8/MINIAODSIM/FlatPU28to62HcalNZSRAW_PhaseIFall16_90X_upgrade2017_realistic_v6_C1-v1/00000/9688E2B3-5A1B-E711-AFE9-003048FF265A.root',
            ]
    _customInfo['maxEvents' ]=  999999

    return _customInfo


def buildGenTausAndMore( process ) :

    import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
    process.hltFilter = hlt.triggerResultsFilter.clone( 
            hltResults = cms.InputTag( "TriggerResults","","MYHLT"), 
            triggerConditions = ( 'HLT_IsoMu*', 'HLT_Double*'),
            l1tResults = '', 
            throw = False 
            )
    
    
    process.tauGenJets = cms.EDProducer(
        "TauGenJetProducer",
        GenParticles =  cms.InputTag('genParticles'),
        includeNeutrinos = cms.bool( False ),
        verbose = cms.untracked.bool( False )
        )
    
    
    process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('oneProng0Pi0', 
                              'oneProng1Pi0', 
                              'oneProng2Pi0', 
                              'oneProngOther',
                              'threeProng0Pi0', 
                              'threeProng1Pi0', 
                              'threeProngOther', 
                              'rare'),
         filter = cms.bool(False)
    )
    
    
    process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('electron'), 
         filter = cms.bool(False)
    )
    
    
    process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('muon'), 
         filter = cms.bool(False)
    )
    
    
    process.load("THRAnalysis.TauHLTStudies.CfiFile_cfi")
    
    
    process.TFileService = cms.Service("TFileService",
                                           fileName = cms.string('ttree.root')
                                       )
    
    
    process.p = cms.Path(
                #process.hltFilter*
                process.tauGenJets*
                process.tauGenJetsSelectorAllHadrons*
                process.tauGenJetsSelectorElectrons*
                process.tauGenJetsSelectorMuons*
                process.tauHLTStudies)

    return process


def simpleDataFromRAW( process ) :

    #import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
    #process.hltFilter = hlt.triggerResultsFilter.clone( 
    #        hltResults = cms.InputTag( "TriggerResults","","HLT"), 
    #        #triggerConditions = ( 'HLT_IsoMu20_v*', 'HLT_IsoMu24_v*', \
    #        triggerConditions = ( 'HLT_IsoMu24_v*', \
    #            'HLT_IsoMu24_eta2p1_v*', 'HLT_IsoMu27_v*'),
    #        l1tResults = '', 
    #        throw = False 
    #        )
    
    
    process.load("THRAnalysis.TauHLTStudies.CfiFile_cfi")
    
    
    process.TFileService = cms.Service("TFileService",
                                           fileName = cms.string('ttree.root')
                                       )
    
    
    process.p = cms.Path(
                #process.hltFilter*
                process.tauHLTStudies)

    return process


def simpleDataFromMiniAOD( process ) :

    #import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
    #process.hltFilter = hlt.triggerResultsFilter.clone( 
    #        hltResults = cms.InputTag( "TriggerResults","","HLT"), 
    #        #triggerConditions = ( 'HLT_IsoMu20_v*', 'HLT_IsoMu24_v*', \
    #        triggerConditions = ( 'HLT_IsoMu24_v*', \
    #            'HLT_IsoMu24_eta2p1_v*', 'HLT_IsoMu27_v*'),
    #        l1tResults = '', 
    #        throw = False 
    #        )
    
    
    process.load("THRAnalysis.TauHLTStudies.miniAOD_CfiFile_cfi")
    
    
    process.TFileService = cms.Service("TFileService",
                                           fileName = cms.string('ttree.root')
                                       )
    
    
    process.p = cms.Path(
                #process.hltFilter*
                process.tauHLTStudies)

    return process


def setOutputFile( process) :
    process.Out = cms.OutputModule( "PoolOutputModule",
        fileName = cms.untracked.string( "stage1_output_ttbar_20files.root" ),
        fastCloning = cms.untracked.bool( False ),
        dataset = cms.untracked.PSet(
            filterName = cms.untracked.string(''),
            dataTier = cms.untracked.string('GEN-SIM-RAW-AOD')
        ),
        outputCommands = cms.untracked.vstring(
                        "drop *",
                        "keep *_TriggerResults_*_MYHLT",
                        "keep *_hltGtStage2Digis_Tau_MYHLT",
                        "keep *_hltGtStage2Digis_Muon_MYHLT",
                        "keep *_addPileupInfo_*_*",
                        "keep recoPFTaus_hpsPFTauProducer__RECO",
                        "keep recoPFTauDiscriminator_*_*_RECO",
                        "keep *_hpsPFTauTransverseImpactParameters__RECO",
                        "keep recoMuons_muons__RECO",
                        "keep *_offlinePrimaryVertices_*_*",
                        #"keep *_selectedPatTrigger_*_*", # Not in AODSIM
                        "keep *_gtStage2Digis_Tau_RECO",
                        "keep recoGenParticles_genParticles_*_HLT",
                        )
    )
    
    process.end = cms.EndPath( process.Out )

    return process


