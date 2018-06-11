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
    leg = buildLegend( [h1, h2], ['HPS', 'Cone-Based'] )
    leg.Draw()

    h1.GetYaxis().SetTitleOffset( h1.GetYaxis().GetTitleOffset() * 1.5 )
    c.SaveAs( plotBase+name+'.png' )
    c.Clear()


def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.5, 0.73, 0.83, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend

def checkBinByBin( denom, passing ) :
    for b in range( 1, denom.GetXaxis().GetNbins()+1 ) :
        if passing.GetBinContent( b ) > denom.GetBinContent( b ) :
            passing.SetBinContent( b, denom.GetBinContent( b ) )

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

        print denom.GetTitle(), denom.Integral(), passing.Integral()
        checkBinByBin( denom, passing )
        print denom.GetTitle(), denom.Integral(), passing.Integral()
        g = ROOT.TGraphAsymmErrors( passing, denom )
        g.SetLineWidth(2)
        g.SetLineColor(colors[count])
        mg.Add( g.Clone() )
        legItems.append( g.Clone() )
        legNames.append( denom.GetTitle() )
        count += 1

    mg.Draw('ap')
    mg.GetXaxis().SetTitle('Offline #tau p_{T} (GeV)')
    mg.GetXaxis().SetTitleOffset( mg.GetXaxis().GetTitleOffset() * 1.3 )
    mg.GetYaxis().SetTitle('L1 + HLT Efficiency')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )

    if isData :
        mg.GetXaxis().SetLimits( 20., 100 )
    else :
        ROOT.gPad.SetLogx()
        mg.GetXaxis().SetMoreLogLabels()
        mg.GetXaxis().SetLimits( 20., 500 )
    


    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.png' )
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.pdf' )



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
name = 'eff_feb27x'
name = 'qqH_june04'
name = 'singleMuon_june10'
name = 'singleMuon_june11'

isData = False
isData = True

iFile = ROOT.TFile('/data/truggles/'+name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

trigger1 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'
trigger2 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1'

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'/'
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
app2 = 'Offline vs Cone-Based'
app3 = 'Gen Tau vs HPS'
app4 = 'Gen Tau vs Cone-Based'
axes = ';(offline p_{T} - online p_{T})/offline p_{T};A.U.'
axesGen = ';(Gen p_{T} - online p_{T})/Gen p_{T};A.U.'
axesHPSGen = ';(Gen p_{T} - online_{HPS} p_{T})/Gen p_{T}'
axesDefGen = ';(Gen p_{T} - online_{Cone-Based} p_{T})/Gen p_{T}'
minPtRes = -0.6
maxPtRes = 0.7


# nvtx
nvtx = ROOT.TH1D('nvtx', 'nvtx;nvtx;Events', 40, 0, 80 )


### EFFICIENCY PLOTS ###
#binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
#    42.5,45,47.5,50,60,80,100,140])

###binning = array('d', [20,30,32.5,34,35,36,37,38,40,\
###    42.5,45,50,60,80,100,140])

if isData :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100])
else :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100,150,200,500])

highPtBinning = array('d', [100,150,175,200,300,400,500,750])


def_denom_med = ROOT.TH1D( 'def denom_med', 'Cone-Based', len(binning)-1, binning)
def_pass_med = ROOT.TH1D( 'def pass_med', 'def pass', len(binning)-1, binning)
hps_denom_med = ROOT.TH1D( 'hps denom_med', 'HPS Tau', len(binning)-1, binning)
hps_pass_med = ROOT.TH1D( 'hps pass_med', 'hps pass', len(binning)-1, binning)
hpsNew_denom_med = ROOT.TH1D( 'hpsNew denom_med', 'HPS Tau Online', len(binning)-1, binning)
hpsNew_pass_med = ROOT.TH1D( 'hpsNew pass_med', 'hpsNew pass', len(binning)-1, binning)

#def_denom_med_TightID = ROOT.TH1D( 'def denom_med_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_med_TightID = ROOT.TH1D( 'def pass_med_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_med_TightID = ROOT.TH1D( 'hps denom_med_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_med_TightID = ROOT.TH1D( 'hps pass_med_TightID', 'hps pass', len(binning)-1, binning)

def_denom_tight = ROOT.TH1D( 'def denom_tight', 'Cone-Based', len(binning)-1, binning)
def_pass_tight = ROOT.TH1D( 'def pass_tight', 'def pass', len(binning)-1, binning)
hps_denom_tight = ROOT.TH1D( 'hps denom_tight', 'HPS Tau', len(binning)-1, binning)
hps_pass_tight = ROOT.TH1D( 'hps pass_tight', 'hps pass', len(binning)-1, binning)

