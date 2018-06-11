#!/usr/bin/env python

import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetOptStat(0)

def checkBinByBin( denom, passing ) :
    for b in range( 1, denom.GetXaxis().GetNbins()+1 ) :
        if passing.GetBinContent( b ) > denom.GetBinContent( b ) :
            passing.SetBinContent( b, denom.GetBinContent( b ) )



def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.3, 0.73, 0.83, 0.88)
    legend.SetNColumns( 2 )
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend


def plotEff( c, plotBase, name, h_denoms, h_passes ) :
    c.Clear()
    c.SetGrid()

    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange, ROOT.kBlack]
    mg = ROOT.TMultiGraph()
    mg.SetTitle( name )
    legItems = []
    legNames = []
    count = 0
    for denom, passing in zip( h_denoms, h_passes ) :

        checkBinByBin( denom, passing )
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
    mg.GetYaxis().SetTitle('Efficiency')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )

    if isData :
        if 'nvtx' in name :
            mg.GetXaxis().SetLimits( 0, 80 )
        else :
            mg.GetXaxis().SetLimits( 20, 100 )
    else :
        ROOT.gPad.SetLogx()
        mg.GetXaxis().SetMoreLogLabels()
        mg.GetXaxis().SetLimits( 20., 500 )
    
    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.png' )
    c.SaveAs( plotBase+'eff_'+name.replace(':','').replace(' ','_')+'.pdf' )



# NAME
name = 'singleMuon_june10'
name = 'vinay_june11'

isData = False
isData = True

iFile = ROOT.TFile('/data/truggles/'+name+'.root','r')
print iFile
iTree = iFile.Get( 'Ntuplizer/TagAndProbe' )

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
hNvtx = ROOT.TH1D('nvtx', 'nvtx;nvtx;Events', 40, 0, 80 )


### EFFICIENCY PLOTS ###
#binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
#    42.5,45,47.5,50,60,80,100,140])

###binning = array('d', [20,30,32.5,34,35,36,37,38,40,\
###    42.5,45,50,60,80,100,140])

if isData :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,100])
else :
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100,150,200,500])
nvtxBinning = array('d', [0,20,30,40,\
    50,60,80])



l1_denom = ROOT.TH1D( 'l1 denom', 'L1', len(binning)-1, binning)
l1_pass = ROOT.TH1D( 'l1 pass', 'def pass', len(binning)-1, binning)
l2p5_denom = ROOT.TH1D( 'l2p5 denom', 'L2p5', len(binning)-1, binning)
l2p5_pass = ROOT.TH1D( 'l2p5 pass', 'def pass', len(binning)-1, binning)
l3_denom = ROOT.TH1D( 'l3 denom', 'L3', len(binning)-1, binning)
l3_pass = ROOT.TH1D( 'l3 pass', 'def pass', len(binning)-1, binning)
all_denom = ROOT.TH1D( 'all denom', 'L1 + HLT', len(binning)-1, binning)
all_pass = ROOT.TH1D( 'all pass', 'def pass', len(binning)-1, binning)
indivCmb_denom = ROOT.TH1D( 'indivCmb denom', 'L1 + HLT all pieces', len(binning)-1, binning)
indivCmb_pass = ROOT.TH1D( 'indivCmb pass', 'def pass', len(binning)-1, binning)


l1_denom_nvtx = ROOT.TH1D( 'nvtx l1 denom', 'L1', len(nvtxBinning)-1, nvtxBinning)
l1_pass_nvtx = ROOT.TH1D( 'nvtx l1 pass', 'def pass', len(nvtxBinning)-1, nvtxBinning)
l2p5_denom_nvtx = ROOT.TH1D( 'nvtx l2p5 denom', 'L2p5', len(nvtxBinning)-1, nvtxBinning)
l2p5_pass_nvtx = ROOT.TH1D( 'nvtx l2p5 pass', 'def pass', len(nvtxBinning)-1, nvtxBinning)
l3_denom_nvtx = ROOT.TH1D( 'nvtx l3 denom', 'L3', len(nvtxBinning)-1, nvtxBinning)
l3_pass_nvtx = ROOT.TH1D( 'nvtx l3 pass', 'def pass', len(nvtxBinning)-1, nvtxBinning)
all_denom_nvtx = ROOT.TH1D( 'nvtx all denom', 'L1 + HLT', len(nvtxBinning)-1, nvtxBinning)
all_pass_nvtx = ROOT.TH1D( 'nvtx all pass', 'def pass', len(nvtxBinning)-1, nvtxBinning)
indivCmb_denom_nvtx = ROOT.TH1D( 'nvtx indivCmb denom', 'L1 + HLT all pieces', len(nvtxBinning)-1, nvtxBinning)
indivCmb_pass_nvtx = ROOT.TH1D( 'nvtx indivCmb pass', 'def pass', len(nvtxBinning)-1, nvtxBinning)



