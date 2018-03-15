import ROOT
from array import array
from pileUpVertexCorrections import PUreweight
import math




def addPuWeight( puDict, iFile, iDir, iTree, isData=False ) :
    f = ROOT.TFile( iFile, 'UPDATE' )
    d = f.Get( iDir )
    t = f.Get( iTree )

    print "file:",f
    print "tree:",t
    
    puweight = array('f', [0])
    puweightB = t.Branch('puweight', puweight, 'puweight/F')
    
    count = 0
    for i in range( t.GetEntries() ) :
        t.GetEntry( i )
        if count % 10000 == 0 : print "Event:",count
        nTrPu = ( math.floor(t.nTruePU * 10))/10
        if isData :
            puweight[0] = 1
        else :
            puweight[0] = puDict[ nTrPu ]
        puweightB.Fill()
        count += 1
    
    print "DONE!"
    
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f.Close()



if '__main__' in __name__ :

    doTauHLT = True
    doZH = False

    if doZH :
        #### Double Lepton Efficiencies ####
        dataFile = 'Data_Pileup_2016_271036-284044_80bins.root' # Moriond2017, full 2016 dataset
        puDict = PUreweight( dataFile )
        #print puDict

        date = 'nov09v3'
        tName = 'DoubleLeptonTAPStudies/tagAndProbe/Ntuple'
        dName = 'DoubleLeptonTAPStudies/tagAndProbe'
        base = '/data/truggles/zhTrigEff_'+date+'/'
        addPuWeight( puDict, base+'zhTrigEff_DYJets_'+date+'.root', dName, tName )
        isData = True
        addPuWeight( puDict, base+'zhTrigEff_SingleMuon_'+date+'.root', dName, tName, isData )
        addPuWeight( puDict, base+'zhTrigEff_SingleElectron_'+date+'.root', dName, tName, isData )


    if doTauHLT :
        #### Tau Trigger Efficiencies ####
        #dataFile = 'Data_Pileup_2017_AllRunB-E_80bins.root'
        dataFile = 'Data_Pileup_2017_RunB-mostOfF_80bins.root'
        puDict = PUreweight( dataFile )
        #print puDict

        tName = 'tauMiniAODHLTStudies/tagAndProbe/Ntuple'
        dName = 'tauMiniAODHLTStudies/tagAndProbe'
        base = '/data/truggles/tauTrigger_nov28forSyncV1/'
        addPuWeight( puDict, base+'DYJetsTauTAP.root', dName, tName )
        ###addPuWeight( puDict, base+'GluGluHToTauTau_M125.root', dName, tName )
        ###addPuWeight( puDict, base+'VBFHToTauTau_M125.root', dName, tName )
        isData = True
        addPuWeight( puDict, base+'SingleMuonTauTAP_nov28forSyncV1.root', dName, tName, isData )



