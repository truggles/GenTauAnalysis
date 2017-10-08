import ROOT
from array import array
from pileUpVertexCorrections import PUreweight
import math



puDict = PUreweight()
#print puDict

def addPuWeight( iFile, iDir, iTree, isData=False ) :
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

    # Double Lepton Efficiencies
    tName = 'DoubleLeptonTAPStudies/tagAndProbe/Ntuple'
    dName = 'DoubleLeptonTAPStudies/tagAndProbe'
    base = '/data/truggles/doubleLepTAP_oct06v2/'
    #addPuWeight( base+'DYJets.root', dName, tName )
    isData = True
    #addPuWeight( base+'SingleMuon.root', dName, tName, isData )
    #addPuWeight( base+'SingleElectron.root', dName, tName, isData )


    # Tau Trigger Efficiencies
    tName = 'tauMiniAODHLTStudies/tagAndProbe/Ntuple'
    dName = 'tauMiniAODHLTStudies/tagAndProbe'
    base = '/data/truggles/hltTaus_oct03v2/'
    #addPuWeight( base+'DYJets.root', dName, tName )
    #addPuWeight( base+'GluGluHToTauTau_M125.root', dName, tName )
    #addPuWeight( base+'VBFHToTauTau_M125.root', dName, tName )
    #isData = True
    #addPuWeight( base+'SingleMuon.root', dName, tName, isData )