for row in iTree :

    hNvtx.Fill( row.Nvtx )

    ''' BASIC TAG-AND-PROBE '''
    if row.muonPt < 20 : continue
    if row.tauPt < 20 : continue

    # Tag
    #if isData :
    #if row.HLT_IsoMu27 < 0.5 : continue
    if row.muonPt < 24 : continue
    if row.mT > 40 : continue
    if row.mVis < 40 : continue
    if row.mVis > 80 : continue
    if row.byLooseIsolationMVArun2v1DBoldDMwLT < 0.5 : continue
    #else :
    #    if row.HLT_IsoMu24 < 0.5 and row.HLT_IsoMu27 < 0.5 : continue
    #    #if row.muonPt < 25 : continue
    #    if row.t1_gen_match != 5 : continue
    #    #if row.t1_gen_match > 4 : continue
    #    #if row.t1_gen_match < 6 : continue
    #    if row.SS != 0 : continue
    #    if row.tMVAIsoMedium < 0.5 : continue

    ##if row.mTrigMatch < 0.5 : continue
    #if row.passingMuons != 1 : continue
    #if row.nVetoMuons != 1 : continue
    ##if row.passingElectrons != 0 : continue
    #if row.nBTag != 0 : continue
    #if row.passingTaus != 1 : continue

    tPt = row.tauPt
    nvtx = row.Nvtx

    ''' Increase min muon pT for matching to Tau35 triggers '''
    #if row.HLT_IsoMu24 > 0.5 and row.muonPt > 24 :
    if row.muonPt > 24 :
        #if row.tMVAIsoTight < 0.5 : continue
        weight = 1. if row.isOS == 1 else -1.

        ''' Fill efficiencies '''
        l1_denom.Fill( tPt, weight ) 
        all_denom.Fill( tPt, weight ) 
        indivCmb_denom.Fill( tPt, weight ) 

        if (row.l1tPt > 32 and row.l1tIso > 0.5) :
            l2p5_denom.Fill( tPt, weight ) 
        if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0) :
            l3_denom.Fill( tPt, weight ) 

        ''' Check passing for numerator defaul triggers '''
        #root [4] triggerNames->Scan("triggerNames","","colsize=100")
        #*******************************************************************************************************************
        #*    Row   *                                                                                         triggerNames *
        #*******************************************************************************************************************
        #*        0 *                                            HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v *
        #*        1 *                                           HLT_IsoMu27_MediumChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v *
        #*        2 *                                             HLT_IsoMu27_TightChargedIsoPFTau20_Trk1_eta2p1_SingleL_v *
        #*        3 *                                 HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v *
        #print bin(row.tauTriggerBits), bin((row.tauTriggerBits>>3)), (row.tauTriggerBits>>3)&1

        if (row.l1tPt > 32 and row.l1tIso > 0.5) :
            l1_pass.Fill( tPt, weight ) 
        if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0) :
            l2p5_pass.Fill( tPt, weight ) 
        if (row.tauTriggerBits>>3)&1 :
            l3_pass.Fill( tPt, weight ) 
        if (row.tauTriggerBits>>3)&1 :
            all_pass.Fill( tPt, weight ) 
        if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0 and (row.tauTriggerBits>>3)&1) :
            indivCmb_pass.Fill( tPt, weight ) 
        ''' Nvtx Fill efficiencies '''
        if tPt > 40 :
            l1_denom_nvtx.Fill( nvtx, weight ) 
            all_denom_nvtx.Fill( nvtx, weight ) 
            indivCmb_denom_nvtx.Fill( nvtx, weight ) 

            if (row.l1tPt > 32 and row.l1tIso > 0.5) :
                l2p5_denom_nvtx.Fill( nvtx, weight ) 
            if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0) :
                l3_denom_nvtx.Fill( nvtx, weight ) 

            ''' Check passing for numerator defaul triggers '''
            if (row.l1tPt > 32 and row.l1tIso > 0.5) :
                l1_pass_nvtx.Fill( nvtx, weight ) 
            if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0) :
                l2p5_pass_nvtx.Fill( nvtx, weight ) 
            if (row.tauTriggerBits>>3)&1 :
                l3_pass_nvtx.Fill( nvtx, weight ) 
            if (row.tauTriggerBits>>3)&1 :
                all_pass_nvtx.Fill( nvtx, weight ) 
            if (row.l1tPt > 32 and row.l1tIso > 0.5 and row.hltL2CaloJetIsoPixPt > 0 and (row.tauTriggerBits>>3)&1) :
                indivCmb_pass_nvtx.Fill( nvtx, weight ) 




denoms = [all_denom, l1_denom, l2p5_denom, l3_denom,]
passes = [all_pass, l1_pass, l2p5_pass, l3_pass,]
plotEff( c, plotBase, 'Eff By Trigger Component', denoms, passes )

denoms = [all_denom, l1_denom, l2p5_denom, l3_denom, indivCmb_denom]
passes = [all_pass, l1_pass, l2p5_pass, l3_pass, indivCmb_pass]
plotEff( c, plotBase, 'Eff By Trigger Component More', denoms, passes )

denoms = [all_denom_nvtx, l1_denom_nvtx, l2p5_denom_nvtx, l3_denom_nvtx,]
passes = [all_pass_nvtx, l1_pass_nvtx, l2p5_pass_nvtx, l3_pass_nvtx,]
plotEff( c, plotBase, 'nvtx Eff By Trigger Component', denoms, passes )

denoms = [all_denom_nvtx, l1_denom_nvtx, l2p5_denom_nvtx, l3_denom_nvtx, indivCmb_denom_nvtx]
passes = [all_pass_nvtx, l1_pass_nvtx, l2p5_pass_nvtx, l3_pass_nvtx, indivCmb_pass_nvtx]
plotEff( c, plotBase, 'nvtx Eff By Trigger Component More', denoms, passes )