#def_denom_tight_TightID = ROOT.TH1D( 'def denom_tight_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_tight_TightID = ROOT.TH1D( 'def pass_tight_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_tight_TightID = ROOT.TH1D( 'hps denom_tight_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_tight_TightID = ROOT.TH1D( 'hps pass_tight_TightID', 'hps pass', len(binning)-1, binning)

def_denom_loose_muTau = ROOT.TH1D( 'def denom_loose_muTau', 'Cone-Based', len(binning)-1, binning)
def_pass_loose_muTau = ROOT.TH1D( 'def pass_loose_muTau', 'def pass', len(binning)-1, binning)
hps_denom_loose_muTau = ROOT.TH1D( 'hps denom_loose_muTau', 'HPS Tau', len(binning)-1, binning)
hps_pass_loose_muTau = ROOT.TH1D( 'hps pass_loose_muTau', 'hps pass', len(binning)-1, binning)
hpsNew_denom_loose_muTau = ROOT.TH1D( 'hpsNew denom_loose_muTau', 'HPS Tau Online', len(binning)-1, binning)
hpsNew_pass_loose_muTau = ROOT.TH1D( 'hpsNew pass_loose_muTau', 'hpsNew pass', len(binning)-1, binning)

#def_denom_loose_muTau_TightID = ROOT.TH1D( 'def denom_loose_muTau_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_loose_muTau_TightID = ROOT.TH1D( 'def pass_loose_muTau_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_loose_muTau_TightID = ROOT.TH1D( 'hps denom_loose_muTau_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_loose_muTau_TightID = ROOT.TH1D( 'hps pass_loose_muTau_TightID', 'hps pass', len(binning)-1, binning)

def_denom_med_muTau = ROOT.TH1D( 'def denom_med_muTau', 'Cone-Based', len(binning)-1, binning)
def_pass_med_muTau = ROOT.TH1D( 'def pass_med_muTau', 'def pass', len(binning)-1, binning)
hps_denom_med_muTau = ROOT.TH1D( 'hps denom_med_muTau', 'HPS Tau', len(binning)-1, binning)
hps_pass_med_muTau = ROOT.TH1D( 'hps pass_med_muTau', 'hps pass', len(binning)-1, binning)

#def_denom_med_muTau_TightID = ROOT.TH1D( 'def denom_med_muTau_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_med_muTau_TightID = ROOT.TH1D( 'def pass_med_muTau_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_med_muTau_TightID = ROOT.TH1D( 'hps denom_med_muTau_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_med_muTau_TightID = ROOT.TH1D( 'hps pass_med_muTau_TightID', 'hps pass', len(binning)-1, binning)

def_denom_tight_muTau = ROOT.TH1D( 'def denom_tight_muTau', 'Cone-Based', len(binning)-1, binning)
def_pass_tight_muTau = ROOT.TH1D( 'def pass_tight_muTau', 'def pass', len(binning)-1, binning)
hps_denom_tight_muTau = ROOT.TH1D( 'hps denom_tight_muTau', 'HPS Tau', len(binning)-1, binning)
hps_pass_tight_muTau = ROOT.TH1D( 'hps pass_tight_muTau', 'hps pass', len(binning)-1, binning)

#def_denom_tight_muTau_TightID = ROOT.TH1D( 'def denom_tight_muTau_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_tight_muTau_TightID = ROOT.TH1D( 'def pass_tight_muTau_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_tight_muTau_TightID = ROOT.TH1D( 'hps denom_tight_muTau_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_tight_muTau_TightID = ROOT.TH1D( 'hps pass_tight_muTau_TightID', 'hps pass', len(binning)-1, binning)

def_denom_loose_mu27Tau20 = ROOT.TH1D( 'def denom_loose_mu27Tau20', 'Cone-Based', len(binning)-1, binning)
def_pass_loose_mu27Tau20 = ROOT.TH1D( 'def pass_loose_mu27Tau20', 'def pass', len(binning)-1, binning)
hps_denom_loose_mu27Tau20 = ROOT.TH1D( 'hps denom_loose_mu27Tau20', 'HPS Tau', len(binning)-1, binning)
hps_pass_loose_mu27Tau20 = ROOT.TH1D( 'hps pass_loose_mu27Tau20', 'hps pass', len(binning)-1, binning)

