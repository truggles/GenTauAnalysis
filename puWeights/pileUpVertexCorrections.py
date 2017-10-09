'''Abreviated version of https://github.com/truggles/Z_to_TauTau_13TeV/blob/master/util/pileUpVertexCorrections.py'''



import ROOT
from collections import OrderedDict



def PUreweight( dataFile ) :
    # https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2015#PU_reweighting
    #data/Data_Pileup_2016_271036-284044_80bins.root - Moriond2017, full 2016 dataset
    #data/Data_Pileup_2017_294927-303825_80bins.root - 18.90/fb - 9 Oct 2017
    datafile = ROOT.TFile('data/'+dataFile, 'READ') # Moriond2017, full 2016 dataset
    dHist = datafile.Get('pileup')
    dHist.Scale( 1 / dHist.Integral() )

    # Early 2017 92x samples use Moriond17 PU distribution
    samplefile = ROOT.TFile('data/MC_Moriond17_PU25ns_V1.root', 'READ') # Moriond2017, full 2016 dataset
    sHist = samplefile.Get('pileup')
    sHist.Scale( 1 / sHist.Integral() )

    reweightDict = OrderedDict()
    for i in range( 1, dHist.GetXaxis().GetNbins()+1 ) :
        # dHist has exactly 600 bins, not 601 w/ over/underflow
        if sHist.GetBinContent( i ) > 0 :
            ratio = dHist.GetBinContent( i ) / sHist.GetBinContent( i )
        else : ratio = 0
        reweightDict[ (i-1)/10. ] = ratio

    #print reweightDict
    return reweightDict


