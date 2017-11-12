#!/usr/bin/env python


doEta = False
doEta = True
doLog = True
if doEta :
    doLog = False
doNvtxComb = True


import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
from collections import OrderedDict
from math import sqrt
import copy

mm_triggers = {
#    # PROBE : [TAG,OtherCuts]
#    # NAME : [TAG,PROBE,PlotBy/ProbeBy]
   "HLT_Mu24" : ["(l2Match_HLT_Mu17_TrkIsoVVL > 0.5)", "((l1Match_HLT_IsoMu24 > 0.5 || l1Match_HLT_IsoTkMu24 > 0.5) && l1Pt > 27)", "l1Match_",27],
   #"HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Part" : ["(l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL > 0.5 && l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL > 0.5)", "(l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ > 0.5 && l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ > 0.5)","",0],
   "HLT_Mu17_TrkIsoVVL" : ["(l1Match_HLT_Mu17_TrkIsoVVL > 0.5 && l1Pt > 20)", "(l2Match_HLT_Mu17_TrkIsoVVL > 0.5)", "l2Match_",19],
   "HLT_Mu8_and_DZ" : ["(l1Match_HLT_Mu17_TrkIsoVVL > 0.5 && l1Pt > 20)", "(l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ > 0.5 || l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ > 0.5)","l2Match_",10],

   #XXX Don'tUse#"HLT_TkMu8_TrkIsoVVL_and_DZ" : ["(l1Match_HLT_Mu17_TrkIsoVVL > 0.5)", "(l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ > 0.5)","l2Match_"],
   #XXX Don'tUse#"HLT_Mu8_TrkIsoVVL_and_DZ" : ["(l1Match_HLT_Mu17_TrkIsoVVL > 0.5)", "(l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ > 0.5)","l2Match_"],
   #XXX Don'tUse#"HLT_Mu17_TrkIsoVVL_vial1" : ["(l2Match_HLT_Mu17_TrkIsoVVL > 0.5)", "(l1Match_HLT_Mu17_TrkIsoVVL > 0.5)", "l1Match_"],
   #XXX Don'tUse#"HLT_Mu8_TrkIsoVVL_self_vial1" : ["(l2Match_HLT_Mu8_TrkIsoVVL > 0.5)", "(l1Match_HLT_Mu8_TrkIsoVVL > 0.5)","l1Match_"],
}

ee_triggers = {
   "HLT_Ele27_WPTight_Gsf" : ["(l2Match_HLT_Ele27_WPTight_Gsf > 0.5)", "(l1Match_HLT_Ele27_WPTight_Gsf > 0.5)", "l1Match_",32],
   #"HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_Match" : ["(l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5 && l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5)", "(l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5 && l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5)", "",27.5],
   "HLT_Ele23_CaloIdL_TrackIdL_IsoVL" : ["(l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL > 0.5 && l2Pt > 30)", "(l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL > 0.5)", "l1Match_",27.5],
   #"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_leadingLepTagPtReq" : ["(l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5 && l1Pt > 25)", "(l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5)", "l2Match_",17.5],
   "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ" : ["(l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL > 0.5 && l1Pt > 30)", "(l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5)", "l2Match_",17.5],


   #XXX Don'tUse#"HLT_Ele12_CaloIdL_TrackIdL_IsoVL" : ["(l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5)", "(l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5)", "l1Match_"],
   #XXX Don'tUse"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_E27" : ["(l1Match_HLT_Ele27_WPTight_Gsf > 0.5)", "(l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL > 0.5)", "l2Match_"],
   #XXX Don'tUse "HLT_Ele23_CaloIdL_TrackIdL_IsoVL_vial1" : ["(l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL > 0.5)", "(l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL > 0.5)", "l2Match_"],
}

nvtxTriggers = [
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Part",
            "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",
            "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
            "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_Match",
]


def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.45, 0.73, 0.83, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend

