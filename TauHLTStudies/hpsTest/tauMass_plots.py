#!/usr/bin/env python

import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)
from helpers import add_lumi, add_CMS, add_Preliminary
#ROOT.gStyle.SetOptStat(0)

def setOverflow( h ) :
    maxBin = h.GetXaxis().GetNbins()
    h.SetBinContent( maxBin, h.GetBinContent( maxBin ) + h.GetBinContent( maxBin+1 ) )

def plotTauMass( c, plotBase, saveTitle, plotTitle, hpsMass00, hpsMass01, hpsMass10, hpsMassOther, hpsMass, coneMass, offlineMass ) :
    c.Clear()
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.3 )
    p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.1 )
    p.SetFrameBorderMode(0)
    p.Draw()
    p.cd()

    ROOT.gStyle.SetOptStat(0)

    # All black lines
    for h in [hpsMass00, hpsMass01, hpsMass10, hpsMassOther, hpsMass, coneMass, offlineMass] :
        h.SetLineColor( ROOT.kBlack )
        h.SetLineWidth( 1 )
        setOverflow( h )

    # Scale all to A.U.
    hpsTotal = hpsMass.Integral()
    for h in [hpsMass00, hpsMass01, hpsMass10, hpsMassOther] :
        h.Scale( 1. / hpsTotal )
    for h in [hpsMass, coneMass, offlineMass] :
        h.Scale( 1. / h.Integral() )
    
        
    stack = ROOT.THStack()
    hpsMass00.SetFillColor( ROOT.TColor.GetColor(248,206,104) )
    stack.Add( hpsMass00 )
    hpsMass01.SetFillColor( ROOT.TColor.GetColor(248,206,104)-1 )
    stack.Add( hpsMass01 )
    hpsMass10.SetFillColor( ROOT.TColor.GetColor(248,206,104)-2 )
    stack.Add( hpsMass10 )
    hpsMassOther.SetFillColor( ROOT.TColor.GetColor(248,206,104)+6 )
    stack.Add( hpsMassOther )

    hpsMass.SetLineWidth( 3 )
    #hpsMass.SetLineWidth( 4 )
    hpsMass.SetTitle( plotTitle )
    #coneMass.SetLineWidth( 3 )
    coneMass.SetLineWidth( 4 )
    coneMass.SetLineStyle( 2 )
    #coneMass.SetLineColor( ROOT.kMagenta )
    #coneMass.SetLineColor( ROOT.kRed )
    coneMass.SetLineColor( ROOT.kBlue )
    #offlineMass.SetLineWidth( 3 )
    offlineMass.SetLineWidth( 4 )
    offlineMass.SetLineStyle( 9 )
    offlineMass.SetLineColor( ROOT.kCyan-3 )


    hpsMass.GetYaxis().SetTitle('A.U.')
    hpsMass.SetTitle('')
    hpsMass.Draw('hist')
    stack.Draw('hist same')
    hpsMass.Draw('hist same')
    offlineMass.Draw('hist same')
    coneMass.Draw('hist same')
    
    leg = buildLegend( [hpsMass00, hpsMass01, hpsMass10, hpsMassOther, hpsMass, coneMass, offlineMass], 
        ['Online HPS 1-prong', 'Online HPS 1-prong+1#pi^{0}', 'Online HPS 3-prong', 'Online HPS other', 'Online HPS Total', 'Online Cone-based Total', 'Offline HPS Total'], hpsMass=True )
    leg.Draw()


    lumi = add_lumi("14.3")
    lumi.Draw()
    cms = add_CMS()
    cms.Draw()
    prelim = add_Preliminary()
    prelim.Draw()

    c.SaveAs( plotBase+saveTitle+'.png' )
    c.SaveAs( plotBase+saveTitle+'.pdf' )
    c.SaveAs( plotBase+saveTitle+'.C' )
    c.SaveAs( plotBase+saveTitle+'.root' )



def buildLegend( items, names, hpsMass=False ) :
    if hpsMass :
        legend = ROOT.TLegend(0.25, 0.50, 0.83, 0.88)
        legend.SetNColumns( 2 )
    else :
        legend = ROOT.TLegend(0.5, 0.73, 0.83, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        if hpsMass :
            if 'Total' not in name :
                legend.AddEntry( item, name, 'f')
            else :
                legend.AddEntry( item, name, 'l')
        else :
            legend.AddEntry( item, name, 'lep')
    return legend



# NAME
mcName = 'dyjets_july01_mass'
dataName = 'data_hps_mass_july01'

isData = False
isData = True

mcFile = ROOT.TFile('/data/truggles/'+mcName+'.root','r')
print "MC File: ",mcFile
mcTree = mcFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )
dataFile = ROOT.TFile('/data/truggles/'+dataName+'.root','r')
print "MC File: ",dataFile
dataTree = dataFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/tau_mass/'+dataName+'vX/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )

c = ROOT.TCanvas( 'c1', 'c1', 700, 600 ) 


