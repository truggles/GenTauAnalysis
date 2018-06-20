#!/usr/bin/env python

import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)


#runLumiMap = {
#315357 :
#    [44,831],
#315361 :
#    [40,619],
#315363 :
#    [0,136],
#315366 :
#    [10,750],
#}


def resComp( c, name, h1, h2 ) :
    c.Clear()
    h1.SetLineColor( ROOT.kBlue )
    h1.SetLineWidth( 2 )
    if 'Gen' in h1.GetXaxis().GetTitle() :
        h1.SetTitle( 'Tau p_{T} Resolution: Gen p_{T} [30,40]' )
    else :
        h1.SetTitle( 'Tau p_{T} Resolution' )
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
    leg = buildLegend( [h1, h2], ['HPS', 'Cone-based'] )
    leg.Draw()

    h1.GetYaxis().SetTitleOffset( h1.GetYaxis().GetTitleOffset() * 1.5 )
    c.SaveAs( plotBase+name+'.png' )
    c.Clear()


def buildLegend( items, names, big=False ) :
    if not big :
        #legend = ROOT.TLegend(0.5, 0.73, 0.83, 0.88)
        legend = ROOT.TLegend(0.35, 0.31, 0.8, 0.48)
    else :
        #legend = ROOT.TLegend(0.35, 0.73, 0.83, 0.88)
        legend = ROOT.TLegend(0.35, 0.31, 0.8, 0.48)
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
    #mg.SetTitle( name )
    mg.SetTitle( "" )
    legItems = []
    legNames = []
    #if 'di-Tau Efficiency' in name :
    #    for h in h_denoms :
    #        if h.GetTitle() == 'Cone-based' :
    #            h.SetTitle( 'Cone-based: All Fully Enabled' ) 
    #        if h.GetTitle() == 'HPS Tau' :
    #            h.SetTitle( 'HPS Tau: pT 35, Med. Iso. WP' ) 
    count = 0
    for denom, passing in zip( h_denoms, h_passes ) :

        g = ROOT.TGraphAsymmErrors( passing, denom )
        g.SetLineWidth(2)
        g.SetLineColor(colors[count])
        g.SetMarkerColor(colors[count])
        mg.Add( g.Clone() )
        legItems.append( g.Clone() )
        legNames.append( denom.GetTitle() )
        count += 1

    mg.Draw('ap')
    mg.GetXaxis().SetTitle('Gen #tau p_{T} (GeV)')
    if 'offline' in name :
        mg.GetXaxis().SetTitle('Offline #tau_{h} p_{T} (GeV)')
    mg.GetXaxis().SetTitleOffset( mg.GetXaxis().GetTitleOffset() * 1.2 )
    mg.GetYaxis().SetTitle('L1 + HLT Efficiency')
    mg.SetMaximum( 1.2 )
    mg.SetMinimum( 0. )

    if isData :
        #mg.GetXaxis().SetLimits( 20., 150 )
        #mg.GetXaxis().SetLimits( 20., 200 )
        mg.GetXaxis().SetLimits( 20., 500 )
        mg.GetXaxis().SetMoreLogLabels()
        ROOT.gPad.SetLogx()
    else :
        ROOT.gPad.SetLogx()
        mg.GetXaxis().SetMoreLogLabels()
        mg.GetXaxis().SetLimits( 20., 500 )
        if 'Tau180' in name :
            mg.GetXaxis().SetLimits( 100, 750 )
    


    if 'di-Tau Efficiency' in name :
        leg = buildLegend( legItems, legNames, True )
    else :
        leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()

    #lumi = ROOT.TLatex(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi = ROOT.TLatex()
    lumi.SetTextSize(0.03)
    #lumi.DrawTextNDC(.75,.92,"2018 (13 TeV)")
    #lumi.DrawTextNDC(.5,.92,"14.3 fb^{-1} 2018 Run A (13 TeV)")
    lumi.DrawLatexNDC(.55,.91,"14.3 fb^{-1}  2018 (13 TeV)")

    #logo = ROOT.TText(.18, .92,"#bf{CMS} #it{Preliminary}")
    #logo.SetTextSize(0.03)
    #logo.DrawTextNDC(.18, .92,"#bf{CMS} #it{Preliminary}")
    lumi.SetTextSize(0.04)
    lumi.DrawLatexNDC(.16, .91,"#bf{CMS} #it{Preliminary}")
    
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.png' )
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.pdf' )
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.C' )
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.root' )



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
    ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetPaintTextFormat("4.0f")
    ROOT.gPad.SetLogz()
    th2.Draw("COLZ TEXT")
    c.SaveAs( name+'.png' )
    
    ROOT.gStyle.SetPaintTextFormat("4.2f")
    ROOT.gPad.SetLogz(0)
    
    normalize2D( th2 )
    c.SaveAs( name+'_norm.png' )