def decorate(cmsLumi) :
    logo = ROOT.TText(.2, .85,"CMS Preliminary")
    logo.SetTextSize(0.04)
    logo.DrawTextNDC(.2, .85,"CMS Preliminary")
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.67,.91,"%.1f / fb (13 TeV)" % cmsLumi )

def getBinning( name, trigger ) :
    if trigger in nvtxTriggers :
        binning = array('d', [])
        for i in range( 0, 110, 10 ) :
            binning.append( i )
    else :
        #binning = array('d', [10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,37.5,40,\
        #    42.5,45,47.5,50,55,60,67.5,80,100,250])#,400,1000])
        if trigger == "HLT_Ele27_WPTight_Gsf" :
            binning = array('d', [5,7.5,10,12.5,15,17.5,20,22,24,26,28,30,32,34,36,40,\
                45,50,60,80,100,150,250,400])#,1000])
        elif trigger == "HLT_Mu8_and_DZ" :
            binning = array('d', [5,6,7,8,9,10,11,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,40,\
                50,60,80,100,150,250,400])#,1000])
        elif trigger == "HLT_Mu24" :
            binning = array('d', [5,7.5,10,12.5,15,17.5,20,21,22,23,24,25,26,27,28,29,30,31,32.5,35,40,\
                50,60,80,100,150,250,400])#,1000])
        elif trigger == "HLT_Mu17_TrkIsoVVL" :
            binning = array('d', [5,7.5,10,12.5,15,16,17,18,19,20,22.5,25,27.5,30,35,40,\
                50,60,80,100,150,250,400])#,1000])
        else :
            binning = array('d', [5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,35,40,\
                50,60,80,100,150,250,400])#,1000])
    return binning

def get2DBinningX( name, trigger ) :
    #binning = array('d', [10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,37.5,40,\
    #    42.5,45,47.5,50,55,60,67.5,80,100,250])#,400,1000])
    if trigger == "HLT_Ele27_WPTight_Gsf" :
        binning = array('d', [28,30,32,36,40,45,50,60,80,100,200])
    elif trigger == "HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ" :
        binning = array('d', [15,17.5,20,25,35,50,200])
    elif trigger == "HLT_Ele23_CaloIdL_TrackIdL_IsoVL" :
        binning = array('d', [25,27.5,32.5,40,50,60,80,100,200])
    elif trigger == "HLT_Mu8_and_DZ" :
        binning = array('d', [7,8,9,10,15,20,30,50,80,200])
    elif trigger == "HLT_Mu24" :
        binning = array('d', [25,27,31,35,40,60,80,100,200])
    elif trigger == "HLT_Mu17_TrkIsoVVL" :
        binning = array('d', [17,19,23,27.5,35,40,50,70,200])
    else :
        binning = array('d', [10,12.5,15,17.5,20,22.5,25,27.5,30,35,40,\
            50,60,80,200])
    return binning

def get2DHist( trigger, name ) :
    binningX = get2DBinningX( trigger, trigger )
    yTitle = 'offline #eta'
    if "Ele" in trigger :
        if trigger == 'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ' :
            binningY = array('d', [0,10,20,30,50])
            yTitle = 'nvtx'
        else :
            binningY = array('d', [-2.5,-1.5,-0.3,0.3,1.5,2.5])
    if "Mu" in trigger :
        if trigger == 'HLT_Mu8_and_DZ' :
            binningY = array('d', [0,10,20,30,50])
            yTitle = 'nvtx'
        else :
            binningY = array('d', [-2.4,-1.6,-0.8,-0.3,0.3,0.8,1.6,2.4])
    print "X",binningX
    print "Y",binningY
    h = ROOT.TH2D( name, name+trigger, len(binningX)-1, binningX, len(binningY)-1, binningY )
    h.GetXaxis().SetTitle( 'offline pT' )
    h.GetYaxis().SetTitle( yTitle )
    return h