# nvtx
mc_nvtx = ROOT.TH1D('mc_nvtx', 'mc_nvtx;nvtx;Events', 40, 0, 80 )
mc_hpsMass00 = ROOT.TH1D('mc_hpsMass00', 'mc_hpsMass00;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_hpsMass01 = ROOT.TH1D('mc_hpsMass01', 'mc_hpsMass01;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_hpsMass10 = ROOT.TH1D('mc_hpsMass10', 'mc_hpsMass10;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_hpsMassOther = ROOT.TH1D('mc_hpsMassOther', 'mc_hpsMassOther;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_hpsMass = ROOT.TH1D('mc_hpsMass', 'mc_hpsMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_coneMass = ROOT.TH1D('mc_coneMass', 'mc_coneMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
mc_offlineMass = ROOT.TH1D('mc_offlineMass', 'mc_offlineMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )

data_nvtx = ROOT.TH1D('data_nvtx', 'data_nvtx;nvtx;Events', 40, 0, 80 )
data_hpsMass00 = ROOT.TH1D('data_hpsMass00', 'data_hpsMass00;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_hpsMass01 = ROOT.TH1D('data_hpsMass01', 'data_hpsMass01;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_hpsMass10 = ROOT.TH1D('data_hpsMass10', 'data_hpsMass10;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_hpsMassOther = ROOT.TH1D('data_hpsMassOther', 'data_hpsMassOther;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_hpsMass = ROOT.TH1D('data_hpsMass', 'data_hpsMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_coneMass = ROOT.TH1D('data_coneMass', 'data_coneMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )
data_offlineMass = ROOT.TH1D('data_offlineMass', 'data_offlineMass;#tau_{h} Mass [GeV];Events', 40, 0, 2.0 )

print "Data First"
print dataFile
print "isData? ", isData
cnt = 0
for row in dataTree :
    cnt += 1
    if cnt % 50000 == 0 : print cnt

    data_nvtx.Fill( row.nvtx )

    ''' BASIC TAG-AND-PROBE '''
    # For all events regardless
    if row.tauPt < 20 : continue
    if row.nBTag != 0 : continue
    if row.passingTaus != 1 : continue
    if row.HLT_IsoMu27 < 0.5 : continue
    if row.muonPt < 24 : continue

    # Tag
    if isData :
        if row.transMass > 40 : continue
        if row.m_vis < 40 : continue
        if row.m_vis > 100 : continue
        if row.tMVAIsoMedium < 0.5 : continue
    else :
        if row.t1_gen_match != 5 : continue
        if row.SS != 0 : continue
        if row.tMVAIsoMedium < 0.5 : continue

    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    if row.passingElectrons != 0 : continue


    if row.hpsTauMass > 0 :
        data_hpsMass.Fill( row.hpsTauMass )
        if row.hpsTauDM == 0 : data_hpsMass00.Fill( row.hpsTauMass )
        elif row.hpsTauDM == 1  : data_hpsMass01.Fill( row.hpsTauMass )
        elif row.hpsTauDM == 10  : data_hpsMass10.Fill( row.hpsTauMass )
        else : data_hpsMassOther.Fill( row.hpsTauMass )
    if row.defaultTauMass > 0 : data_coneMass.Fill( row.defaultTauMass )
    if row.hpsTauMass > 0 or row.defaultTauMass > 0 : data_offlineMass.Fill( row.tauMass )

print "MC Second"
print mcFile
isData = False
print "isData? ", isData
cnt = 0
for row in mcTree :
    cnt += 1
    if cnt % 50000 == 0 : print cnt

    mc_nvtx.Fill( row.nvtx )

    ''' BASIC TAG-AND-PROBE '''
    # For all events regardless
    if row.tauPt < 20 : continue
    if row.nBTag != 0 : continue
    if row.passingTaus != 1 : continue

    if row.HLT_IsoMu27 < 0.5 : continue
    if row.muonPt < 24 : continue

    # Tag
    if isData :
        if row.transMass > 40 : continue
        if row.m_vis < 40 : continue
        if row.m_vis > 100 : continue
        if row.tMVAIsoMedium < 0.5 : continue
    else :
        if row.t1_gen_match != 5 : continue
        if row.SS != 0 : continue
        if row.tMVAIsoMedium < 0.5 : continue

    #if row.mTrigMatch < 0.5 : continue
    if row.passingMuons != 1 : continue
    if row.nVetoMuons != 1 : continue
    if row.passingElectrons != 0 : continue


    if row.hpsTauMass > 0 :
        mc_hpsMass.Fill( row.hpsTauMass )
        if row.hpsTauDM == 0 : mc_hpsMass00.Fill( row.hpsTauMass )
        elif row.hpsTauDM == 1  : mc_hpsMass01.Fill( row.hpsTauMass )
        elif row.hpsTauDM == 10  : mc_hpsMass10.Fill( row.hpsTauMass )
        else : mc_hpsMassOther.Fill( row.hpsTauMass )
    if row.defaultTauMass > 0 : mc_coneMass.Fill( row.defaultTauMass )
    if row.hpsTauMass > 0 or row.defaultTauMass > 0 : mc_offlineMass.Fill( row.tauMass )




mc_nvtx.Draw()
ROOT.gPad.SetLogx( 0 )
c.SaveAs( plotBase+'nvtx_mc.png' )
mc_coneMass.Draw()
ROOT.gPad.SetLogx( 0 )
c.SaveAs( plotBase+'mass_cone_mc.png' )
data_nvtx.Draw()
ROOT.gPad.SetLogx( 0 )
c.SaveAs( plotBase+'nvtx_data.png' )
data_coneMass.Draw()
ROOT.gPad.SetLogx( 0 )
c.SaveAs( plotBase+'mass_cone_data.png' )

plotTauMass( c, plotBase, 'mass_comp_mc', 'HLT #tau_{h} Mass - MC ZTT', mc_hpsMass00, mc_hpsMass01, mc_hpsMass10, mc_hpsMassOther, mc_hpsMass, mc_coneMass, mc_offlineMass )


plotTauMass( c, plotBase, 'mass_comp_data', 'HLT #tau_{h} Mass - Data ZTT Enriched', data_hpsMass00, data_hpsMass01, data_hpsMass10, data_hpsMassOther, data_hpsMass, data_coneMass, data_offlineMass )

