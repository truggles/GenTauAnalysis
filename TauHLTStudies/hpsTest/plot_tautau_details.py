#!/usr/bin/env python

import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from TauTriggerSFs2017.TauTriggerSFs2017.getTauTriggerSFs import  getTauTriggerSFs
tauSFs = getTauTriggerSFs('medium')

def buildLegend( items, names, big=False ) :
    if not big :
        legend = ROOT.TLegend(0.5, 0.73, 0.83, 0.88)
    else :
        legend = ROOT.TLegend(0.35, 0.73, 0.83, 0.88)
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
    if 'di-Tau Efficiency' in name :
        for h in h_denoms :
            if h.GetTitle() == 'Cone-Based' :
                h.SetTitle( 'Cone-Based: All Fully Enabled' ) 
            if h.GetTitle() == 'HPS Tau' :
                h.SetTitle( 'HPS Tau: pT 35, Med. Iso. WP' ) 
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
    mg.GetXaxis().SetTitleOffset( mg.GetXaxis().GetTitleOffset() * 1.3 )
    mg.GetYaxis().SetTitle('L1 + HLT Efficiency')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )

    if isData :
        mg.GetXaxis().SetLimits( 20., 150 )
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

    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    #lumi.DrawTextNDC(.7,.96,"%.1f / fb (13 TeV)" % cmsLumi )
    lumi.DrawTextNDC(.75,.92,"2018 (13 TeV)")
    #lumi.DrawTextNDC(.15,.65,"2018, Collision Runs 315357, 315361, 315363, 315366" )
    
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
name = 'dyjets_tauTau'
name = 'dyjets_94X_june30v2'
name = 'dyjets_94X_july07v1'

iFile = ROOT.TFile('/data/truggles/'+name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )

plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/tauTau/'+name+'v2/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )

binning = array('d', [35,40,\
    45,50,60,80,100,200])

effStr1 = ';L1 + HLT Efficiency'
effStr2 = ';L1 + HLT Efficiency = #epsilon(leg1) x #epsilon(leg2)'

tauTauEffMeasured = ROOT.TH2D( 'tauTauEffMeasured', 'di-Tau Trigger Efficiency;Offline Leading #tau_{h} p_{T} [GeV];Offline Subeading #tau_{h} p_{T} [GeV]'+effStr1, len(binning)-1, binning, len(binning)-1, binning)
tauTauEffNorm = ROOT.TH2D( 'tauTauEffNorm', 'di-Tau Trigger Efficiency;Offline Leading #tau_{h} p_{T} [GeV];Offline Subeading #tau_{h} p_{T} [GeV]'+effStr1, len(binning)-1, binning, len(binning)-1, binning)
tauTauDenom = ROOT.TH2D( 'tauTauDenom', 'di-Tau Trigger Efficiency;Offline Leading #tau_{h} p_{T} [GeV];Offline Subeading #tau_{h} p_{T} [GeV]'+effStr1, len(binning)-1, binning, len(binning)-1, binning)
tauTauPassing = ROOT.TH2D( 'tauTauPassing', 'di-Tau Trigger Efficiency;Offline Leading #tau_{h} p_{T} [GeV];Offline Subeading #tau_{h} p_{T} [GeV]'+effStr1, len(binning)-1, binning, len(binning)-1, binning)
tauTauEffMeasured.Sumw2()
tauTauEffNorm.Sumw2()
tauTauDenom.Sumw2()
tauTauPassing.Sumw2()

