#!/usr/bin/env python

from collections import OrderedDict

hale_triggers = OrderedDict()
hale_triggers[ 'hasHLTetauPath_13' ] = 'Electron Tau Paths'
hale_triggers[ 'hasHLTmutauPath_13' ] = 'Muon Tau Paths'
hale_triggers[ 'hasHLTditauPath_11or20or21' ] = 'di-Tau Paths'
hale_triggers[ 'hasHLTditauPath_9or10or11' ] = 'di-Tau Paths'

doLog = True
#doLog = False
doNvtxComb = True

do2D = False
#do2D = True

if do2D :
    doLog = False

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
from math import sqrt
import os



def buildLegend( items, names ) :
    #legend = ROOT.TLegend(0.45, 0.73, 0.83, 0.88)
    if '- nvtx' in names[0] :
        legend = ROOT.TLegend(0.18, 0.15, 0.50, 0.40)
    else : # not nvtx
        legend = ROOT.TLegend(0.45, 0.15, 0.83, 0.40)
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
    lumi.DrawTextNDC(.60,.91,"2017, %.1f / fb (13 TeV)" % cmsLumi )

def getBinning( name, division ) :
    #binning = array('d', [20,25,30,32.5,35,37.5,40,42.5,\
    #    45,50,60,80,100,150,200,500])#,400,1000])
    binning = array('d', [20,25,30,35,40,\
        45,50,60,80,100,150,200,500])#,400,1000])
    return binning


def get2DHist( trees, var, cut, name, division, trigger ) :
    xBinning = array('d', [ -2.5, -2.1, -1.5, 0, 1.5, 2.1, 2.5] )
    #xBinning = array('d', [ -2.1, -1.5, 0, 1.5, 2.1] )
    yBinning = array('d', [] )
    for y in range( -32, 33, 4 ) :
        yBinning.append( y*.1 )
    print "ybinning:"
    #h = ROOT.TH2F( name, name+trigger, 6, -2.1, 2.1, 18, -3.2, 3.2 )
    h = ROOT.TH2F( name, name+trigger, len(xBinning)-1, xBinning, len(yBinning)-1, yBinning )
    doCut = ''
    doCut += cut

    # Adding MC Samples
    if 'DYJets' in division :
        trees['DYJets'].Draw( var+' >> '+name, doCut )
    else :
        trees['singleMu'].Draw( var+' >> '+name, doCut )

    print name, h.Integral() #, binning
    h.GetXaxis().SetTitle('Offline Tau #eta')
    h.GetYaxis().SetTitle('Offline Tau #phi')
    h.GetZaxis().SetTitle('L1 + HLT Efficiency')
    h.SetDirectory( 0 )
    return h

def getHist( trees, var, cut, name, division, trigger ) :
    binning = getBinning( trigger, division )
    #h = ROOT.TH1F( name, name, 20, 0, 100)
    h = ROOT.TH1F( name, name+trigger, len(binning)-1, binning)
    #h.Sumw2()
    doCut = ''
    doCut += cut

    # Adding MC Samples
    if 'DYJets' in division :
        trees['DYJets'].Draw( var+' >> '+name, doCut )
    else :
        trees['singleMu'].Draw( var+' >> '+name, doCut )

    print name, h.Integral() #, binning
    h.GetXaxis().SetTitle('Offline #tau p_{T} (GeV)')
    h.GetYaxis().SetTitle('Number of Events')
    h.SetDirectory( 0 )
    return h