def getHist( trees, var, cut, name, division, trigger, doEta=False ) :
    #h = ROOT.TH1D( name, name, 20, 0, 100)
    if doEta :
        #h = ROOT.TH1D( name, name+trigger, 40, -2.5, 2.5 )
        h = get2DHist( trigger, name )
    else :
        binning = getBinning( trigger, trigger )
        h = ROOT.TH1D( name, name+trigger, len(binning)-1, binning)
    #h.Sumw2()
    doCut = ''
    doCut += cut

    # Adding MC Samples
    print "Actual draw place:",var,name,doCut
    if 'DYJets' in division :
        trees['DYJets'].Draw( var+' >> '+name, doCut )
    else :
        trees['data'].Draw( var+' >> '+name, doCut )

    print name, h, h.Integral()
    
    if trigger in nvtxTriggers :
        h.GetXaxis().SetTitle('nvtx')
    else :
        h.GetXaxis().SetTitle('Offline #l1 p_{T} (GeV)')
    h.GetYaxis().SetTitle('Number of Events')
    h.SetDirectory( 0 )
    return h

# Less useful now that hists for SS are negative at the beginning
def subtractTH1( h1, h2 ) :
    h3 = h1
    h3.Add( h2 )
    h3.SetTitle( h1.GetTitle()+'_Minus_'+h2.GetTitle() )
    return h3

def addTH1( h1, h2 ) :
    h3 = h1
    h3.Add( 1 * h2 )
    h3.SetTitle( h1.GetTitle()+'_Plus_'+h2.GetTitle() )
    return h3

def checkReturnedUncert( g, g2 ) :
    print g
    x = ROOT.Double(0)
    y = ROOT.Double(0)
    for i in range( g.GetN() ) :
        # If the error calculation failed in TGraphAsymmErrors
        # take it from the "unweighted" version
        if g.GetErrorYhigh(i) == 0.0 and g.GetErrorYlow(i) == 0.0 :
            point = g.GetPoint( i, x, y )
            if y == 1.0 :
                g.SetPointEYlow( i, g2.GetErrorYlow(i) )
            elif y == 0.0 :
                g.SetPointEYlow( i, g2.GetErrorYhigh(i) )
            else :
                print "\n\n\nHaven't been here before checkReturnedUncert point not 100% or 0% \n\n\n"


def tgraphToTH1( graph, hist ) :
    x = ROOT.Double(0)
    y = ROOT.Double(0)
    for i in range( graph.GetN() ) :
        graph.GetPoint( i, x, y )
        hist.SetBinContent( hist.FindBin( x ), y )
    


def divideTH1( h1, h2, binning ) :
    ### FIXME Check bins to make sure Pass <= All
    for b in range( 1, h1.GetNbinsX()+1 ) :
        b1 =  h1.GetBinContent( b )
        b2 =  h2.GetBinContent( b )
        #print b, b1, b2
        if b1 > b2 :
            print "Bin in Numerator > Bin in Denominator",b1,b2
            print "Setting Numerator == Denominator bin"
            h2.SetBinContent( b, b1 )
            h2.SetBinError( b, h1.GetBinError( b ) )
    # Some times the weighted histograms fail to give good
    # uncertainties for TGraphAsymmErrors.  When that happens
    # grab the uncertainty from the "unweighted" version
    g = ROOT.TGraphAsymmErrors( h1, h2 )
    #g = ROOT.TGraphAsymmErrors( h1, h2, 'v' ) # Verbose
    h1.Sumw2(False) # treat h1 as unweighted
    h2.Sumw2(False)
    g2 = ROOT.TGraphAsymmErrors( h1, h2 ) # created unweighted version
    checkReturnedUncert( g, g2 ) # take only uncertainty for failed points
    return g