# 40/40
tauTauDenomDR = ROOT.TH1D( 'tauTauDenomDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTauPassingDR = ROOT.TH1D( 'tauTauPassingDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTauDRSF = ROOT.TH1D( 'tauTauDRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTauNormDRSF = ROOT.TH1D( 'tauTauNormDRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTauDenomDR.Sumw2()
tauTauPassingDR.Sumw2()
tauTauDRSF.Sumw2()
tauTauNormDRSF.Sumw2()
# 35/35
tauTau3535DenomDR = ROOT.TH1D( 'tauTau3535DenomDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau3535PassingDR = ROOT.TH1D( 'tauTau3535PassingDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau3535DRSF = ROOT.TH1D( 'tauTau3535DRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau3535NormDRSF = ROOT.TH1D( 'tauTau3535NormDRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau3535DenomDR.Sumw2()
tauTau3535PassingDR.Sumw2()
tauTau3535DRSF.Sumw2()
tauTau3535NormDRSF.Sumw2()
# 50/40
tauTau5040DenomDR = ROOT.TH1D( 'tauTau5040DenomDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau5040PassingDR = ROOT.TH1D( 'tauTau5040PassingDR', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau5040DRSF = ROOT.TH1D( 'tauTau5040DRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau5040NormDRSF = ROOT.TH1D( 'tauTau5040NormDRSF', 'di-Tau Trigger Efficiency;#Delta R(#tau1, #tau2)'+effStr1, 10, 0, 5)
tauTau5040DenomDR.Sumw2()
tauTau5040PassingDR.Sumw2()
tauTau5040DRSF.Sumw2()
tauTau5040NormDRSF.Sumw2()



# nvtx
nvtx = ROOT.TH1D('nvtx', 'nvtx;nvtx;Events', 40, 0, 80 )

cnt = 0
for row in iTree :
    cnt += 1
    if cnt % 100000 == 0 : print cnt

    nvtx.Fill( row.nvtx )

    ''' BASIC TAG-AND-PROBE '''
    if row.tauPt < 30 : continue
    if row.t2Pt < 30 : continue

        
    if row.t1_gen_match != 5 : continue
    if row.t2_gen_match != 5 : continue
    if row.tMVAIsoMedium < 0.5 : continue
    if row.t2MVAIsoMedium < 0.5 : continue

    if row.passingMuons > 0.5 : continue
    if row.nVetoMuons > 0.5 : continue
    if row.passingElectrons != 0 : continue
    if row.nBTag != 0 : continue

    t1Pt = row.tauPt
    t1Eta = row.tauEta
    t1Phi = row.tauPhi
    t2Pt = row.t2Pt
    t2Eta = row.t2Eta
    t2Phi = row.t2Phi
    dr = row.leptonDR_t1_t2


    ''' Fill efficiencies '''
    tauTauDenom.Fill( t1Pt, t2Pt )
    tauTauEffMeasured.Fill( t1Pt, t2Pt, (tauSFs.getDiTauEfficiencyMC( t1Pt, t1Eta, t1Phi) * \
        tauSFs.getDiTauEfficiencyMC( t2Pt, t2Eta, t2Phi )) )
    tauTauEffNorm.Fill( t1Pt, t2Pt )

    if row.tauPt > 35 and row.t2Pt > 35 :
        tauTau3535DenomDR.Fill( dr )
        tauTau3535DRSF.Fill( dr, (tauSFs.getDiTauEfficiencyMC( t1Pt, t1Eta, t1Phi) * \
            tauSFs.getDiTauEfficiencyMC( t2Pt, t2Eta, t2Phi )) )
        tauTau3535NormDRSF.Fill( dr )
    if row.tauPt > 40 and row.t2Pt > 40 :
        tauTauDenomDR.Fill( dr )
        tauTauDRSF.Fill( dr, (tauSFs.getDiTauEfficiencyMC( t1Pt, t1Eta, t1Phi ) * \
            tauSFs.getDiTauEfficiencyMC( t2Pt, t2Eta, t2Phi )) )
        tauTauNormDRSF.Fill( dr )
    if row.tauPt > 50 and row.t2Pt > 40 :
        tauTau5040DenomDR.Fill( dr )
        tauTau5040DRSF.Fill( dr, (tauSFs.getDiTauEfficiencyMC( t1Pt, t1Eta, t1Phi) * \
            tauSFs.getDiTauEfficiencyMC( t2Pt, t2Eta, t2Phi )) )
        tauTau5040NormDRSF.Fill( dr )



    ''' Check passing for numerator defaul triggers '''
    if ( (row.l1TauPt > 32 and row.l1Tau2Pt > 32) and
            ( row.HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg > 0.5 or
            row.HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg > 0.5 or
            row.HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg > 0.5) ) :
        tauTauPassing.Fill( t1Pt, t2Pt )
        # 1D
        if row.tauPt > 35 and row.t2Pt > 35 :
            tauTau3535PassingDR.Fill( dr )
        if row.tauPt > 40 and row.t2Pt > 40 :
            tauTauPassingDR.Fill( dr )
        if row.tauPt > 50 and row.t2Pt > 40 :
            tauTau5040PassingDR.Fill( dr )

tauTauPassing.Divide( tauTauDenom )
tauTauPassing.GetZaxis().SetTitleOffset( tauTauPassing.GetZaxis().GetTitleOffset() * 1.3 )
tauTauPassing.GetZaxis().SetRangeUser( 0.0, 1.0 )

c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.3 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.6 )
p.Draw()
p.cd()

tauTauPassing.Draw('COLZ')
c.SaveAs( plotBase+'di-Tau_eff_2D.png' )
#fTmp = ROOT.TFile('tmp.root','RECREATE')
#fTmp.cd()
#tauTauPassing.SetTitle('di-tau_eff_from_MC')
#tauTauPassing.SetName('di-tau_eff_from_MC')
#tauTauPassing.Write()
#fTmp.Close()

tauTauEffMeasured.Divide( tauTauEffNorm )
tauTauEffMeasured.GetZaxis().SetTitleOffset( tauTauEffMeasured.GetZaxis().GetTitleOffset() * 1.3 )
tauTauEffMeasured.GetZaxis().SetRangeUser( 0.0, 1.0 )
tauTauEffMeasured.Draw('COLZ')
c.SaveAs( plotBase+'di-Tau_eff_2D_from_SFs.png' )

tauTauEffMeasured.Divide( tauTauPassing )
tauTauEffMeasured.GetZaxis().SetTitle( 'Eff. from #mu#tau SFs / Eff. from #tau#tau MC' )
tauTauEffMeasured.GetZaxis().SetRangeUser( 0.6, 1.1 )
tauTauEffMeasured.SetTitle( 'di-Tau Efficiency' )
ROOT.gStyle.SetPaintTextFormat("4.2f")
tauTauEffMeasured.Draw('COLZ TEXT')
c.SaveAs( plotBase+'di-Tau_eff_2D_SF_over_MC.png' )
p.SetLogx()
p.SetLogy()
tauTauEffMeasured.Draw('COLZ TEXT')
c.SaveAs( plotBase+'di-Tau_eff_2D_SF_over_MC_log.png' )
p.SetLogx(0)
p.SetLogy(0)


# 1D REgion
tauTauPassingDR.Divide( tauTauDenomDR )
tauTauDRSF.Divide( tauTauNormDRSF )
tauTau3535PassingDR.Divide( tauTau3535DenomDR )
tauTau3535DRSF.Divide( tauTau3535NormDRSF )
tauTau5040PassingDR.Divide( tauTau5040DenomDR )
tauTau5040DRSF.Divide( tauTau5040NormDRSF )
# DR 1D 40/40 - repeate twice for TGaxis is problem
tauTauComp = tauTauPassingDR.Clone()
tauTauComp.Sumw2()
tauTauComp.Divide( tauTauDRSF )

tauTauPassingDR.SetLineColor( ROOT.kBlack )
tauTauDRSF.SetLineColor( ROOT.kRed )
tauTauComp.SetLineColor( ROOT.kBlue )
tauTauPassingDR.SetLineWidth( 2 )
tauTauDRSF.SetLineWidth( 2 )
tauTauComp.SetLineWidth( 2 )

tauTauPassingDR.SetMaximum( 1.8 )
tauTauPassingDR.SetMinimum( 0.0 )

# draw an axis on the right side
tauTauPassingDR.Draw('e1 p')
rightmax = tauTauPassingDR.GetMaximum()
newAxis = ROOT.TGaxis(p.GetUxmax(), p.GetUymin(), p.GetUxmax(), p.GetUymax(), 0, rightmax, 510, "+L");
newAxis.SetLineColor(ROOT.kBlue)
newAxis.SetLabelSize( tauTauPassingDR.GetYaxis().GetLabelSize() )
newAxis.SetTitleSize( tauTauPassingDR.GetYaxis().GetTitleSize() )
newAxis.SetTitleOffset( 1.3 )
newAxis.SetTitle('#tau#tau MC Eff. / #mu#tau SFs Eff.')

tauTauPassingDR.Draw('e1 p same')
tauTauDRSF.Draw('e1 p same')
tauTauComp.Draw('e1 p same')
newAxis.Draw()

legItems = [tauTauPassingDR, tauTauDRSF, tauTauComp]
legNames = ['#tau#tau MC Eff.', 'From #mu#tau SFs', '#tau#tau MC Eff. / #mu#tau SFs Eff.']
leg = buildLegend( legItems, legNames, True )
leg.Draw()

c.SaveAs( plotBase+'di-Tau_eff_DR_Cmb_4040.png' )

# DR 1D 40/40 - repeate twice for TGaxis is problem
# draw an axis on the right side
rightmax = tauTauPassingDR.GetMaximum()
newAxis = ROOT.TGaxis(p.GetUxmax(), p.GetUymin(), p.GetUxmax(), p.GetUymax(), 0, rightmax, 510, "+L");
newAxis.SetLineColor(ROOT.kBlue)
newAxis.SetLabelSize( tauTauPassingDR.GetYaxis().GetLabelSize() )
newAxis.SetTitleSize( tauTauPassingDR.GetYaxis().GetTitleSize() )
newAxis.SetTitleOffset( 1.3 )
newAxis.SetTitle('#tau#tau MC Eff. / #mu#tau SFs Eff.')

tauTauPassingDR.Draw('e1 p')
tauTauDRSF.Draw('e1 p same')
tauTauComp.Draw('e1 p same')
newAxis.Draw()

legItems = [tauTauPassingDR, tauTauDRSF, tauTauComp]
legNames = ['#tau#tau MC Eff.', 'From #mu#tau SFs', '#tau#tau MC Eff. / #mu#tau SFs Eff.']
leg = buildLegend( legItems, legNames, True )
leg.Draw()

c.SaveAs( plotBase+'di-Tau_eff_DR_Cmb_4040.png' )

# DR 1D 35/35
tauTau3535Comp = tauTau3535PassingDR.Clone()
tauTau3535Comp.Sumw2()
tauTau3535Comp.Divide( tauTau3535DRSF )

tauTau3535PassingDR.SetLineColor( ROOT.kBlack )
tauTau3535DRSF.SetLineColor( ROOT.kRed )
tauTau3535Comp.SetLineColor( ROOT.kBlue )
tauTau3535PassingDR.SetLineWidth( 2 )
tauTau3535DRSF.SetLineWidth( 2 )
tauTau3535Comp.SetLineWidth( 2 )

tauTau3535PassingDR.SetMaximum( 1.8 )
tauTau3535PassingDR.SetMinimum( 0.0 )

# draw an axis on the right side
rightmax = tauTau3535PassingDR.GetMaximum()
newAxis = ROOT.TGaxis(p.GetUxmax(), p.GetUymin(), p.GetUxmax(), p.GetUymax(), 0, rightmax, 510, "+L");
newAxis.SetLineColor(ROOT.kBlue)
newAxis.SetLabelSize( tauTau3535PassingDR.GetYaxis().GetLabelSize() )
newAxis.SetTitleSize( tauTau3535PassingDR.GetYaxis().GetTitleSize() )
newAxis.SetTitleOffset( 1.3 )
newAxis.SetTitle('#tau#tau MC Eff. / #mu#tau SFs Eff.')

tauTau3535PassingDR.Draw('e1 p')
tauTau3535DRSF.Draw('e1 p same')
tauTau3535Comp.Draw('e1 p same')
newAxis.Draw()

legItems = [tauTau3535PassingDR, tauTau3535DRSF, tauTau3535Comp]
legNames = ['#tau#tau MC Eff.', 'From #mu#tau SFs', '#tau#tau MC Eff. / #mu#tau SFs Eff.']
leg = buildLegend( legItems, legNames, True )
leg.Draw()

c.SaveAs( plotBase+'di-Tau_eff_DR_Cmb_3535.png' )


# DR 1D 50/40
tauTau5040Comp = tauTau5040PassingDR.Clone()
tauTau5040Comp.Sumw2()
tauTau5040Comp.Divide( tauTau5040DRSF )

tauTau5040PassingDR.SetLineColor( ROOT.kBlack )
tauTau5040DRSF.SetLineColor( ROOT.kRed )
tauTau5040Comp.SetLineColor( ROOT.kBlue )
tauTau5040PassingDR.SetLineWidth( 2 )
tauTau5040DRSF.SetLineWidth( 2 )
tauTau5040Comp.SetLineWidth( 2 )

tauTau5040PassingDR.SetMaximum( 1.8 )
tauTau5040PassingDR.SetMinimum( 0.0 )

# draw an axis on the right side
rightmax = tauTau5040PassingDR.GetMaximum()
newAxis = ROOT.TGaxis(p.GetUxmax(), p.GetUymin(), p.GetUxmax(), p.GetUymax(), 0, rightmax, 510, "+L");
newAxis.SetLineColor(ROOT.kBlue)
newAxis.SetLabelSize( tauTau5040PassingDR.GetYaxis().GetLabelSize() )
newAxis.SetTitleSize( tauTau5040PassingDR.GetYaxis().GetTitleSize() )
newAxis.SetTitleOffset( 1.3 )
newAxis.SetTitle('#tau#tau MC Eff. / #mu#tau SFs Eff.')

tauTau5040PassingDR.Draw('e1 p')
tauTau5040DRSF.Draw('e1 p same')
tauTau5040Comp.Draw('e1 p same')
newAxis.Draw()

legItems = [tauTau5040PassingDR, tauTau5040DRSF, tauTau5040Comp]
legNames = ['#tau#tau MC Eff.', 'From #mu#tau SFs', '#tau#tau MC Eff. / #mu#tau SFs Eff.']
leg = buildLegend( legItems, legNames, True )
leg.Draw()

c.SaveAs( plotBase+'di-Tau_eff_DR_Cmb_5040.png' )