# NAME
name = 'eff_feb13_test'
name = 'eff_feb15_v90per'
name = 'eff_feb15_v60per'
name = 'eff_feb15_v30per'
name = 'eff_feb16_v60per'
name = 'feb16_tmp'
name = 'eff_feb16_v60pMT30pL_pTreset'
name = 'eff_v2_feb16_v60pMT30pL_pTreset'
name = 'outputFileName'
name = 'eff_singleMu_test'
name = 'eff_feb18'
name = 'eff_feb18_singleMuon'
#name = 'eff_qqH_feb21'
#name = 'eff_qqH_feb27'
#name = 'eff_qqH_feb27_nonReg'
#name = 'eff_Zprime1500_mar02'
#name = 'eff_DYToLL_mar03'
name = 'eff_april02'
name = 'eff_feb27x'
name = 'muTau_promptReco_May03'
name = 'singleMuon_may27'
name = 'singleMuon_may28'
name = 'outfile_10'
name = 'singleMuon_may29_cut2'
#name = 'singleMuon_june11_cut'
name = 'june20_RunA_Golden'

isData = False
isData = True


iFile = ROOT.TFile('/data/truggles/'+name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

trigger1 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'
trigger2 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1'
#trigger1 = 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr'
#trigger2 = 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr'

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'_log_v2/'
#plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'_GenJet/'
#plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'_GenEorMu/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )

c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

app1 = 'Offline vs HPS'
app2 = 'Offline vs Cone-based'
app3 = 'Gen Tau vs HPS'
app4 = 'Gen Tau vs Cone-based'
axes = ';(offline p_{T} - online p_{T})/offline p_{T};A.U.'
axesGen = ';(Gen p_{T} - online p_{T})/Gen p_{T};A.U.'
axesHPSGen = ';(Gen p_{T} - online_{HPS} p_{T})/Gen p_{T}'
axesDefGen = ';(Gen p_{T} - online_{Cone-based} p_{T})/Gen p_{T}'
minPtRes = -0.6
maxPtRes = 0.7
#ptRes1 = ROOT.TH1D('Pt Resolution '+app1, 'Pt_Resolution_'+app1.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes2 = ROOT.TH1D('Pt Resolution '+app2, 'Pt_Resolution_'+app2.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes3 = ROOT.TH1D('Pt Resolution '+app3, 'Pt_Resolution_'+app3.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
#ptRes4 = ROOT.TH1D('Pt Resolution '+app4, 'Pt_Resolution_'+app4.replace(' ','_')+axes, 50, minPtRes, maxPtRes )
ptRes1 = ROOT.TH1D('HPS', 'Pt_Resolution_'+app1.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes2 = ROOT.TH1D('Cone-based', 'Pt_Resolution_'+app2.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes3 = ROOT.TH1D('HPS', 'Pt_Resolution_'+app3.replace(' ','_')+axesGen, 100, minPtRes, maxPtRes )
ptRes4 = ROOT.TH1D('Cone-based', 'Pt_Resolution_'+app4.replace(' ','_')+axesGen, 100, minPtRes, maxPtRes )
ptRes5 = ROOT.TH1D('HPS', 'HPS'+axesGen, 100, minPtRes, maxPtRes )
ptRes6 = ROOT.TH1D('Cone-based', 'Cone-based'+axesGen, 100, minPtRes, maxPtRes )
ptRes7 = ROOT.TH1D('HPS', 'Pt_Resolution_2'+app1.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes8 = ROOT.TH1D('Cone-based', 'Pt_Resolution_2'+app2.replace(' ','_')+axes, 100, minPtRes, maxPtRes )
ptRes2DGenHPS = ROOT.TH2D( 'ptRes2DGenHPS', 'HPS Tau p_{T} Resolution vs. Gen p_{T};Gen p_{T} [GeV]'+axesHPSGen, 11,20,75,50,-.6,.6 )
ptRes2DGenDef = ROOT.TH2D( 'ptRes2DGenDef', 'HPS Tau p_{T} Resolution vs. Gen p_{T};Gen p_{T} [GeV]'+axesDefGen, 11,20,75,50,-.6,.6 )

drAxes = ';#Delta R( offline - online);A.U.'
drRes1 = ROOT.TH1D('dR Resolution '+app1, 'dR_Resolution_'+app1.replace(' ','_')+drAxes, 50, 0, 0.05)
drRes2 = ROOT.TH1D('dR Resolution '+app2, 'dR_Resolution_'+app2.replace(' ','_')+drAxes, 50, 0, 0.05)

# nvtx
nvtx = ROOT.TH1D('nvtx', 'nvtx;nvtx;Events', 40, 0, 80 )

### 2D PLOTS ###
#h_dm_offline_hps = make_DM_plot( 'Offline', 'Online HPS' )
#
#h_dm_hps_offline = make_DM_plot( 'Online HPS', 'Offline' )
#h_dm_hps_offline30to80 = make_DM_plot( 'Online HPS pt30to80', 'Offline' )
#h_dm_hps_offline80to150 = make_DM_plot( 'Online HPS pt80to150', 'Offline' )
#h_dm_hps_offline150plus = make_DM_plot( 'Online HPS pt150plus', 'Offline' )
#
#h_dm_offline_default = make_DM_plot( 'Offline', 'Online HLT Cone-based' )
#h_dm_default_offline = make_DM_plot( 'Online HLT Cone-based', 'Offline' )
#h_dm_hps_conebased = make_DM_plot( 'Online HPS', 'Online Cone-based' )
#h_dm_hps_conebased30to80 = make_DM_plot( 'Online HPS pt30to80', 'Online Cone-based' )
#h_dm_hps_conebased80to150 = make_DM_plot( 'Online HPS pt80to150', 'Online Cone-based' )
#h_dm_hps_conebased150plus = make_DM_plot( 'Online HPS pt150plus', 'Online Cone-based' )

### EFFICIENCY PLOTS ###
#binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
#    42.5,45,47.5,50,60,80,100,140])

###binning = array('d', [20,30,32.5,34,35,36,37,38,40,\
###    42.5,45,50,60,80,100,140])

if isData :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100,200,500])
    binning27 = array('d', [20,22.5,25,27.5,30,32.5,35,40,\
        45,50,60,80,100,200,500])
    binning35 = array('d', [20,25,30,32.5,35,37.5,40,\
        45,50,60,80,100,200,500])
else :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100,150,200,500])