def checkReturnedUncert( g, g2 ) :
    print g
    x = ROOT.Double(0)
    y = ROOT.Double(0)
    x2 = ROOT.Double(0)
    y2 = ROOT.Double(0)
    for i in range( g.GetN() ) :
        g.GetPoint( i, x, y )
        g2.GetPoint( i, x2, y2 )
        
        # If the error calculation failed in TGraphAsymmErrors
        # take it from the "unweighted" version
        if (g.GetErrorYhigh(i) == 0.0 and g.GetErrorYlow(i) == 0.0) :
            g.GetPoint( i, x, y )
            if y == 1.0 :
                g.SetPointEYlow( i, g2.GetErrorYlow(i) )
            elif y == 0.0 :
                g.SetPointEYhigh( i, g2.GetErrorYhigh(i) )
            else :
                print "\n\n\nHaven't been here before checkReturnedUncert point not 100% or 0% \n\n\n"

        erUp1 = g.GetErrorYhigh(i)
        erDown1 = g.GetErrorYlow(i)
        erUp2 = g2.GetErrorYhigh(i)
        erDown2 = g2.GetErrorYlow(i)

        if erUp1 + erUp2 > 0. :
            if ( abs(erUp1 - erUp2) / ((erUp1 + erUp2)/2) ) > 1 and erUp2 != 0.0 :
                print "Adjusting Error"
                print "Bin: %i (x,y): (%2.4f, %2.4f) Error up: %2.4f Error down: %2.4f vs. (x,y) (%2.4f, %2.4f) ErUp: %2.4f ErDn: %2.4f" % (i, x, y, g.GetErrorYhigh(i), g.GetErrorYlow(i), x2, y2, g2.GetErrorYhigh(i), g2.GetErrorYlow(i) )
                print abs(erUp1 - erUp2) / ((erUp1 + erUp2)/2)
                
                up = erUp2 if y + erUp2 > 1.0 else 1.0 - y
                print "To Set error up:",up
                g.SetPointEYhigh( i, up )

        if erDown1 + erDown2 > 0. :
            if ( abs(erDown1 - erDown2) / ((erDown1 + erDown2)/2) ) > 1 and erDown2 != 0.0 :
                print "Adjusting Error"
                print "Bin: %i (x,y): (%2.4f, %2.4f) Error up: %2.4f Error down: %2.4f vs. (x,y) (%2.4f, %2.4f) ErUp: %2.4f ErDn: %2.4f" % (i, x, y, g.GetErrorYhigh(i), g.GetErrorYlow(i), x2, y2, g2.GetErrorYhigh(i), g2.GetErrorYlow(i) )
                print abs(erDown1 - erDown2) / ((erDown1 + erDown2)/2)
                down = erDown2 if y - erDown2 >= 0.0 else y
                print "To Set error down:",down
                g.SetPointEYlow( i, down )




def divideTH2( h1, h2 ) :
    hNew = h1.Clone()
    if h2.Integral() > 0.0 :
        hNew.Divide( h2 )
    hNew.SetDirectory( 0 )
    return hNew


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


def makeFinalEfficiencyPlot( c, trigger, divisions, effPlots, matchList, legendApp='', doFit=True ) :
    mini = 15.
    mini = 20.
    maxi = 250.
    maxi = 500.
    #maxi = 100.
    fitMin = 20.
    doFit=False
    
    # turn off doFit if plot by nvtx
    if ' - nvtx' in matchList[0] :
        doFit = False
        maxi = 70
    
    #colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange, ROOT.kCyan]
    #colors = [ROOT.kBlue, ROOT.kRed, ROOT.kGreen+1, ROOT.kOrange, ROOT.kCyan]
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kBlack, ROOT.kGreen+1, ROOT.kOrange+3, ROOT.kSpring-7]
    legItems = []
    legNames = []
    cnt = 0
    mg = ROOT.TMultiGraph()
    mg.SetTitle( hale_triggers[trigger] )
    xMax = 0.
    fits = []
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
        if doLog :
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
    mg.Draw('ap')
    #mg.SetMaximum( 1.3 )
    #mg.SetMaximum( 1.05 )
    mg.SetMaximum( 1.15 )
    mg.SetMinimum( 0. )
    if ' - nvtx' in matchList[0] :
        mg.GetXaxis().SetTitle('Num. Reconstructed Vertixes')
    else :
        mg.GetXaxis().SetTitle('Offline #tau p_{T} (GeV)')
    mg.GetXaxis().SetTitleOffset( mg.GetXaxis().GetTitleOffset()*1.3 )
    mg.GetYaxis().SetTitle('L1 + HLT Efficiency')
    if doLog :
        mg.GetXaxis().SetLimits( 20., maxi )
    else :
        mg.GetXaxis().SetLimits( 0., maxi )
    mg.GetXaxis().SetMoreLogLabels()

    if doFit :
        for fit in fits :
            fit.Draw('SAME R')

    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    decorate(42.0)
    c.SaveAs(plotBase+c.GetName()+'.png')
    c.SaveAs(plotBase+c.GetName()+'.pdf')
    del leg
    c.Clear()



