#!/usr/bin/env python

import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)

def resComp( c, name, h1, h2 ) :
    c.Clear()
    h1.SetLineColor( ROOT.kBlue )
    h1.SetLineWidth( 2 )
    h1.SetTitle( 'p_{T} Resolution: Gen p_{T} [30,40]' )
    h2.SetLineColor( ROOT.kRed )
    h2.SetLineWidth( 2 )
    if h1.Integral() > 0 :
        h1.Scale( 1. / h1.Integral() )
    if h2.Integral() > 0 :
        h2.Scale( 1. / h2.Integral() )
    h1.Draw()
    h1.SetMaximum( max(h1.GetMaximum(), h2.GetMaximum()) * 1.2 )
    h2.Draw('SAMES')
    ROOT.gPad.Update()
    s1 = h1.FindObject("stats")
    s1.SetLineColor( ROOT.kBlue )
    s2 = h2.FindObject("stats")
    s2.SetLineColor( ROOT.kRed )
    y1 = s2.GetY1NDC()
    y2 = s2.GetY2NDC()
    yDiff = y2-y1
    #print "Old coords:",y1,y2
    s1.SetY1NDC(.3+2*yDiff)
    s1.SetY2NDC(.3+yDiff)
    s2.SetY1NDC(.3)
    s2.SetY2NDC(.3+yDiff)

    #ROOT.gPad.BuildLegend()
    leg = buildLegend( [h1, h2], ['HPS', 'Default'] )
    leg.Draw()

    h1.GetYaxis().SetTitleOffset( h1.GetYaxis().GetTitleOffset() * 1.5 )
    c.SaveAs( plotBase+name+'.png' )
    c.Clear()


def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.45, 0.73, 0.83, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend


def plotEff( c, plotBase, name, h_denoms, h_passes ) :
    c.Clear()
    c.SetGrid()

    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange]
    mg = ROOT.TMultiGraph()
    mg.SetTitle( name )
    legItems = []
    legNames = []
    count = 0
    for denom, passing in zip( h_denoms, h_passes ) :

        g = ROOT.TGraphAsymmErrors( passing, denom )
        g.SetLineWidth(2)
        g.SetLineColor(colors[count])
        mg.Add( g.Clone() )
        legItems.append( g.Clone() )
        legNames.append( denom.GetTitle() )
        count += 1

    mg.Draw('ap')
    mg.GetXaxis().SetTitle('Gen #tau p_{T} (GeV)')
    if 'offline' in name :
        mg.GetXaxis().SetTitle('Offline #tau p_{T} (GeV)')
    mg.GetYaxis().SetTitle('HLT Efficiency')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )

    ROOT.gPad.SetLogx()
    mg.GetXaxis().SetMoreLogLabels()
    mg.GetXaxis().SetLimits( 20., 500 )


    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    
    c.SaveAs( plotBase+'eff_'+name.replace(' ','_')+'.png' )



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


#name = 'ggH125_jan15_ptRes_iso20PerInc'
#name = 'ggH125_jan15_ptRes'
#name = 'ggH125_jan14_default'
#name = 'ggH125_jan16_0p5PtAdjIso60'
#name = 'ggH125_jan16_0p5PtAdjIso40'
#name = 'ggH125_jan17_Menu_V6'
#name = 'qqH_strebler'
#name = 'qqH_20180118v2_TS_Def'
name = 'qqH125_jan19_Menu_V6'
#name = 'qqH125_jan23_chrgIso3p7'

#iFile = ROOT.TFile('tmp2.root','r')
#iFile = ROOT.TFile('20180114v2_default.root','r')
iFile = ROOT.TFile(name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

trigger1 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'
trigger2 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1'

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )

c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