highPtBinning = array('d', [100,150,175,200,300,400,500,750])


h_def_denom_medDiTauFull = ROOT.TH1D( 'def denom_medDiTauFull', 'Cone-based #tau_{h} Reco.', len(binning35)-1, binning35)
h_def_pass_medDiTauFull = ROOT.TH1D( 'def pass_medDiTauFull', 'def pass', len(binning35)-1, binning35)
h_def_denom_medDiTauAll = ROOT.TH1D( 'def denom_medDiTauAll', 'Cone-based #tau_{h} Reco.', len(binning35)-1, binning35)
h_def_pass_medDiTauAll = ROOT.TH1D( 'def pass_medDiTauAll', 'def pass', len(binning35)-1, binning35)

#h_def_denom_med_gen = ROOT.TH1D( 'def denom_med_gen', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_med_gen = ROOT.TH1D( 'def pass_med_gen', 'def pass', len(binning)-1, binning)
#h_hps_denom_med_gen = ROOT.TH1D( 'hps denom_med_gen', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_med_gen = ROOT.TH1D( 'hps pass_med_gen', 'hps pass', len(binning)-1, binning)

h_def_denom_loose = ROOT.TH1D( 'def denom_loose', 'Cone-based #tau_{h} Reco.', len(binning27)-1, binning27)
h_def_pass_loose = ROOT.TH1D( 'def pass_loose', 'def pass', len(binning27)-1, binning27)
h_hps_denom_loose = ROOT.TH1D( 'hps denom_loose', 'HPS #tau_{h} Reco.', len(binning27)-1, binning27)
h_hps_pass_loose = ROOT.TH1D( 'hps pass_loose', 'hps pass', len(binning27)-1, binning27)

#h_def_denom_loose_TightID = ROOT.TH1D( 'def denom_loose_TightID', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_loose_TightID = ROOT.TH1D( 'def pass_loose_TightID', 'def pass', len(binning)-1, binning)
#h_hps_denom_loose_TightID = ROOT.TH1D( 'hps denom_loose_TightID', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_loose_TightID = ROOT.TH1D( 'hps pass_loose_TightID', 'hps pass', len(binning)-1, binning)

h_def_denom_med = ROOT.TH1D( 'def denom_med', 'Cone-based #tau_{h} Reco.', len(binning35)-1, binning35)
h_def_pass_med = ROOT.TH1D( 'def pass_med', 'def pass', len(binning35)-1, binning35)
h_hps_denom_med = ROOT.TH1D( 'hps denom_med', 'HPS #tau_{h} Reco.', len(binning35)-1, binning35)
h_hps_pass_med = ROOT.TH1D( 'hps pass_med', 'hps pass', len(binning35)-1, binning35)