def makeFinalEfficiencyPlot( fOut, c, trigger, divisions, effPlots, matchList, legendApp='', doFit=True ) :
    mini = 5.
    maxi = 400.
    #maxi = 100.
    fitMin = 20.
    doFit=False
    #doLog=True

    if doLog and trigger not in nvtxTriggers :
        mini = 5.
        maxi = 400.
        #maxi = 100.
        ROOT.gPad.SetLogx()
    else :
        mini = 0.
        maxi = 60.
        #maxi = 100.
        ROOT.gPad.SetLogx(0)

    
    # turn off doFit if plot by nvtx
    if trigger in nvtxTriggers :
        doFit = False
        maxi = 60
    
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange]
    legItems = []
    legNames = []
    cnt = 0
    mg = ROOT.TMultiGraph()
    mg.SetTitle( trigger )
    xMax = 0.
    fits = []


    # Before plotting, get the ratio for storage of SF
    # If doEta, then 2D
    if doEta :
        ratioPlot = get2DHist( trigger, 'Ratio' )
        ratioPlot.SetTitle( trigger+'_SF' )
        ratioPlot.SetName( trigger+'_SF' )
    else :
        ratioPlot = ROOT.TH1D(trigger+'_SF',trigger+'_SF',len(binning)-1,binning)
    binning = getBinning( trigger, trigger )
    ratioPlotN = ROOT.TH1D('ratioN','ratioN',len(binning)-1,binning)
    ratioPlotD = ROOT.TH1D('ratioD','ratioD',len(binning)-1,binning)
    for i, division in enumerate(divisions) :
        if division not in matchList : continue
        if effPlots[division].Integral() == 0.0 : continue

        # For SF calculation
        if 'All 2016 Data' in division :
            fOut.cd()
            if doEta :
                ratioPlotN = effPlots[division].Clone()
                ratioPlotN.SetTitle( trigger+'_data' )
                ratioPlotN.SetName( trigger+'_data' )
                ratioPlotN.Write()
            else :
                tgraphToTH1( effPlots[division], ratioPlotN )
                effPlots[division].Write(trigger+'_data')
        if 'DYJets' in division :
            fOut.cd()
            if doEta :
                ratioPlotD = effPlots[division].Clone()
                ratioPlotD.SetTitle( trigger+'_MC' )
                ratioPlotD.SetName( trigger+'_MC' )
                ratioPlotD.Write()
            else :
                tgraphToTH1( effPlots[division], ratioPlotD )
                effPlots[division].Write(trigger+'_MC')
    ratioPlot.Add( ratioPlotN )
    ratioPlot.Divide( ratioPlotD )

    # Finish ratio plot
    fOut.cd()
    ratioPlot.Write()
    if doEta : return

    for i, division in enumerate(divisions) :
        if division not in matchList : continue
        print i, division, effPlots[division]
        if effPlots[division].Integral() == 0.0 : continue
        #print i, cnt, division, effPlots[division].Integral(), "color:",colors[cnt]
        #effPlots[division].SetLineColor( colors[cnt] )
        #effPlots[division].SetLineColor( ROOT.kBlack )
        effPlots[division].SetLineColor( colors[cnt] )
        effPlots[division].SetLineWidth( 1 )
        effPlots[division].SetMarkerSize( 1 )
        effPlots[division].SetMarkerStyle( 20+cnt )
        effPlots[division].SetMarkerColor( colors[cnt] )
        #effPlots[division].SetMarkerColor( cnt+1 )
        if not doEta :
            if doLog and trigger not in nvtxTriggers :
                effPlots[division].GetXaxis().SetLimits( mini, maxi )
            else :
                effPlots[division].GetXaxis().SetLimits( 0., maxi )
        if doFit :
            #f1 = ROOT.TF1( 'f1', 'ROOT::Math::crystalball_cdf(x, [0], [1], [2], [3])*[4]', fitMin, maxi )
            f1 = ROOT.TF1( 'f1', '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*[4]', fitMin, maxi )
            #f1 = ROOT.TF1( 'f1', '1 - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*[4]', fitMin, maxi )
            f1.SetParName( 0, "alpha" )
            f1.SetParName( 1, "n" )
            f1.SetParName( 2, "simga" )
            f1.SetParName( 3, "x0" )
            f1.SetParName( 4, "scale" )
            f1.SetParName( 5, "y-rise" )
            #f1.SetParameter( 0, 1. ) # Good fit for Tau50 RunC & RunD
            #f1.SetParameter( 1, 5. )
            #f1.SetParameter( 2, 7. )
            #f1.SetParameter( 3, -50. )
            #f1.SetParameter( 4, 1. )
            #f1.SetParameter( 5, 1. )
            f1.SetParameter( 0, 1. )
            f1.SetParameter( 1, 5. )
            f1.SetParameter( 2, 7. )
            f1.SetParameter( 3, -50. )
            f1.SetParameter( 4, 1. )
            f1.SetParameter( 5, 1. )
            effPlots[division].Fit('f1', 'SR' )
            f2 = ROOT.TF1( 'f'+division, '[5] - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*[4]', fitMin, maxi )
            #f2 = ROOT.TF1( 'f'+division, '1 - ROOT::Math::crystalball_cdf(-x, [0], [1], [2], [3])*[4]', fitMin, maxi )
            f2.SetParameter( 0, f1.GetParameter(0) )
            f2.SetParameter( 1, f1.GetParameter(1) )
            f2.SetParameter( 2, f1.GetParameter(2) )
            f2.SetParameter( 3, f1.GetParameter(3) )
            f2.SetParameter( 4, f1.GetParameter(4) )
            f2.SetParameter( 5, f1.GetParameter(5) )
            #f2.SetLineColor( cnt+1 )
            f2.SetLineColor( colors[cnt] )
            fits.append( f2 )
        mg.Add( effPlots[division].Clone() )
        legItems.append( effPlots[division] )
        legNames.append( legendApp+division )
        cnt += 1

    ROOT.gPad.cd()
    mg.Draw('ap')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )
    if trigger in nvtxTriggers :
        mg.GetXaxis().SetTitle('Num. Reconstructed Vertixes')
    else :
        mg.GetXaxis().SetTitle('Offline Lepton p_{T} (GeV)')
    mg.GetXaxis().SetTitleOffset( mg.GetXaxis().GetTitleOffset()*1.3 )
    mg.GetYaxis().SetTitle('L1 + HLT Efficiency')
    if not doEta :
        if doLog and trigger not in nvtxTriggers :
            mg.GetXaxis().SetLimits( mini, maxi )
        else :
            mg.GetXaxis().SetLimits( 0., maxi )
    mg.GetXaxis().SetMoreLogLabels()

    if doFit :
        for fit in fits :
            fit.Draw('SAME R')

    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    decorate(35.9)
    c.SaveAs(plotBase+c.GetName()+'.png')
    c.SaveAs(plotBase+c.GetName()+'.pdf')
    del leg
    c.Clear()