app1 = 'Offline vs HPS'
app2 = 'Offline vs Default'
app3 = 'Gen Tau vs HPS'
app4 = 'Gen Tau vs Default'
axes = ';(offline p_{T} - online p_{T})/offline p_{T};A.U.'
axesGen = ';(Gen p_{T} - online p_{T})/Gen p_{T};A.U.'
axesHPSGen = ';(Gen p_{T} - online_{HPS} p_{T})/Gen p_{T}'
axesDefGen = ';(Gen p_{T} - online_{Default} p_{T})/Gen p_{T}'
minPtRes = -0.6
maxPtRes = 0.7
#ptRes1 = ROOT.TH1D('Pt Resolution '+app1, 'Pt_Resolution_'+app1.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes2 = ROOT.TH1D('Pt Resolution '+app2, 'Pt_Resolution_'+app2.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes3 = ROOT.TH1D('Pt Resolution '+app3, 'Pt_Resolution_'+app3.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes4 = ROOT.TH1D('Pt Resolution '+app4, 'Pt_Resolution_'+app4.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
ptRes1 = ROOT.TH1D('HPS', 'Pt_Resolution_'+app1.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes2 = ROOT.TH1D('Default', 'Pt_Resolution_'+app2.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes3 = ROOT.TH1D('HPS', 'Pt_Resolution_'+app3.replace(' ','_')+axesGen, 100, minPtRes, maxPtRes )
ptRes4 = ROOT.TH1D('Default', 'Pt_Resolution_'+app4.replace(' ','_')+axesGen, 100, minPtRes, maxPtRes )
ptRes5 = ROOT.TH1D('HPS', 'HPS'+axesGen, 100, minPtRes, maxPtRes )
ptRes6 = ROOT.TH1D('Default', 'Default'+axesGen, 100, minPtRes, maxPtRes )
ptRes2DGenHPS = ROOT.TH2D( 'ptRes2DGenHPS', 'HPS Tau p_{T} Resolution vs. Gen p_{T};Gen p_{T} [GeV]'+axesHPSGen, 11,20,75,50,-.6,.6 )
ptRes2DGenDef = ROOT.TH2D( 'ptRes2DGenDef', 'HPS Tau p_{T} Resolution vs. Gen p_{T};Gen p_{T} [GeV]'+axesDefGen, 11,20,75,50,-.6,.6 )

drAxes = ';#Delta R( offline - online);A.U.'
drRes1 = ROOT.TH1D('dR Resolution '+app1, 'dR_Resolution_'+app1.replace(' ','_')+drAxes, 50, 0, 0.05)
drRes2 = ROOT.TH1D('dR Resolution '+app2, 'dR_Resolution_'+app2.replace(' ','_')+drAxes, 50, 0, 0.05)


### 2D PLOTS ###
h_dm_offline_hps = make_DM_plot( 'Offline', 'Online HPS' )
h_dm_hps_offline = make_DM_plot( 'Online HPS', 'Offline' )
h_dm_offline_default = make_DM_plot( 'Offline', 'Online HLT Default' )
h_dm_default_offline = make_DM_plot( 'Online HLT Default', 'Offline' )

### EFFICIENCY PLOTS ###
#binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
#    42.5,45,47.5,50,60,80,100,140])

###binning = array('d', [20,30,32.5,34,35,36,37,38,40,\
###    42.5,45,50,60,80,100,140])

binning = array('d', [20,25,30,35,40,\
    45,50,60,80,100,150,200,500])

h_def_denom = ROOT.TH1D( 'def denom', 'Default', len(binning)-1, binning)
h_def_pass = ROOT.TH1D( 'def pass', 'def pass', len(binning)-1, binning)
h_hps_denom = ROOT.TH1D( 'hps denom', 'HPS Tau', len(binning)-1, binning)
h_hps_pass = ROOT.TH1D( 'hps pass', 'hps pass', len(binning)-1, binning)

h_def_denom2 = ROOT.TH1D( 'def denom2', 'Default', len(binning)-1, binning)
h_def_pass2 = ROOT.TH1D( 'def pass2', 'def pass', len(binning)-1, binning)
h_hps_denom2 = ROOT.TH1D( 'hps denom2', 'HPS Tau', len(binning)-1, binning)
h_hps_pass2 = ROOT.TH1D( 'hps pass2', 'hps pass', len(binning)-1, binning)

for row in iTree :


    ''' BASIC TAG-AND-PROBE '''
    if row.muonPt < 20 : continue
    if row.tauPt < 20 : continue
    if row.HLT_IsoMu20 < 0.5 : continue
    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    if row.SS != 0 : continue
    if row.passingElectrons != 0 : continue
    if row.nBTag != 0 : continue
    if row.tMVAIsoMedium < 0.5 : continue
    if row.t1_gen_match != 5 : continue

    tPt = row.tauPt
    hpsPt = row.hpsTauPt
    defPt = row.defaultTauPt
    genTauPt = row.genTauPt
    if genTauPt < 0.1 : genTauPt = 1.
    if tPt < 0.1 : tPt = 1.
    if hpsPt < 0.1 : hpsPt = 1.
    if defPt < 0.1 : defPt = 1.

    ''' Increase min muon pT for matching to Tau35 triggers '''
    #if row.HLT_IsoMu24 > 0.5 and row.muonPt > 24 :
    if row.muonPt > 25 :
        #if row.tMVAIsoTight < 0.5 : continue

        ''' Fill efficiencies '''
        h_def_denom.Fill( genTauPt ) 
        h_hps_denom.Fill( genTauPt )
        h_def_denom2.Fill( tPt ) 
        h_hps_denom2.Fill( tPt )
        # Check passing for numerator
        if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            h_def_pass.Fill( genTauPt )
            h_def_pass2.Fill( tPt )
        if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            h_hps_pass.Fill( genTauPt )
            h_hps_pass2.Fill( tPt )




    # Require tau trigger fired or good online taus will not be present
    if getattr( row, trigger1 ) < 0.5 and getattr( row, trigger2 ) < 0.5 : continue 
    if row.tauPt < 27 : continue

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

    # Only compare pT and dR if they are both matched
    if hpsPt > 0 and defPt > 0 :
        ptRes3.Fill( (genTauPt - hpsPt) / genTauPt )
        ptRes4.Fill( (genTauPt - defPt) / genTauPt )
        if genTauPt > 30 and genTauPt < 40 :
            ptRes1.Fill( (tPt - hpsPt) / tPt )
            ptRes2.Fill( (tPt - defPt) / tPt )
            ptRes5.Fill( (genTauPt - hpsPt) / genTauPt )
            ptRes6.Fill( (genTauPt - defPt) / genTauPt )
        ptRes2DGenHPS.Fill( genTauPt, ((genTauPt - hpsPt) / genTauPt) )
        ptRes2DGenDef.Fill( genTauPt, ((genTauPt - defPt) / genTauPt) )

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



resComp( c, 'resolutionPt', ptRes1, ptRes2 )
resComp( c, 'resolutionPtGen', ptRes3, ptRes4 )
resComp( c, 'resolutionPtGenPt30to40', ptRes5, ptRes6 )
resComp( c, 'resolutionDRGen', drRes1, drRes2 )

c.Clear()
ptRes2DGenHPS.Draw('COLZ')
c.SaveAs( plotBase+'resolutionPt2D_Gen_HPS.png' )
c.Clear()
ptRes2DGenDef.Draw('COLZ')
c.SaveAs( plotBase+'resolutionPt2D_Gen_Def.png' )
c.Clear()


h_denoms = [h_def_denom, h_hps_denom]
h_passes = [h_def_pass, h_hps_pass]
plotEff( c, plotBase, 'Def vs HPS fine grain', h_denoms, h_passes )

h_denoms = [h_def_denom2, h_hps_denom2]
h_passes = [h_def_pass2, h_hps_pass2]
plotEff( c, plotBase, 'Def vs HPS: offline pT', h_denoms, h_passes )

h_denoms = [h_hps_denom2, h_def_denom2]
h_passes = [h_hps_pass2, h_def_pass2]
plotEff( c, plotBase, 'HPS vs Def fine grain offline pT', h_denoms, h_passes )




