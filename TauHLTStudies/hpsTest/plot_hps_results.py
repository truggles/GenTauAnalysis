#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)



def make_DM_plot( label='Online' ) :
    bin_label_map_mva = {
        1 : 'None',
        2 : '#pi',
        3 : '#pi#pi^{0}',
        4 : '#pi#pi^{0}#pi^{0}',
        5 : '#pi#pi',
        6 : '#pi#pi#pi^{0}',
        7 : '#pi#pi#pi',
        8 : '#pi#pi#pi#pi^{0}',
    }
    h_dm = ROOT.TH2D( 'Tau Decay Modes', 'Tau Decay Modes: Offline vs. %s;Offline #tau DM;%s #tau DM' % (label, label), 8,0,8,8,0,8 )
    for k, v in bin_label_map_mva.iteritems() :
        h_dm.GetXaxis().SetBinLabel( k, v )
        h_dm.GetYaxis().SetBinLabel( k, v )
    h_dm.GetYaxis().SetTitleOffset( h_dm.GetYaxis().GetTitleOffset() * 2 )
    h_dm.SetDirectory(0)
    return h_dm

def getDMCode( dmVal ) :
    dmMap = {
        0 : 1,
        1 : 2,
        2 : 3,
        5 : 4,
        6 : 5,
        10 : 6,
        11 : 7
    }
    if dmVal not in dmMap.keys() :
        return 0 # None bine
    else : return dmMap[ dmVal ]

# Normalize so each row = 100%
def normalize2D( th2 ) :
    for x in range( 1, th2.GetNbinsX()+1 ) :
        colTotal = 0.
        for y in range( 1, th2.GetNbinsY()+1 ) :
            colTotal += th2.GetBinContent( x, y )
        print x, colTotal
        if colTotal == 0. : continue
        for y in range( 1, th2.GetNbinsY()+1 ) :
            th2.SetBinContent( x, y, th2.GetBinContent( x, y ) / colTotal )
        


iFile = ROOT.TFile('tmp2.root','r')
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )
h_dm_hps = make_DM_plot( 'Online HPS' )
#h_dm_hps = make_DM_plot( 'Online HPS' )

trigger = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/nov29/'

c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

for row in iTree :

    # Require trigger fired or good online taus not present
    if getattr( row, trigger ) < 0.5 : continue 

    offlineDM = row.tauDM
    hpsDM = row.hpsTauDM
    defaultDM = row.defaultTauDM

    offlineCode = getDMCode( offlineDM )
    hpsCode = getDMCode( hpsDM )
    h_dm_hps.Fill( offlineCode, hpsCode )

h_dm_hps.Draw("COLZ TEXT")
ROOT.gPad.SetLogz()
c.SaveAs( plotBase+'onlinesVsHPS.png' )

#h_dm_hps.Scale( 1. / h_dm_hps.Integral() )
normalize2D( h_dm_hps )
ROOT.gPad.SetLogz(0)
c.SaveAs( plotBase+'onlinesVsHPS_norm.png' )




