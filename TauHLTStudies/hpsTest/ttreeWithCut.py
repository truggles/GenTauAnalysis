import ROOT


def ttreeWithCuts( oldFile, oldTreePath, fOutName='ttreeWithCut.root', cut='' ) :
    f = ROOT.TFile( oldFile, 'r' )
    t = f.Get(oldTreePath)
    print "Num Events in initial TTree:",t.GetEntries()
    
    fOut = ROOT.TFile(fOutName,'RECREATE')
    tOut = t.CopyTree( cut )
    print "Num events in new TTree:",tOut.GetEntries()

    fOut.cd()
    
    # Make same directory path
    info = oldTreePath.split('/')
    info.pop() # Get rid of TTree name
    newPath = '/'.join( info )
    fOut.mkdir( newPath )
    fOut.cd( newPath )
    print "New path: %s/%s" % (newPath, tOut.GetName() )

    tOut.Write()
    fOut.Close()



if __name__ == '__main__' :
    oldFile = 'rate_april02.root'
    oldTreePath = 'hpsTauHLTStudies/tagAndProbe/Ntuple'
    fOutName = 'rate_april02_cut.root'
    cut = "RunNumber == 305636 && lumi >= 199 && lumi < 528"
    ttreeWithCuts( oldFile, oldTreePath, fOutName, cut )