#def_denom_loose_mu27Tau20_TightID = ROOT.TH1D( 'def denom_loose_mu27Tau20_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_loose_mu27Tau20_TightID = ROOT.TH1D( 'def pass_loose_mu27Tau20_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_loose_mu27Tau20_TightID = ROOT.TH1D( 'hps denom_loose_mu27Tau20_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_loose_mu27Tau20_TightID = ROOT.TH1D( 'hps pass_loose_mu27Tau20_TightID', 'hps pass', len(binning)-1, binning)

def_denom_med_mu27Tau20 = ROOT.TH1D( 'def denom_med_mu27Tau20', 'Cone-Based', len(binning)-1, binning)
def_pass_med_mu27Tau20 = ROOT.TH1D( 'def pass_med_mu27Tau20', 'def pass', len(binning)-1, binning)
hps_denom_med_mu27Tau20 = ROOT.TH1D( 'hps denom_med_mu27Tau20', 'HPS Tau', len(binning)-1, binning)
hps_pass_med_mu27Tau20 = ROOT.TH1D( 'hps pass_med_mu27Tau20', 'hps pass', len(binning)-1, binning)

#def_denom_med_mu27Tau20_TightID = ROOT.TH1D( 'def denom_med_mu27Tau20_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_med_mu27Tau20_TightID = ROOT.TH1D( 'def pass_med_mu27Tau20_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_med_mu27Tau20_TightID = ROOT.TH1D( 'hps denom_med_mu27Tau20_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_med_mu27Tau20_TightID = ROOT.TH1D( 'hps pass_med_mu27Tau20_TightID', 'hps pass', len(binning)-1, binning)

def_denom_tight_mu27Tau20 = ROOT.TH1D( 'def denom_tight_mu27Tau20', 'Cone-Based', len(binning)-1, binning)
def_pass_tight_mu27Tau20 = ROOT.TH1D( 'def pass_tight_mu27Tau20', 'def pass', len(binning)-1, binning)
hps_denom_tight_mu27Tau20 = ROOT.TH1D( 'hps denom_tight_mu27Tau20', 'HPS Tau', len(binning)-1, binning)
hps_pass_tight_mu27Tau20 = ROOT.TH1D( 'hps pass_tight_mu27Tau20', 'hps pass', len(binning)-1, binning)

#def_denom_tight_mu27Tau20_TightID = ROOT.TH1D( 'def denom_tight_mu27Tau20_TightID', 'Cone-Based', len(binning)-1, binning)
#def_pass_tight_mu27Tau20_TightID = ROOT.TH1D( 'def pass_tight_mu27Tau20_TightID', 'def pass', len(binning)-1, binning)
#hps_denom_tight_mu27Tau20_TightID = ROOT.TH1D( 'hps denom_tight_mu27Tau20_TightID', 'HPS Tau', len(binning)-1, binning)
#hps_pass_tight_mu27Tau20_TightID = ROOT.TH1D( 'hps pass_tight_mu27Tau20_TightID', 'hps pass', len(binning)-1, binning)


