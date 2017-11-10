
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)


def decorate(cmsLumi) :
    logo = ROOT.TText(.2, .85,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .85,"CMS Preliminary")
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.67,.91,"%.1f / fb (13 TeV)" % cmsLumi )

def getHist( tree, var, cut, name ) :
    h = ROOT.TH1F( name, name, 200, -.25, .25)
    #h = ROOT.TH1F( name, name+trigger, len(binning)-1, binning)
    #h.Sumw2()
    doCut = ''
    doCut += cut

    tree.Draw( var+' >> '+name, doCut )

    print name, h.Integral()
    
    h.GetXaxis().SetTitle('(Offline pT - HLT pT)/Offline pT')
    h.GetYaxis().SetTitle('A.U.')
    h.SetDirectory( 0 )
    return h


plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/zhTrigEff_nov09v3/'
nDYJets = 'zhTrigEff_DYJets_nov09v3.root'
directory = 'zhTrigEff_nov09v3'
fDYJets = ROOT.TFile('/data/truggles/'+directory+'/'+nDYJets, 'r')
tDYJets = fDYJets.Get('DoubleLeptonTAPStudies/tagAndProbe/Ntuple')


for channel in ['ee', 'mm',] :
    if channel == 'ee' :
        dataFile = 'zhTrigEff_SingleElectron_nov09v3.root'
        mapper = {
            'Ele27 WPTight Gsf' : '(l1Match_HLT_Ele27_WPTight_Gsf > 0.5) && l1Pt > 27 && l1Pt < 33',
            'Ele12 CaloIdL TrackIdL IsoVL' : 'l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5 && l2Pt > 10 && l2Pt < 15',
            'Ele23 CaloIdL TrackIdL IsoVL' : 'l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5 && l1Pt > 24 && l1Pt < 27',
        }

    if channel == 'mm' :
        dataFile = 'zhTrigEff_SingleMuon_nov09v3.root'
        mapper = {
            'IsoMu24 Pt Res' : '(l1Match_HLT_IsoMu24 > 0.5 || l1Match_HLT_IsoTkMu24 > 0.5) && l1Pt > 22 && l1Pt < 30',
            'Mu17 TrkIsoVVL' : '(l1Match_HLT_Mu17_TrkIsoVVL > 0.5 || l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL > 0.5) && l1Pt > 15 && l1Pt < 20',
            'Mu8 TrkIsoVVL' : '(l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL > 0.5) && l2Pt > 8 && l2Pt < 12',
        }
    
    fData = ROOT.TFile('/data/truggles/'+directory+'/'+dataFile, 'r')
    tData = fData.Get('DoubleLeptonTAPStudies/tagAndProbe/Ntuple')
    
    
    c = ROOT.TCanvas( 'c1', 'c1', 800, 700 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.8 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    
    for nBase, cut in mapper.iteritems() :
        if nBase in ['Mu8_TrkIsoVVL', 'Ele12_CaloIdL_TrackIdL_IsoVL'] :
            var = '(l2Pt-l2Level1Pt)/l2Pt'
        else :
            var = '(l1Pt-l1Level1Pt)/l1Pt'
        
        hMC = getHist( tDYJets, var, cut, 'DYJets '+nBase )
        hData = getHist( tData, var, cut, '2016 Data '+nBase )
        hMC.SetLineColor( ROOT.kRed )
        hMC.SetLineWidth( 3 )
        hData.SetLineColor( ROOT.kBlue )
        hData.SetLineWidth( 3 )
        hMC.Scale( 1. / hMC.Integral() )
        hData.Scale( 1. / hData.Integral() )
        
        hMC.SetTitle( nBase )
        hMC.Draw('HIST')
        hData.Draw('HIST SAME')
        
        hMC.SetMaximum( 1.3 * max( hMC.GetMaximum(), hData.GetMaximum() ) )
        
        legend = ROOT.TLegend(0.65, 0.33, 0.90, 0.58)
        legend.SetMargin(0.3)
        legend.SetBorderSize(0)
        legend.AddEntry( hMC, 'DYJets', 'lep')
        legend.AddEntry( hData, '2016 Data', 'lep')
        legend.Draw('SAME')
        
        c.SaveAs( plotBase+nBase.replace(' ','_')+'.png')
        
        
        