for channel in ['mt',] :

    plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/jan28_halesFiles/'
    if not os.path.exists( plotBase ) : os.makedirs( plotBase )

    inDir = '/afs/cern.ch/user/h/hsert/public/94XSamples/'
    triggers = hale_triggers.keys()
    dyName = 'NTuple_DYJets_RunIIFall17MiniAOD-RECOSIMstep_94X_mc2017_realistic_v10-v1_14_01_2018_PU_forFit.root'
    dataName = 'NTuple_Data2017BCDEF_17Nov2017-v1_14_01_2018_forFit.root'
    tnpTree = 'TagAndProbe'
    fData = ROOT.TFile(inDir+dataName, 'r')
    tData = fData.Get(tnpTree)
    fDYJets = ROOT.TFile(inDir+dyName, 'r')
    tDYJets = fDYJets.Get(tnpTree)
    trees = {
        'DYJets' : tDYJets,
        'singleMu' : tData,
    }
    for k, v in trees.iteritems() :
        print k, v
    
    c = ROOT.TCanvas( 'c1', 'c1', 800, 700 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()


    #ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    #ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    ROOT.gPad.SetLeftMargin( .15 )
    ROOT.gPad.SetRightMargin( .15 )
    p.Draw()
    p.cd()
    
    

    Divisions = OrderedDict()

    Divisions['All 2017 Data'] = '(RunNumber > 0)'
    #Divisions['All 2017 Data phi>2.8 & eta>1.5'] = '(tauPhi > 2.8 && tauEta > 1.5)'
    #Divisions['All 2017 Data phi>0 & eta>1.5'] = '(tauPhi > 0 && tauEta > 1.5)'
    #Divisions['All 2017 Data phi>2.8 & eta>0 & eta<1.5'] = '(tauPhi > 2.8 && tauEta > 0 && tauEta < 1.5)'
    #Divisions['All 2017 Data Not Dead'] = '(tauPhi < 2.8 || tauEta < 1.5)'
    Divisions['DYJets'] = '(RunNumber > 0)'
    #Divisions['DYJets phi>2.8 & eta>1.5'] = '(tauPhi > 2.8 && tauEta > 1.5)'
    #Divisions['DYJets phi>0 & eta>1.5'] = '(tauPhi > 0 && tauEta > 1.5)'
    #Divisions['DYJets phi>2.8 & eta>0 & eta<1.5'] = '(tauPhi > 2.8 && tauEta > 0 && tauEta < 1.5)'
    #Divisions['DYJets Not Dead'] = '(tauPhi < 2.8 || tauEta < 1.5)'
    #Divisions['DYJets'] = '(RunNumber > 0)'

    all2017 = ['All 2017 Data','DYJets']
    all2017LepDead = ['All 2017 Data','All 2017 Data phi>2.8 & eta>1.5',
        'DYJets','DYJets phi>2.8 & eta>1.5']
    all2017DiTauDead = ['All 2017 Data','All 2017 Data phi>0 & eta>1.5',
        'DYJets','DYJets phi>0 & eta>1.5']
    all2017DiTauDeadBarrel = ['All 2017 Data','All 2017 Data phi>2.8 & eta>0 & eta<1.5',
        'DYJets','DYJets phi>2.8 & eta>0 & eta<1.5']

    if 'All 2017 Data' not in Divisions.keys() : all2017 = []
    if 'All 2017 Data phi>2.8 & eta>1.5' not in Divisions.keys() : all2017LepDead = []
    if 'All 2017 Data phi>0 & eta>1.5' not in Divisions.keys() : all2017DiTauDead = []
    if 'All 2017 Data phi>2.8 & eta>0 & eta<1.5' not in Divisions.keys() : all2017DiTauDeadBarrel = []


    saveMap = {}
    for trigger in triggers :
        print "\n\nHLT Trigger: ",trigger
        effPlots = {}
        effPlots2D = {}
        for division in Divisions :
            binning = getBinning( trigger, division )
            print division
            effPlots[division] = {}
            effPlots2D[division] = {}

            baselineCut = Divisions[ division ] 
            #baselineCut = 'bkgSubANDpuW'


            cuts = {
                #'Pass': baselineCut+' * ( hasHLTetauPath_13 > 0.5 )',
                'Pass': baselineCut+' * ( %s > 0.5 )' % trigger,
                'All': baselineCut,
            }
            if 'ditau' in trigger :
                cuts[ 'Pass' ] = baselineCut+' * ( %s > 0.5 && l1tPt >= 32 )' % trigger


            hists = {}
            for name, cut in cuts.iteritems() :
                xCut = 'bkgSubANDpuW * ('+cut+')'
                print name, xCut
                if do2D :
                    if 'etau' in trigger : xCut += '*(tauPt > 35)'
                    if 'mutau' in trigger : xCut += '*(tauPt > 32)'
                    if 'ditau' in trigger : xCut += '*(tauPt > 40)'
                    hists[ name ] = get2DHist( trees, 'tauPhi:tauEta', xCut, name, division, trigger )
                else : # normal hists via tau pt
                    hists[ name ] = getHist( trees, 'tauPt', xCut, name, division, trigger )
                

            ### If doing 2D, just divide them, plot and return
            if do2D :
                h = divideTH2( hists['Pass'], hists['All'] )
                h.SetTitle('%s - %s' % (hale_triggers[trigger], division))
                ROOT.gPad.SetLeftMargin( .15 )
                ROOT.gPad.SetRightMargin( .15 )
                h.Draw('COLZ TEXT')
                c.SaveAs(plotBase+trigger+'_'+division.replace(' ','_')+'_2D.png')
                c.SaveAs(plotBase+trigger+'_'+division.replace(' ','_')+'_2D.pdf')
                c.Clear()
                effPlots2D[division] = h
                continue
                

            ### Make Eff Plot
            g = divideTH1( hists['Pass'], hists['All'], binning )    
            c.SetGrid()
            g.GetXaxis().SetTitle('#tau p_{T} (GeV)')
            g.GetYaxis().SetTitle('L1 + HLT Efficiency')
            g.SetTitle(trigger)
            g.SetLineWidth(2)
            g.Draw()
            c.Clear()
            effPlots[division] = g

        if doLog :
            ROOT.gPad.SetLogx()

        # Do all data
        if all2017 != [] and not do2D :
            print "All 2017 Data"
            c.SetName(trigger+'_combined')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017, '' )

        if all2017 != [] and do2D :
            c.Clear()
            effPlots2D['All 2017 Data'].Divide( effPlots2D['DYJets'] )
            effPlots2D['All 2017 Data'].SetTitle( '%s data/MC SF' % hale_triggers[trigger] )
            ROOT.gPad.SetLeftMargin( .15 )
            ROOT.gPad.SetRightMargin( .15 )
            effPlots2D['All 2017 Data'].Draw('COLZ TEXT')
            c.SaveAs(plotBase+trigger+'_SF_2D.png')
            c.SaveAs(plotBase+trigger+'_SF_2D.pdf')
            
        # Do all data - check dead lep_tau region
        if all2017LepDead != [] and not do2D :
            print "All 2017 Data"
            c.SetName(trigger+'_combined_lepDead')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017LepDead, '' )
        # Do all data - check dead di-tau region
        if all2017DiTauDead != [] and not do2D :
            print "All 2017 Data"
            c.SetName(trigger+'_combined_tauDead')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017DiTauDead, '' )
        # Do all data - check dead di-tau region Barrel
        if all2017DiTauDeadBarrel != [] and not do2D :
            print "All 2017 Data"
            c.SetName(trigger+'_combined_tauDeadBarrel')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017DiTauDeadBarrel, '' )
            