for row in iTree :

    nvtx.Fill( row.nvtx )

    ''' BASIC TAG-AND-PROBE '''
    if row.muonPt < 20 : continue
    if row.tauPt < 20 : continue

    # Tag
    if isData :
        #if row.RunNumber < 317509 : continue
        if row.HLT_IsoMu27 < 0.5 : continue
        if row.muonPt < 24 : continue
        if row.transMass > 40 : continue
        if row.m_vis < 40 : continue
        if row.m_vis > 100 : continue
        if row.tMVAIsoLoose < 0.5 : continue
    else :
        if row.HLT_IsoMu24 < 0.5 and row.HLT_IsoMu27 < 0.5 : continue
        #if row.muonPt < 25 : continue
        if row.t1_gen_match != 5 : continue
        #if row.t1_gen_match > 4 : continue
        #if row.t1_gen_match < 6 : continue
        if row.SS != 0 : continue
        if row.tMVAIsoMedium < 0.5 : continue

    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    #if row.passingElectrons != 0 : continue
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
        # For the first 20 / fb
        if row.RunNumber < 317509 :
            # only 2 TnP paths are available for HPS before run 317509
            def_denom_loose_muTau.Fill( tPt, weight ) 
            hps_denom_loose_muTau.Fill( tPt, weight )
            def_denom_loose_mu27Tau20.Fill( tPt, weight ) 
            def_denom_med.Fill( tPt, weight ) 
            hps_denom_med.Fill( tPt, weight )

            # Cone base are not available after run run 317509
            #def_denom_loose_muTau_TightID.Fill( tPt, weight ) 
            #def_denom_med_TightID.Fill( tPt, weight ) 
            def_denom_med_muTau.Fill( tPt, weight ) 
            def_denom_med_mu27Tau20.Fill( tPt, weight ) 
            #def_denom_med_muTau_TightID.Fill( tPt, weight ) 
            def_denom_tight.Fill( tPt, weight ) 
            #def_denom_tight_TightID.Fill( tPt, weight ) 
            def_denom_tight_muTau.Fill( tPt, weight ) 
            def_denom_tight_mu27Tau20.Fill( tPt, weight ) 
            #def_denom_tight_muTau_TightID.Fill( tPt, weight ) 


            ''' Check passing for numerator defaul triggers '''
            if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
                def_pass_med.Fill( tPt, weight )
            if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
                def_pass_tight.Fill( tPt, weight )
            #if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 :
            #    def_pass_tight_TightID.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
                def_pass_loose_muTau.Fill( tPt, weight )
            if row.HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1 > 0.5 :
                def_pass_loose_mu27Tau20.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
            #    def_pass_loose_muTau_TightID.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
                def_pass_med_muTau.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
            #    def_pass_med_muTau_TightID.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1 > 0.5 :
                def_pass_tight_muTau.Fill( tPt, weight )
            if row.HLT_IsoMu27_TightChargedIsoPFTau20_Trk1_eta2p1_SingleL1 > 0.5 :
                def_pass_tight_mu27Tau20.Fill( tPt, weight )
            if row.HLT_IsoMu27_MediumChargedIsoPFTau20_Trk1_eta2p1_SingleL1 > 0.5 :
                def_pass_med_mu27Tau20.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1 > 0.5 :
            #    def_pass_tight_muTau_TightID.Fill( tPt, weight )
            #if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 :
            #    def_pass_med_TightID.Fill( tPt, weight )

            ''' Check passing for numerator HPS triggers '''
            if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
                hps_pass_med.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
                hps_pass_loose_muTau.Fill( tPt, weight )

        # Fill the new HPS triggers
        if row.RunNumber >= 317509 :
            # were not available before run 317509
            #hps_denom_loose_muTau_TightID.Fill( tPt, weight )
            #hps_denom_med_TightID.Fill( tPt, weight )
            hps_denom_med_muTau.Fill( tPt, weight )
            hps_denom_med_mu27Tau20.Fill( tPt, weight )
            #hps_denom_med_muTau_TightID.Fill( tPt, weight )
            hps_denom_tight.Fill( tPt, weight )
            #hps_denom_tight_TightID.Fill( tPt, weight )
            hps_denom_tight_muTau.Fill( tPt, weight )
            hps_denom_tight_mu27Tau20.Fill( tPt, weight )
            #hps_denom_tight_muTau_TightID.Fill( tPt, weight )
            # available before and after
            hpsNew_denom_loose_muTau.Fill( tPt, weight )
            hpsNew_denom_med.Fill( tPt, weight )
            hps_denom_loose_mu27Tau20.Fill( tPt, weight )
            if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
                hpsNew_pass_med.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
                hpsNew_pass_loose_muTau.Fill( tPt, weight )
            if row.HLT_IsoMu27_LooseChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1 > 0.5 :
                hps_pass_loose_mu27Tau20.Fill( tPt, weight )
            if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1 > 0.5 :
                hps_pass_tight.Fill( tPt, weight )
            #if row.HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 :
            #    hps_pass_med_TightID.Fill( tPt, weight )
            #if row.HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1 > 0.5 :
            #    hps_pass_tight_TightID.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
            #    hps_pass_loose_muTau_TightID.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
                hps_pass_med_muTau.Fill( tPt, weight )
            if row.HLT_IsoMu27_MediumChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1 > 0.5 :
                hps_pass_med_mu27Tau20.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
            #    hps_pass_med_muTau_TightID.Fill( tPt, weight )
            if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0.5 :
                hps_pass_tight_muTau.Fill( tPt, weight )
            if row.HLT_IsoMu27_TightChargedIsoPFTauHPS20_Trk1_eta2p1_SingleL1 > 0.5 :
                hps_pass_tight_mu27Tau20.Fill( tPt, weight )
            #if row.HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1 > 0.5 :
            #    hps_pass_tight_muTau_TightID.Fill( tPt, weight )




print "hpsNew_denom_loose_muTau",hpsNew_denom_loose_muTau.Integral()
print "hpsNew_pass_loose_muTau",hpsNew_pass_loose_muTau.Integral()