h_def_denom_med_muTau = ROOT.TH1D( 'def denom_med_muTau', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
h_def_pass_med_muTau = ROOT.TH1D( 'def pass_med_muTau', 'def pass', len(binning)-1, binning)
h_hps_denom_med_muTau = ROOT.TH1D( 'hps denom_med_muTau', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
h_hps_pass_med_muTau = ROOT.TH1D( 'hps pass_med_muTau', 'hps pass', len(binning)-1, binning)

#h_def_denom_med_muTau_TightID = ROOT.TH1D( 'def denom_med_muTau_TightID', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_med_muTau_TightID = ROOT.TH1D( 'def pass_med_muTau_TightID', 'def pass', len(binning)-1, binning)
#h_hps_denom_med_muTau_TightID = ROOT.TH1D( 'hps denom_med_muTau_TightID', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_med_muTau_TightID = ROOT.TH1D( 'hps pass_med_muTau_TightID', 'hps pass', len(binning)-1, binning)

h_def_denom_tight = ROOT.TH1D( 'def denom_tight', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
h_def_pass_tight = ROOT.TH1D( 'def pass_tight', 'def pass', len(binning)-1, binning)
h_hps_denom_tight = ROOT.TH1D( 'hps denom_tight', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
h_hps_pass_tight = ROOT.TH1D( 'hps pass_tight', 'hps pass', len(binning)-1, binning)

h_def_denom_tight_muTau = ROOT.TH1D( 'def denom_tight_muTau', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
h_def_pass_tight_muTau = ROOT.TH1D( 'def pass_tight_muTau', 'def pass', len(binning)-1, binning)
h_hps_denom_tight_muTau = ROOT.TH1D( 'hps denom_tight_muTau', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
h_hps_pass_tight_muTau = ROOT.TH1D( 'hps pass_tight_muTau', 'hps pass', len(binning)-1, binning)

#h_def_denom_tight_muTau_TightID = ROOT.TH1D( 'def denom_tight_muTau_TightID', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_tight_muTau_TightID = ROOT.TH1D( 'def pass_tight_muTau_TightID', 'def pass', len(binning)-1, binning)
#h_hps_denom_tight_muTau_TightID = ROOT.TH1D( 'hps denom_tight_muTau_TightID', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_tight_muTau_TightID = ROOT.TH1D( 'hps pass_tight_muTau_TightID', 'hps pass', len(binning)-1, binning)
#
#h_def_denom_med_muTau50_1pr_dm01 = ROOT.TH1D( 'def denom_med_muTau50_1pr_dm01', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_med_muTau50_1pr_dm01 = ROOT.TH1D( 'def pass_med_muTau50_1pr_dm01', 'def pass', len(binning)-1, binning)
#h_hps_denom_med_muTau50_1pr_dm01 = ROOT.TH1D( 'hps denom_med_muTau50_1pr_dm01', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_med_muTau50_1pr_dm01 = ROOT.TH1D( 'hps pass_med_muTau50_1pr_dm01', 'hps pass', len(binning)-1, binning)
#
#h_def_denom_med_muTau50_1pr = ROOT.TH1D( 'def denom_med_muTau50_1pr', 'Cone-based #tau_{h} Reco.', len(binning)-1, binning)
#h_def_pass_med_muTau50_1pr = ROOT.TH1D( 'def pass_med_muTau50_1pr', 'def pass', len(binning)-1, binning)
#h_hps_denom_med_muTau50_1pr = ROOT.TH1D( 'hps denom_med_muTau50_1pr', 'HPS #tau_{h} Reco.', len(binning)-1, binning)
#h_hps_pass_med_muTau50_1pr = ROOT.TH1D( 'hps pass_med_muTau50_1pr', 'hps pass', len(binning)-1, binning)
#
#h_def_denom_med_muTau180 = ROOT.TH1D( 'def denom_med_muTau180', 'Cone-based #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_def_pass_med_muTau180 = ROOT.TH1D( 'def pass_med_muTau180', 'def pass', len(highPtBinning)-1, highPtBinning)
#h_hps_denom_med_muTau180 = ROOT.TH1D( 'hps denom_med_muTau180', 'HPS #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_hps_pass_med_muTau180 = ROOT.TH1D( 'hps pass_med_muTau180', 'hps pass', len(highPtBinning)-1, highPtBinning)
#
#h_def_denom_med_muTau180_dm01 = ROOT.TH1D( 'def denom_med_muTau180_dm01', 'Cone-based #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_def_pass_med_muTau180_dm01 = ROOT.TH1D( 'def pass_med_muTau180_dm01', 'def pass', len(highPtBinning)-1, highPtBinning)
#h_hps_denom_med_muTau180_dm01 = ROOT.TH1D( 'hps denom_med_muTau180_dm01', 'HPS #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_hps_pass_med_muTau180_dm01 = ROOT.TH1D( 'hps pass_med_muTau180_dm01', 'hps pass', len(highPtBinning)-1, highPtBinning)
#
#h_def_denom_med_muTau180_1pr = ROOT.TH1D( 'def denom_med_muTau180_1pr', 'Cone-based #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_def_pass_med_muTau180_1pr = ROOT.TH1D( 'def pass_med_muTau180_1pr', 'def pass', len(highPtBinning)-1, highPtBinning)
#h_hps_denom_med_muTau180_1pr = ROOT.TH1D( 'hps denom_med_muTau180_1pr', 'HPS #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_hps_pass_med_muTau180_1pr = ROOT.TH1D( 'hps pass_med_muTau180_1pr', 'hps pass', len(highPtBinning)-1, highPtBinning)
#
#h_def_denom_med_muTau180_1pr_dm01 = ROOT.TH1D( 'def denom_med_muTau180_1pr_dm01', 'Cone-based #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_def_pass_med_muTau180_1pr_dm01 = ROOT.TH1D( 'def pass_med_muTau180_1pr_dm01', 'def pass', len(highPtBinning)-1, highPtBinning)
#h_hps_denom_med_muTau180_1pr_dm01 = ROOT.TH1D( 'hps denom_med_muTau180_1pr_dm01', 'HPS #tau_{h} Reco.', len(highPtBinning)-1, highPtBinning)
#h_hps_pass_med_muTau180_1pr_dm01 = ROOT.TH1D( 'hps pass_med_muTau180_1pr_dm01', 'hps pass', len(highPtBinning)-1, highPtBinning)


for row in iTree :

    nvtx.Fill( row.nvtx )

    ''' BASIC TAG-AND-PROBE '''
    if row.muonPt < 20 : continue
    if row.tauPt < 20 : continue

    # Tag
    if isData :
        if row.HLT_IsoMu27 < 0.5 and row.HLT_IsoMu24 < 0.5 : continue
        if row.muonPt < 24 : continue
        if row.transMass > 40 : continue
        if row.m_vis < 40 : continue
        if row.m_vis > 80 : continue
        if row.tMVAIsoLoose < 0.5 : continue
        #if row.tMVAIsoMedium < 0.5 : continue
        #if row.tMVAIsoTight < 0.5 : continue
        #if row.RunNumber not in runLumiMap.keys() : continue
        #if row.lumi < runLumiMap[ row.RunNumber ][0] : continue
        #if row.lumi > runLumiMap[ row.RunNumber ][1] : continue
        
    else :
        if row.HLT_IsoMu20 < 0.5 : continue
        #if row.muonPt < 25 : continue
        if row.t1_gen_match != 5 : continue
        #if row.t1_gen_match > 4 : continue
        #if row.t1_gen_match < 6 : continue
        if row.SS != 0 : continue
        if row.tMVAIsoMedium < 0.5 : continue

    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    if row.passingElectrons != 0 : continue
    if row.nBTag != 0 : continue
    if row.passingTaus != 1 : continue

    tPt = row.tauPt
    hpsPt = row.hpsTauPt
    defPt = row.defaultTauPt
    genTauPt = row.genTauPt
    if genTauPt < 0.1 : genTauPt = 1.
    if tPt < 0.1 : tPt = 1.
    if hpsPt < 0.1 : hpsPt = 1.
    if defPt < 0.1 : defPt = 1.
    tDM = row.tauDM

    ''' Increase min muon pT for matching to Tau35 triggers '''
    #if row.HLT_IsoMu24 > 0.5 and row.muonPt > 24 :
    if row.muonPt > 25 :
        #if row.tMVAIsoTight < 0.5 : continue
        weight = 1. if row.SS == 0 else -1.

        ''' Fill efficiencies '''
        h_def_denom_medDiTauFull.Fill( tPt, weight )
        h_def_denom_medDiTauAll.Fill( tPt, weight )
        #h_def_denom_med_gen.Fill( genTauPt, weight ) 
        #h_hps_denom_med_gen.Fill( genTauPt, weight )
        h_def_denom_loose.Fill( tPt, weight ) 
        h_hps_denom_loose.Fill( tPt, weight )
        #h_def_denom_loose_TightID.Fill( tPt, weight ) 
        #h_hps_denom_loose_TightID.Fill( tPt, weight )
        h_def_denom_med.Fill( tPt, weight ) 
        h_hps_denom_med.Fill( tPt, weight )
        h_def_denom_med_muTau.Fill( tPt, weight ) 
        h_hps_denom_med_muTau.Fill( tPt, weight )
        #h_def_denom_med_muTau_TightID.Fill( tPt, weight ) 
        #h_hps_denom_med_muTau_TightID.Fill( tPt, weight )
        #h_def_denom_med_muTau50_1pr.Fill( tPt, weight ) 
        #h_hps_denom_med_muTau50_1pr.Fill( tPt, weight )
        #h_def_denom_med_muTau180.Fill( tPt, weight ) 
        #h_hps_denom_med_muTau180.Fill( tPt, weight )
        #h_def_denom_med_muTau180_1pr.Fill( tPt, weight ) 
        #h_hps_denom_med_muTau180_1pr.Fill( tPt, weight )
        h_def_denom_tight.Fill( tPt, weight ) 
        h_hps_denom_tight.Fill( tPt, weight )
        h_def_denom_tight_muTau.Fill( tPt, weight ) 
        h_hps_denom_tight_muTau.Fill( tPt, weight )
        #h_def_denom_tight_muTau_TightID.Fill( tPt, weight ) 
        #h_hps_denom_tight_muTau_TightID.Fill( tPt, weight )

        # 1 Prong taus
        #if tDM == 0 or tDM == 1 :
        #    h_def_denom_med_muTau50_1pr_dm01.Fill( tPt, weight ) 
        #    h_hps_denom_med_muTau50_1pr_dm01.Fill( tPt, weight )
        #    h_def_denom_med_muTau180_dm01.Fill( tPt, weight ) 
        #    h_hps_denom_med_muTau180_dm01.Fill( tPt, weight )
        #    h_def_denom_med_muTau180_1pr_dm01.Fill( tPt, weight ) 
        #    h_hps_denom_med_muTau180_1pr_dm01.Fill( tPt, weight )
        #    if row.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_1pr > 0.5 :
        #        h_def_pass_med_muTau180_1pr_dm01.Fill( tPt, weight )
        #    if row.HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1_1pr > 0.5 :
        #        h_hps_pass_med_muTau180_1pr_dm01.Fill( tPt, weight )
        #    if row.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1 > 0.5 :
        #        h_def_pass_med_muTau180_dm01.Fill( tPt, weight )
        #    if row.HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1 > 0.5 :
        #        h_hps_pass_med_muTau180_dm01.Fill( tPt, weight )
        #    if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr > 0.5 :
        #        h_def_pass_med_muTau50_1pr_dm01.Fill( tPt, weight )
        #    if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr > 0.5 :
        #        h_hps_pass_med_muTau50_1pr_dm01.Fill( tPt, weight )

        ''' Check passing for numerator defaul triggers '''
        if ( (row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 and tPt > 40) or
                row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 or
                (row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 and tPt > 40) ) :
            h_def_pass_medDiTauFull.Fill( tPt, weight )
        if ( (row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 and tPt > 40) or
                row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 or
                (row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 and tPt > 40) or
                row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5) :
            h_def_pass_medDiTauAll.Fill( tPt, weight )
        if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            #h_def_pass_med_gen.Fill( genTauPt, weight )
            h_def_pass_med.Fill( tPt, weight )
        if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            h_def_pass_tight.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
            h_def_pass_loose.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_def_pass_loose_TightID.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
            h_def_pass_med_muTau.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_def_pass_med_muTau_TightID.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
            h_def_pass_tight_muTau.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_def_pass_tight_muTau_TightID.Fill( tPt, weight )
        #if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr > 0.5 :
        #    h_def_pass_med_muTau50_1pr.Fill( tPt, weight )
        #if row.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1 > 0.5 :
        #    h_def_pass_med_muTau180.Fill( tPt, weight )
        #if row.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_1pr > 0.5 :
        #    h_def_pass_med_muTau180_1pr.Fill( tPt, weight )

        ''' Check passing for numerator HPS triggers '''
        if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            #h_hps_pass_med_gen.Fill( genTauPt, weight )
            h_hps_pass_med.Fill( tPt, weight )
        if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
            h_hps_pass_tight.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
            h_hps_pass_loose.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_hps_pass_loose_TightID.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
            h_hps_pass_med_muTau.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_hps_pass_med_muTau_TightID.Fill( tPt, weight )
        if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
            h_hps_pass_tight_muTau.Fill( tPt, weight )
        #if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
        #    h_hps_pass_tight_muTau_TightID.Fill( tPt, weight )
        #if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr > 0.5 :
        #    h_hps_pass_med_muTau50_1pr.Fill( tPt, weight )
        #if row.HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1 > 0.5 :
        #    h_hps_pass_med_muTau180.Fill( tPt, weight )
        #if row.HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1_1pr > 0.5 :
        #    h_hps_pass_med_muTau180_1pr.Fill( tPt, weight )




    ## Require tau trigger fired or good online taus will not be present
    #if getattr( row, trigger1 ) < 0.5 and getattr( row, trigger2 ) < 0.5 : continue 
    #if row.tauPt < 30 : continue
    ##if row.tauPt < 50 : continue

    #offlineDM = row.tauDM
    #hpsDM = row.hpsTauDM
    #defaultDM = row.defaultTauDM

    #offlineCode = getDMCode( offlineDM )
    #hpsCode = getDMCode( hpsDM )
    #defaultCode = getDMCode( defaultDM )
    #h_dm_offline_hps.Fill( offlineCode, hpsCode )
    #h_dm_hps_offline.Fill( hpsCode, offlineCode )
    #h_dm_offline_default.Fill( offlineCode, defaultCode )
    #h_dm_default_offline.Fill( defaultCode, offlineCode )
    #h_dm_hps_conebased.Fill( hpsCode, defaultCode )
    #if row.tauPt > 30 and row.tauPt < 80 :
    #    h_dm_hps_conebased30to80.Fill( hpsCode, defaultCode )
    #    h_dm_hps_offline30to80.Fill( hpsCode, offlineCode )
    #elif row.tauPt > 80 and row.tauPt < 150 :
    #    h_dm_hps_conebased80to150.Fill( hpsCode, defaultCode )
    #    h_dm_hps_offline80to150.Fill( hpsCode, offlineCode )
    #elif row.tauPt > 150 :
    #    h_dm_hps_conebased150plus.Fill( hpsCode, defaultCode )
    #    h_dm_hps_offline150plus.Fill( hpsCode, offlineCode )

    ## Only compare pT and dR if they are both matched
    #if hpsPt > 0 and defPt > 0 :
    #    ptRes3.Fill( (genTauPt - hpsPt) / genTauPt )
    #    ptRes4.Fill( (genTauPt - defPt) / genTauPt )
    #    ptRes7.Fill( (tPt - hpsPt) / tPt )
    #    ptRes8.Fill( (tPt - defPt) / tPt )
    #    if genTauPt > 30 and genTauPt < 40 :
    #        ptRes1.Fill( (tPt - hpsPt) / tPt )
    #        ptRes2.Fill( (tPt - defPt) / tPt )
    #        ptRes5.Fill( (genTauPt - hpsPt) / genTauPt )
    #        ptRes6.Fill( (genTauPt - defPt) / genTauPt )
    #    ptRes2DGenHPS.Fill( genTauPt, ((genTauPt - hpsPt) / genTauPt) )
    #    ptRes2DGenDef.Fill( genTauPt, ((genTauPt - defPt) / genTauPt) )

    #    drRes1.Fill( row.hpsTauDR )
    #    drRes2.Fill( row.defaultTauDR )



#resComp( c, 'resolutionPt', ptRes1, ptRes2 )
#resComp( c, 'resolutionPtOnVsOff', ptRes7, ptRes8 )
#resComp( c, 'resolutionPtGen', ptRes3, ptRes4 )
#resComp( c, 'resolutionPtGenPt30to40', ptRes5, ptRes6 )
#resComp( c, 'resolutionDRGen', drRes1, drRes2 )
#
#c.Clear()
#ptRes2DGenHPS.Draw('COLZ')
#c.SaveAs( plotBase+'resolutionPt2D_Gen_HPS.png' )
#c.Clear()
#ptRes2DGenDef.Draw('COLZ')
#c.SaveAs( plotBase+'resolutionPt2D_Gen_Def.png' )
#c.Clear()


#h_denoms_med_gen = [h_def_denom_med_gen, h_hps_denom_med_gen]
#h_passes_med_gen = [h_def_pass_med_gen, h_hps_pass_med_gen]
#plotEff( c, plotBase, 'Med Iso WP: Gen pT', h_denoms_med_gen, h_passes_med_gen )

h_denoms_loose = [h_def_denom_loose, h_hps_denom_loose]
h_passes_loose = [h_def_pass_loose, h_hps_pass_loose]
plotEff( c, plotBase, 'Loose Iso WP: offline pT', h_denoms_loose, h_passes_loose )

##h_denoms_loose_TightID = [h_def_denom_loose_TightID, h_hps_denom_loose_TightID]
##h_passes_loose_TightID = [h_def_pass_loose_TightID, h_hps_pass_loose_TightID]
##plotEff( c, plotBase, 'Loose Iso TightID WP: offline pT', h_denoms_loose_TightID, h_passes_loose_TightID )
#
#h_denoms_med = [h_def_denom_med, h_hps_denom_med]
#h_passes_med = [h_def_pass_med, h_hps_pass_med]
#plotEff( c, plotBase, 'Med Iso WP: offline pT', h_denoms_med, h_passes_med )

# Make HPS comp to fully enabled cone-based
h_denoms_med = [h_def_denom_medDiTauFull, h_hps_denom_med]
h_passes_med = [h_def_pass_medDiTauFull, h_hps_pass_med]
plotEff( c, plotBase, 'di-Tau Efficiency: offline pT', h_denoms_med, h_passes_med )

### Make HPS comp to fully enabled + med 35 cone-based
##h_denoms_med = [h_def_denom_medDiTauAll, h_hps_denom_med]
##h_passes_med = [h_def_pass_medDiTauAll, h_hps_pass_med]
##plotEff( c, plotBase, 'di-Tau Efficiency: offline pT_', h_denoms_med, h_passes_med )
#
#h_denoms_med_muTau = [h_def_denom_med_muTau, h_hps_denom_med_muTau]
#h_passes_med_muTau = [h_def_pass_med_muTau, h_hps_pass_med_muTau]
#plotEff( c, plotBase, 'Med Iso WP MuTauCrossTrig: offline pT', h_denoms_med_muTau, h_passes_med_muTau )
#
##h_denoms_med_muTau_TightID = [h_def_denom_med_muTau_TightID, h_hps_denom_med_muTau_TightID]
##h_passes_med_muTau_TightID = [h_def_pass_med_muTau_TightID, h_hps_pass_med_muTau_TightID]
##plotEff( c, plotBase, 'Med Iso TightID WP MuTauCrossTrig: offline pT', h_denoms_med_muTau_TightID, h_passes_med_muTau_TightID )
#
#h_denoms_tight = [h_def_denom_tight, h_hps_denom_tight]
#h_passes_tight = [h_def_pass_tight, h_hps_pass_tight]
#plotEff( c, plotBase, 'Tight Iso WP: offline pT', h_denoms_tight, h_passes_tight )
#
#h_denoms_tight_muTau = [h_def_denom_tight_muTau, h_hps_denom_tight_muTau]
#h_passes_tight_muTau = [h_def_pass_tight_muTau, h_hps_pass_tight_muTau]
#plotEff( c, plotBase, 'Tight Iso WP MuTauCrossTrig: offline pT', h_denoms_tight_muTau, h_passes_tight_muTau )
#
##h_denoms_tight_muTau_TightID = [h_def_denom_tight_muTau_TightID, h_hps_denom_tight_muTau_TightID]
##h_passes_tight_muTau_TightID = [h_def_pass_tight_muTau_TightID, h_hps_pass_tight_muTau_TightID]
##plotEff( c, plotBase, 'Tight Iso TightID WP MuTauCrossTrig: offline pT', h_denoms_tight_muTau_TightID, h_passes_tight_muTau_TightID )
##
##h_denoms_med_muTau50_1pr_dm01 = [h_def_denom_med_muTau50_1pr_dm01, h_hps_denom_med_muTau50_1pr_dm01]
##h_passes_med_muTau50_1pr_dm01 = [h_def_pass_med_muTau50_1pr_dm01, h_hps_pass_med_muTau50_1pr_dm01]
##plotEff( c, plotBase, 'Med Iso WP MuTau50 1Prong DM 0or1: offline pT', h_denoms_med_muTau50_1pr_dm01, h_passes_med_muTau50_1pr_dm01 )
##
##h_denoms_med_muTau50_1pr = [h_def_denom_med_muTau50_1pr, h_hps_denom_med_muTau50_1pr]
##h_passes_med_muTau50_1pr = [h_def_pass_med_muTau50_1pr, h_hps_pass_med_muTau50_1pr]
##plotEff( c, plotBase, 'Med Iso WP MuTau50 1Prong: offline pT', h_denoms_med_muTau50_1pr, h_passes_med_muTau50_1pr )
##
##h_denoms_med_muTau180 = [h_def_denom_med_muTau180, h_hps_denom_med_muTau180]
##h_passes_med_muTau180 = [h_def_pass_med_muTau180, h_hps_pass_med_muTau180]
##plotEff( c, plotBase, 'Med Iso WP Tau180: offline pT', h_denoms_med_muTau180, h_passes_med_muTau180 )
##
##h_denoms_med_muTau180_dm01 = [h_def_denom_med_muTau180_dm01, h_hps_denom_med_muTau180_dm01]
##h_passes_med_muTau180_dm01 = [h_def_pass_med_muTau180_dm01, h_hps_pass_med_muTau180_dm01]
##plotEff( c, plotBase, 'Med Iso WP Tau180 DM 0or1: offline pT', h_denoms_med_muTau180_dm01, h_passes_med_muTau180_dm01 )
##
##h_denoms_med_muTau180_1pr = [h_def_denom_med_muTau180_1pr, h_hps_denom_med_muTau180_1pr]
##h_passes_med_muTau180_1pr = [h_def_pass_med_muTau180_1pr, h_hps_pass_med_muTau180_1pr]
##plotEff( c, plotBase, 'Med Iso WP Tau180 1Prong: offline pT', h_denoms_med_muTau180_1pr, h_passes_med_muTau180_1pr )
##
##h_denoms_med_muTau180_1pr_dm01 = [h_def_denom_med_muTau180_1pr_dm01, h_hps_denom_med_muTau180_1pr_dm01]
##h_passes_med_muTau180_1pr_dm01 = [h_def_pass_med_muTau180_1pr_dm01, h_hps_pass_med_muTau180_1pr_dm01]
##plotEff( c, plotBase, 'Med Iso WP Tau180 1Prong DM 0or1: offline pT', h_denoms_med_muTau180_1pr_dm01, h_passes_med_muTau180_1pr_dm01 )
#
#c.Clear()
#nvtx.Draw()
#ROOT.gPad.SetLogx( 0 )
#c.SaveAs( plotBase+'nvtx.png' )
#
#p2 = ROOT.TPad( 'p2', 'p2', 0, 0, 1, 1 )
#p2.Draw()
#p2.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
#p2.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
#p2.Draw()
#p2.cd()
#
#
#print "offlineVsHPS"
#saveHists( h_dm_offline_hps, plotBase+'offlineVsHPS' )
#print "hpsVsOffline"
#saveHists( h_dm_hps_offline, plotBase+'hpsVsOffline' )
#saveHists( h_dm_hps_offline30to80, plotBase+'hpsVsOffline30to80' )
#saveHists( h_dm_hps_offline80to150, plotBase+'hpsVsOffline80to150' )
#saveHists( h_dm_hps_offline150plus, plotBase+'hpsVsOffline150plus' )
#print "offlineVsCone-based"
#saveHists( h_dm_offline_default, plotBase+'offlineVsCone-based' )
#print "Cone-basedVsOffline"
#saveHists( h_dm_default_offline, plotBase+'defaultVsOffline' )
#print "hpsVsConeBased"
#saveHists( h_dm_hps_conebased, plotBase+'hpsVsConebased' )
#saveHists( h_dm_hps_conebased30to80, plotBase+'hpsVsConebased30to80' )
#saveHists( h_dm_hps_conebased80to150, plotBase+'hpsVsConebased80to150' )
#saveHists( h_dm_hps_conebased150plus, plotBase+'hpsVsConebased150plus' )