fOut = ROOT.TFile('triggerSFs2.root','RECREATE')

for channel in ['ee','mm',] :
#for channel in ['mm',] :
#for channel in ['ee',] :

    plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/zhTrigEff_nov10v4_eta/'

    if channel == 'ee' :
        triggers = ee_triggers.keys()
        dataFile = 'zhTrigEff_SingleElectron_nov08.root'
    if channel == 'mm' :
        triggers = mm_triggers.keys()
        dataFile = 'zhTrigEff_SingleMuon_nov08.root'

    nDYJets = 'zhTrigEff_DYJets_nov08.root'
    

    directory = 'zhTrigEff_nov09'

    fData = ROOT.TFile('/data/truggles/'+directory+'/'+dataFile, 'r')
    tData = fData.Get('DoubleLeptonTAPStudies/tagAndProbe/Ntuple')
    fDYJets = ROOT.TFile('/data/truggles/'+directory+'/'+nDYJets, 'r')
    tDYJets = fDYJets.Get('DoubleLeptonTAPStudies/tagAndProbe/Ntuple')
    trees = {
        'DYJets' : tDYJets,
        'data' : tData,
    }
    for k, v in trees.iteritems() :
        print k, v
    
    c = ROOT.TCanvas( 'c1', 'c1', 800, 700 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    
    

    Divisions = OrderedDict()

#    Divisions['All 2016 Data - nvtx'] = 'run > 0'
#    Divisions['DYJets - nvtx'] = 'run > 0'
#    Divisions['RunB - nvtx'] = 'run >= 297020 && run <= 299329'
#    Divisions['RunC - nvtx'] = 'run >= 299337 && run <= 302029'
#    Divisions['RunD - nvtx'] = 'run >= 302030 && run <= 303434'
    Divisions['All 2016 Data'] = 'run > 0'
    Divisions['DYJets'] = 'run > 0'
#    Divisions['RunB'] = 'run >= 297020 && run <= 299329'
#    Divisions['RunC'] = 'run >= 299337 && run <= 302029'
#    Divisions['RunD'] = 'run >= 302030 && run <= 303434'
    #Divisions['Medium'] = 'tMVAIsoMedium == 1 && tMVAIsoTight != 1'
    #Divisions['Tight'] = 'tMVAIsoTight == 1 && tMVAIsoVTight != 1'
    #Divisions['VTight'] = 'tMVAIsoVTight == 1'
    #Divisions['nvtx0to15'] = 'nvtx >= 0 && nvtx < 15'
    #Divisions['nvtx15to25'] = 'nvtx >= 15 && nvtx < 25'
    #Divisions['nvtx25to35'] = 'nvtx >= 25 && nvtx < 35'
    #Divisions['nvtx35plus'] = 'nvtx >= 35'
    #Divisions['2016 RunD 0 <= nvtx <= 25'] = 'nvtx >= 0 && nvtx < 25 && run >= 302030 && run <= 303434'
    #Divisions['2016 RunD nvtx > 25'] = 'nvtx >= 25 && run >= 302030 && run <= 303434'

    isolations = ['Medium','Tight','VTight']
    runs = ['RunB','RunC','RunD','DYJets']
    nvtxs = ['nvtx0to15','nvtx15to25','nvtx25to35','nvtx35plus',]
    nvtxsRunD = ['2016 RunD 0 <= nvtx <= 25','2016 RunD nvtx > 25',]
    all2016 = ['All 2016 Data','DYJets']
    all2016nvtx = ['All 2016 Data - nvtx','DYJets - nvtx']
    nvtxByRun = ['RunB - nvtx', 'RunC - nvtx', 'RunD - nvtx','DYJets - nvtx']

    if 'Medium' not in Divisions.keys() : isolations = []
    if 'RunB' not in Divisions.keys() : runs = []
    if 'nvtx0to15' not in Divisions.keys() : nvtxs = []
    if '2016 RunD 0 <= nvtx <= 25' not in Divisions.keys() : nvtxsRunD = []
    if 'All 2016 Data' not in Divisions.keys() : all2016 = []
    if 'All 2016 Data - nvtx' not in Divisions.keys() : all2016nvtx = []
    if 'RunB - nvtx' not in Divisions.keys() : nvtxByRun = []


    saveMap = {}
    #isolations = ['Tight',]
    for trigger in triggers :
        print "\n\nHLT Trigger: ",trigger
        effPlots = {}
        #for iso in isolations :
        for division in Divisions :
            binning = getBinning( trigger, trigger )
            print division
            effPlots[division] = {}

#   "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
#   "HLT_Ele23_CaloIdL_TrackIdL_IsoVL",
#   "HLT_Ele12_CaloIdL_TrackIdL_IsoVL",
#   "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",

            if channel == 'ee' :
                lepCount = 'passingElectrons == 2'
                #numTrigger = 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ > 0.5'
                numTrigger = ee_triggers[trigger][1]
                denomTrigger = ee_triggers[trigger][0]
            if channel == 'mm' :
                lepCount = 'passingMuons == 2'
                # FIXME decide on double Mu triggers
                #numTrigger = '(HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ > 0.5 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ > 0.5)'
                #numTrigger = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ > 0.5'
                numTrigger = mm_triggers[trigger][1]
                denomTrigger = mm_triggers[trigger][0]

            #baselineCut = lepCount+' && l2Match_'+trigger+' == 1 && (eventD%2==0)'
            print "num:",numTrigger
            print "denom:",denomTrigger
            baselineCut = lepCount+' && m_vis>75 && m_vis<105 &&  nBTags == 0 && '+denomTrigger
            print "baseline:",baselineCut

            baselineCut += ' && '+Divisions[division]

            cuts = {
                'SSPassL1': '(-1)*('+baselineCut+' && SS == 1 && %s' % numTrigger+')',
                'OSPassL1': baselineCut+' && SS == 0 && %s' % numTrigger,
                'SSAllL1': '(-1)*('+baselineCut+' && SS == 1)',
                'OSAllL1': baselineCut+' && SS == 0'
            }
            #cuts['SSPassL2'] = copy.deepcopy(cuts['SSPassL1']).replace('l2Match','l1Match').replace('D%2==0','D%2==1')
            #cuts['OSPassL2'] = copy.deepcopy(cuts['OSPassL1']).replace('l2Match','l1Match').replace('D%2==0','D%2==1')
            #cuts['SSAllL2'] = copy.deepcopy(cuts['SSAllL1']).replace('l2Match','l1Match').replace('D%2==0','D%2==1')
            #cuts['OSAllL2'] = copy.deepcopy(cuts['OSAllL1']).replace('l2Match','l1Match').replace('D%2==0','D%2==1')


            hists = {}
            for name, cut in cuts.iteritems() :
                xCut = '('+cut+')*puweight' # puweight set to 1 for all data events
                #print name, xCut

                lep = mm_triggers[trigger][2].replace('Match_','') if channel == 'mm' else ee_triggers[trigger][2].replace('Match_','')

                if trigger in nvtxTriggers :
                    hists[ name ] = getHist( trees, 'nvtx', xCut, name, division, trigger )
                elif doEta : # via Eta
                    # Modify xCut to include a base pT threshold on these eta plots
                    if channel == 'mm' :
                        # use Eta cut with threshold for 1D eta distributions, else forget it
                        #etaCut = xCut+'*( %sPt > %s)' % ( lep, mm_triggers[trigger][3])
                        etaCut = xCut
                        #print name, etaCut
                        #print "Drawing "+lep+'Pt:'+lep+'Eta'
                        #hists[ name ] = getHist( trees, lep+'Eta', etaCut, name, division, trigger, doEta ) # 1D
                        if trigger == 'HLT_Mu8_and_DZ' :
                            hists[ name ] = getHist( trees, 'nvtx:'+lep+'Pt', etaCut, name, division, trigger, doEta )
                        else :
                            hists[ name ] = getHist( trees, lep+'Eta:'+lep+'Pt', etaCut, name, division, trigger, doEta )
                    if channel == 'ee' :
                        #etaCut = xCut+'*( %sPt > %s)' % ( lep, ee_triggers[trigger][3])
                        etaCut = xCut
                        #print name, etaCut
                        #print "Drawing "+lep+'Pt:'+lep+'Eta'
                        #hists[ name ] = getHist( trees, lep+'Eta', etaCut, name, division, trigger, doEta ) # 1D
                        if trigger == 'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_and_DZ' :
                            hists[ name ] = getHist( trees, 'nvtx:'+lep+'Pt', etaCut, name, division, trigger, doEta )
                        else :
                            hists[ name ] = getHist( trees, lep+'Eta:'+lep+'Pt', etaCut, name, division, trigger, doEta )
                else : # via Pt
                    if channel == 'mm' :
                        #print "Drawing "+mm_triggers[trigger][2]+"Pt"
                        hists[ name ] = getHist( trees, lep+'Pt', xCut, name, division, trigger )
                    if channel == 'ee' :
                        #print "Drawing "+ee_triggers[trigger][2]+"Pt"
                        hists[ name ] = getHist( trees, lep+'Pt', xCut, name, division, trigger )
                
            ### Do OS - SS
            #groups = ['PassL1','AllL1','PassL2','AllL2']
            groups = ['PassL1','AllL1']
            subMap1 = {}
            for group in groups :
                subMap1[ group ] = subtractTH1( hists['OS'+group], hists['SS'+group] )
                #subMap1[ group ] = hists['OS'+group].Clone()
            ### Do adding of both legs
            groups = ['Pass','All']
            subMap = {}
            for group in groups :
                #subMap[ group ] = addTH1( subMap1[group+'L1'], subMap1[group+'L2'] )
                subMap[ group ] = hists['OS'+group+'L1'].Clone()


            ### Make Eff Plot
            ### HACK for 2D skip TGraphAsymErrors and just use TH2D
            is2D = False
            is2D = True
            if is2D :
                g = get2DHist( trigger, 'Division' )
                g.Add( subMap['Pass'] )
                g.Divide( subMap['All'] )
            else : # 1D
                g = divideTH1( subMap['Pass'], subMap['All'], binning )    
                g.SetLineWidth(2)
            c.SetGrid()
            g.GetXaxis().SetTitle('Lepton p_{T} (GeV)')
            g.GetYaxis().SetTitle('L1 + HLT Efficiency')
            g.SetTitle(trigger)
            g.Draw()
            c.Clear()
            effPlots[division] = g

        # Do MVA ID/Iso comparison
        if isolations != [] :
            print "Tau MVA ID/Iso Comparison"
            c.SetName(trigger+'_allIsos')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, isolations, 'Tau MVA Iso ' )
        # Do Run comparison
        if runs != [] :
            print "Run Comparison"
            c.SetName(trigger+'_allRuns')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, runs, '2016 ' )

        # Do NVTX comparison
        if nvtxs != [] :
            print "NVTX Comparison"
            c.SetName(trigger+'_nvtx')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, nvtxs, '' )

        # Do NVTX comparison for Run D
        if nvtxsRunD != [] :
            print "NVTX Comparison for Run D"
            c.SetName(trigger+'_nvtxRunD')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, nvtxsRunD, '' )

        # Do all data
        if all2016 != [] :
            print "All 2016 Data"
            c.SetName(trigger+'_combined')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, all2016, '' )

        # Do NVTX comparison for all 2016
        if all2016nvtx != [] :
            print "All 2016 Data NVTX"
            c.SetName(trigger+'_nvtxAll')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, all2016nvtx, '' )
            #if doNvtxComb :
            #    effPlots[0].SetTitle(trigger+all2016nvtx[0]+' - nvtx')
            #    saveMap[trigger+all2016nvtx[0]] = effPlots[0]

        # Do NVTX comparison by run
        if all2016nvtx != [] :
            print "All 2016 Data By Run NVTX"
            c.SetName(trigger+'_nvtxByRun')
            makeFinalEfficiencyPlot( fOut, c, trigger, Divisions, effPlots, nvtxByRun, '' )

    ## Do NVTX comparison for all 2016 and all triggers
    #if doNvtxComb and all2016nvtx != [] :
    #    Divisions = OrderedDict()
    #    Divisions['PFTau20, All 2016 Data - nvtx'] = ''
    #    Divisions['PFTau35, All 2016 Data - nvtx'] = ''
    #    Divisions['PFTau50, All 2016 Data - nvtx'] = ''

    #    print "All 2016 Data NVTX"
    #    c.SetName('all_triggers_all_data_nvtxAll')
    #    makeFinalEfficiencyPlot( c, trigger, Divisions, saveMap, Divisions.keys(), '' )


fOut.Close()





