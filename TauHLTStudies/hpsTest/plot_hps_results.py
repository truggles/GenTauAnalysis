#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)



def make_DM_plot( label1='Offline', label2='Online' ) :
    bin_label_map_mva = {
        1 : 'None',
        2 : 'Other',
        3 : '#pi',
        4 : '#pi#pi^{0}s',
        5 : '#pi#pi#pi',
        6 : '#pi#pi#pi#pi^{0}s',
    }
    h_dm = ROOT.TH2D( 'Tau Decay Modes', 'Tau Decay Modes: %s vs. %s;%s #tau DM;%s #tau DM' % (label1, label2, label1, label2), 6,0,6,6,0,6 )
    for k, v in bin_label_map_mva.iteritems() :
        h_dm.GetXaxis().SetBinLabel( k, v )
        h_dm.GetYaxis().SetBinLabel( k, v )
    h_dm.GetYaxis().SetTitleOffset( h_dm.GetYaxis().GetTitleOffset() * 2 )
    h_dm.SetDirectory(0)
    return h_dm

def getDMCode( dmVal ) :
    if dmVal == 0 : return 2
    if dmVal == 1 : return 3
    if dmVal == 2 : return 3
    if dmVal == 3 : return 3
    if dmVal == 5 : return 1
    if dmVal == 6 : return 1
    if dmVal == 7 : return 1
    if dmVal == 10 : return 4
    if dmVal > 10 : return 5
    else : return 0


# Normalize so each row = 100%
def normalize2D( th2 ) :
    total = 0.
    for x in range( 1, th2.GetNbinsX()+1 ) :
        colTotal = 0.
        for y in range( 1, th2.GetNbinsY()+1 ) :
            colTotal += th2.GetBinContent( x, y )
        print x, colTotal
        if colTotal == 0. : continue
        for y in range( 1, th2.GetNbinsY()+1 ) :
            th2.SetBinContent( x, y, th2.GetBinContent( x, y ) / colTotal )
        total += colTotal
    print "Total Entries:",total

def saveHists( th2, name ) :

    ROOT.gStyle.SetPaintTextFormat("4.0f")
    ROOT.gPad.SetLogz()
    th2.Draw("COLZ TEXT")
    c.SaveAs( name+'.png' )
    
    ROOT.gStyle.SetPaintTextFormat("4.2f")
    ROOT.gPad.SetLogz(0)
    
    normalize2D( th2 )
    c.SaveAs( name+'_norm.png' )


iFile = ROOT.TFile('tmp2.root','r')
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

trigger1 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'
trigger2 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1'

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/nov29/'

c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

app1 = 'Offline vs HPS'
app2 = 'Offline vs Default'
axes = ';(offline p_{T} - online p_{T})/offline p_{T};Events'
ptRes1 = ROOT.TH1D('Pt Resolution '+app1, 'Pt_Resolution_'+app1.replace(' ','_')+axes, 50, -1, 1.2)
ptRes2 = ROOT.TH1D('Pt Resolution '+app2, 'Pt_Resolution_'+app2.replace(' ','_')+axes, 50, -1, 1.2)

drAxes = ';#Delta R( offline - online);Events'
drRes1 = ROOT.TH1D('dR Resolution '+app1, 'dR_Resolution_'+app1.replace(' ','_')+drAxes, 50, 0, 0.05)
drRes2 = ROOT.TH1D('dR Resolution '+app2, 'dR_Resolution_'+app2.replace(' ','_')+drAxes, 50, 0, 0.05)


### 2D PLOTS ###
h_dm_offline_hps = make_DM_plot( 'Offline', 'Online HPS' )
h_dm_hps_offline = make_DM_plot( 'Online HPS', 'Offline' )
h_dm_offline_default = make_DM_plot( 'Offline', 'Online HLT Default' )
h_dm_default_offline = make_DM_plot( 'Online HLT Default', 'Offline' )

for row in iTree :

    # Require trigger fired or good online taus not present
    if getattr( row, trigger1 ) < 0.5 and getattr( row, trigger2 ) < 0.5 : continue 
    if row.muonPt < 20 : continue
    if row.tauPt < 27 : continue
    if row.HLT_IsoMu20 < 0.5 : continue
    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    if row.SS == 1 : continue
    if row.passingElectrons != 0 : continue
    if row.nBTag != 0 : continue
    if row.tMVAIsoMedium < 0.5 : continue
    if row.t1_gen_match != 5 : continue

    offlineDM = row.tauDM
    hpsDM = row.hpsTauDM
    defaultDM = row.defaultTauDM

    offlineCode = getDMCode( offlineDM )
    hpsCode = getDMCode( hpsDM )
    defaultCode = getDMCode( defaultDM )
    h_dm_offline_hps.Fill( offlineCode, hpsCode )
    h_dm_hps_offline.Fill( hpsCode, offlineCode )
    h_dm_offline_default.Fill( offlineCode, defaultCode )
    h_dm_default_offline.Fill( defaultCode, offlineCode )

    tPt = row.tauPt
    hpsPt = row.hpsTauPt
    defPt = row.defaultTauPt

    ptRes1.Fill( (tPt - hpsPt) / tPt )
    ptRes2.Fill( (tPt - defPt) / tPt )
    drRes1.Fill( row.hpsTauDR )
    drRes2.Fill( row.defaultTauDR )

print "offlineVsHPS"
saveHists( h_dm_offline_hps, plotBase+'offlineVsHPS' )
print "hpsVsOffline"
saveHists( h_dm_hps_offline, plotBase+'hpsVsOffline' )
print "offlineVsDefault"
saveHists( h_dm_offline_default, plotBase+'offlineVsDefault' )
print "DefaultVsOffline"
saveHists( h_dm_default_offline, plotBase+'defaultVsOffline' )

ptRes1.SetLineColor( ROOT.kBlack )
ptRes1.SetLineWidth( 2 )
ptRes2.SetLineColor( ROOT.kRed )
ptRes2.SetLineWidth( 2 )
ptRes1.Draw()
ptRes2.Draw('SAME')
ROOT.gPad.BuildLegend()
ptRes1.GetYaxis().SetTitleOffset( ptRes1.GetYaxis().GetTitleOffset() * 1.5 )
c.SaveAs( plotBase+'ptResolution.png' )
c.Clear()

drRes1.SetLineColor( ROOT.kBlack )
drRes1.SetLineWidth( 2 )
drRes2.SetLineColor( ROOT.kRed )
drRes2.SetLineWidth( 2 )
drRes1.Draw()
drRes2.Draw('SAME')
ROOT.gPad.BuildLegend()
drRes1.GetYaxis().SetTitleOffset( drRes1.GetYaxis().GetTitleOffset() * 1.5 )
c.SaveAs( plotBase+'drResolution.png' )