denoms_loose_muTau = [def_denom_loose_muTau, hps_denom_loose_muTau, hpsNew_denom_loose_muTau]
passes_loose_muTau = [def_pass_loose_muTau, hps_pass_loose_muTau, hpsNew_pass_loose_muTau]
plotEff( c, plotBase, 'Loose Iso WP - mu20tau27', denoms_loose_muTau, passes_loose_muTau )

denoms_loose_mu27Tau20 = [def_denom_loose_mu27Tau20, hps_denom_loose_mu27Tau20]
passes_loose_mu27Tau20 = [def_pass_loose_mu27Tau20, hps_pass_loose_mu27Tau20]
plotEff( c, plotBase, 'Loose Iso WP - mu27Tau20', denoms_loose_mu27Tau20, passes_loose_mu27Tau20 )

#denoms_loose_muTau_TightID = [def_denom_loose_muTau_TightID, hps_denom_loose_muTau_TightID]
#passes_loose_muTau_TightID = [def_pass_loose_muTau_TightID, hps_pass_loose_muTau_TightID]
#plotEff( c, plotBase, 'Loose Iso TightID WP - mu20tau27', denoms_loose_muTau_TightID, passes_loose_muTau_TightID )

denoms_med = [def_denom_med, hps_denom_med, hpsNew_denom_med]
passes_med = [def_pass_med, hps_pass_med, hpsNew_pass_med]
plotEff( c, plotBase, 'Med Iso WP - mu24tau35', denoms_med, passes_med )

#denoms_med_TightID = [def_denom_med_TightID, hps_denom_med_TightID]
#passes_med_TightID = [def_pass_med_TightID, hps_pass_med_TightID]
#plotEff( c, plotBase, 'Med Iso TightID WP - mu24tau35', denoms_med_TightID, passes_med_TightID )

denoms_med_muTau = [def_denom_med_muTau, hps_denom_med_muTau]
passes_med_muTau = [def_pass_med_muTau, hps_pass_med_muTau]
plotEff( c, plotBase, 'Med Iso WP - mu20tau27', denoms_med_muTau, passes_med_muTau )

denoms_med_mu27Tau20 = [def_denom_med_mu27Tau20, hps_denom_med_mu27Tau20]
passes_med_mu27Tau20 = [def_pass_med_mu27Tau20, hps_pass_med_mu27Tau20]
plotEff( c, plotBase, 'Med Iso WP - mu27Tau20', denoms_med_mu27Tau20, passes_med_mu27Tau20 )

#denoms_med_muTau_TightID = [def_denom_med_muTau_TightID, hps_denom_med_muTau_TightID]
#passes_med_muTau_TightID = [def_pass_med_muTau_TightID, hps_pass_med_muTau_TightID]
#plotEff( c, plotBase, 'Med Iso TightID WP - mu20tau27', denoms_med_muTau_TightID, passes_med_muTau_TightID )

denoms_tight = [def_denom_tight, hps_denom_tight]
passes_tight = [def_pass_tight, hps_pass_tight]
plotEff( c, plotBase, 'Tight Iso WP - mu24tau35', denoms_tight, passes_tight )

#denoms_tight_TightID = [def_denom_tight_TightID, hps_denom_tight_TightID]
#passes_tight_TightID = [def_pass_tight_TightID, hps_pass_tight_TightID]
#plotEff( c, plotBase, 'Tight Iso TightID WP - mu24tau35', denoms_tight_TightID, passes_tight_TightID )

denoms_tight_muTau = [def_denom_tight_muTau, hps_denom_tight_muTau]
passes_tight_muTau = [def_pass_tight_muTau, hps_pass_tight_muTau]
plotEff( c, plotBase, 'Tight Iso WP - mu20tau27', denoms_tight_muTau, passes_tight_muTau )

denoms_tight_mu27Tau20 = [def_denom_tight_mu27Tau20, hps_denom_tight_mu27Tau20]
passes_tight_mu27Tau20 = [def_pass_tight_mu27Tau20, hps_pass_tight_mu27Tau20]
plotEff( c, plotBase, 'Tight Iso WP - mu27Tau20', denoms_tight_mu27Tau20, passes_tight_mu27Tau20 )

#denoms_tight_muTau_TightID = [def_denom_tight_muTau_TightID, hps_denom_tight_muTau_TightID]
#passes_tight_muTau_TightID = [def_pass_tight_muTau_TightID, hps_pass_tight_muTau_TightID]
#plotEff( c, plotBase, 'Tight Iso TightID WP - mu20tau27', denoms_tight_muTau_TightID, passes_tight_muTau_TightID )

c.Clear()
nvtx.Draw()
ROOT.gPad.SetLogx( 0 )
c.SaveAs( plotBase+'nvtx.png' )

