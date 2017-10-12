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

    #### Double Lepton Efficiencies ####
    dataFile = 'Data_Pileup_2016_271036-284044_80bins.root' # Moriond2017, full 2016 dataset
    puDict = PUreweight( dataFile )
    #print puDict

    tName = 'DoubleLeptonTAPStudies/tagAndProbe/Ntuple'
    dName = 'DoubleLeptonTAPStudies/tagAndProbe'
    base = '/data/truggles/doubleLepTAP_oct06v2/'
    #addPuWeight( puDict, base+'DYJetsExt.root', dName, tName )
    #isData = True
    #addPuWeight( puDict, base+'SingleMuon.root', dName, tName, isData )
    #addPuWeight( puDict, base+'SingleElectron.root', dName, tName, isData )


    #### Tau Trigger Efficiencies ####
    dataFile = 'Data_Pileup_2017_294927-303825_80bins.root' # 18.90/fb - 9 Oct 2017
    puDict = PUreweight( dataFile )
    #print puDict

    tName = 'tauMiniAODHLTStudies/tagAndProbe/Ntuple'
    dName = 'tauMiniAODHLTStudies/tagAndProbe'
    base = '/data/truggles/oct09v1_TauTAP/'
    #addPuWeight( puDict, base+'DYJetsTauTAP.root', dName, tName )
    #addPuWeight( puDict, base+'GluGluHToTauTau_M125.root', dName, tName )
    #addPuWeight( puDict, base+'VBFHToTauTau_M125.root', dName, tName )
    isData = True
    addPuWeight( puDict, base+'SingleMuonTauTAP.root', dName, tName, isData )



