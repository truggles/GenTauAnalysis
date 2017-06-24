from collections import OrderedDict
from CRABClient.UserUtilities import config
import os

config = config()

config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.psetName        = 'rerunningHLT_92x_crab_cfg.py'
config.JobType.pluginName      = 'Analysis'
# config.JobType.outputFiles     = ['outputFULL.root']
config.JobType.maxMemoryMB     = 2500
config.JobType.priority        = 2
config.JobType.numCores        = 4

#config.Data.splitting          = 'EventAwareLumiBased' # split by number of events
#config.Data.unitsPerJob        = 15000

config.Data.splitting          = 'FileBased'
config.Data.unitsPerJob        = 1
#config.Data.totalUnits         = 10 # For small tests

# JSON files:
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/
#config.Data.publication        = True
config.Data.outputDatasetTag   = 'rerunningHLT_92x'

config.Site.storageSite        = 'T2_US_Wisconsin'
# config.Site.blacklist          = ['T1_US_FNAL']
# config.Site.whitelist          = ['T2_CH_CERN']

config.User.voGroup            = 'uscms'

if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    #tag = 'MinosRatesV1'

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    #config.General.workArea   = 'crab_rate_' + tag
    #config.Data.outLFNDirBase = '/store/group/phys_tau/' + tag
    
    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    datasets = OrderedDict()

    #datasets['QCD_Pt_120to170'] = '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/PhaseIFall16DR-FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v1/GEN-SIM-RAW'
    datasets['TT_TuneCUETP8M2T4'] = '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/PhaseIFall16DR-FlatPU28to62HcalNZSRAW_90X_upgrade2017_realistic_v6_C1-v2/AODSIM'
   
    base = os.getenv("CMSSW_BASE")
    print "Base: ",base
    for k, v in datasets.iteritems():
        config.General.requestName = k
        #config.Data.inputDataset = v
        config.Data.outputPrimaryDataset = v.split('/').pop()
        config.Data.userInputFiles = open(base+'/src/THRAnalysis/TauHLTStudies/data/'+k+'.txt').readlines()
        #config.Data.useParent = True
        print 'submitting config:'
        print config
        submit(config)


