#!/usr/bin/env python

mt_triggers = [
#   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
#   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
#   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
]

doLog = True
doLog = False
doNvtxComb = True

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
from collections import OrderedDict
from math import sqrt
import os



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
    lumi.DrawTextNDC(.60,.91,"2017, %.1f / fb (13 TeV)" % cmsLumi )

def getBinning( name, division ) :
    #if 'IsoPFTau20' in trigger or 'IsoPFTau35' in trigger :
    #    binning = array('d', [])
    #    for i in range( 20, 45, 2 ) :
    #        binning.append( i )
    #    for i in range( 45, 60, 5 ) :
    #        binning.append( i )
    #    for i in range( 60, 110, 20 ) :
    #        binning.append( i )
    #    #binning.append( 150 )
    #    binning.append( 250 )
    #    #binning.append( 400 )
    #    #binning.append( 1000 )
    #elif 'IsoPFTau50' in trigger :
    #    binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
    #        42.5,45,47.5,50,55,60,67.5,80,100,250])#,400,1000])
    
    if ' - nvtx' in division :
        binning = array('d', [])
        for i in range( 0, 110, 10 ) :
            binning.append( i )
    else :
        binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
            42.5,45,47.5,50,55,60,65,70,80,100,150,250])#,400,1000])
    return binning


def getHist( trees, var, cut, name, division, trigger ) :
    binning = getBinning( trigger, division )
    #h = ROOT.TH1F( name, name, 20, 0, 100)
    h = ROOT.TH1F( name, name+trigger, len(binning)-1, binning)
    #h.Sumw2()
    doCut = ''
    doCut += cut

    # Adding MC Samples
    if 'ggH125' in division :
        trees['ggH125'].Draw( var+' >> '+name, doCut )
    elif 'qqH125' in division :
        trees['qqH125'].Draw( var+' >> '+name, doCut )
    elif 'DYJets' in division :
        trees['DYJets'].Draw( var+' >> '+name, doCut )
    else :
        trees['singleMu'].Draw( var+' >> '+name, doCut )

    print name, h.Integral() #, binning
    h.GetXaxis().SetTitle('Offline #tau p_{T} (GeV)')
    h.GetYaxis().SetTitle('Number of Events')
    h.SetDirectory( 0 )
    return h

def subtractTH1( h1, h2 ) :
    h3 = h1
    h3.Add( -1 * h2 )
    h3.SetTitle( h1.GetTitle()+'_Minus_'+h2.GetTitle() )
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
    maxi = 250.
    #maxi = 100.
    fitMin = 20.
    doFit=False
    
    # turn off doFit if plot by nvtx
    if ' - nvtx' in matchList[0] :
        doFit = False
        maxi = 60
    
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+1, ROOT.kOrange, ROOT.kYellow]
    legItems = []
    legNames = []
    cnt = 0
    mg = ROOT.TMultiGraph()
    mg.SetTitle( trigger )
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
    mg.SetMaximum( 1.3 )
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
    decorate(21.15)
    c.SaveAs(plotBase+c.GetName()+'.png')
    c.SaveAs(plotBase+c.GetName()+'.pdf')
    del leg
    c.Clear()

for channel in ['mt',] :

    plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/nov21/'
    if not os.path.exists( plotBase ) : os.makedirs( plotBase )

    triggers = mt_triggers
    inDir = '/data/truggles/nov12_tauTAP_sync/'
    fData = ROOT.TFile(inDir+'SingleMuonTauTAP_nov09forSyncV_B-E.root', 'r')
    tData = fData.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')
    #fggH125 = ROOT.TFile('/data/truggles/hltTaus_oct03v2/GluGluHToTauTau_M125.root', 'r')
    #tggH125 = fggH125.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')
    #fqqH125 = ROOT.TFile('/data/truggles/hltTaus_oct03v2/VBFHToTauTau_M125.root', 'r')
    #tqqH125 = fqqH125.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')
    inDir = '/data/truggles/oct24_tauTAP_sync/'
    fDYJets = ROOT.TFile(inDir+'DYJets_all_sync_ext1_v4.root', 'r')
    tDYJets = fDYJets.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')
    trees = {
        #'ggH125' : tggH125,
        #'qqH125' : tqqH125,
        'DYJets' : tDYJets,
        'singleMu' : tData,
    }
    for k, v in trees.iteritems() :
        print k, v
    
    c = ROOT.TCanvas( 'c1', 'c1', 800, 700 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.4 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.2 )
    p.Draw()
    p.cd()
    
    

    Divisions = OrderedDict()

    # Run F starts at 304911
#    Divisions['All 2017 Data - nvtx'] = 'RunNumber > 0 && RunNumber < 304911'
#    #Divisions['ggH125 - nvtx'] = 'RunNumber > 0 && RunNumber < 304911'
#    #Divisions['qqH125 - nvtx'] = 'RunNumber > 0 && RunNumber < 304911'
#    Divisions['DYJets - nvtx'] = 'RunNumber > 0 && RunNumber < 304911'
#    Divisions['RunB - nvtx'] = 'RunNumber >= 297020 && RunNumber <= 299329'
#    Divisions['RunC - nvtx'] = 'RunNumber >= 299337 && RunNumber <= 302029'
#    Divisions['RunD - nvtx'] = 'RunNumber >= 302030 && RunNumber <= 303434'
#    Divisions['RunE - nvtx'] = 'RunNumber >= 303435 && RunNumber <= 304826'
    Divisions['All 2017 Data'] = 'RunNumber > 0 && RunNumber < 304911'
    #Divisions['ggH125'] = 'RunNumber > 0 && RunNumber < 304911'
    #Divisions['qqH125'] = 'RunNumber > 0 && RunNumber < 304911'
    Divisions['DYJets'] = 'RunNumber > 0 && RunNumber < 304911'
#    Divisions['RunB'] = 'RunNumber >= 297020 && RunNumber <= 299329'
#    Divisions['RunC'] = 'RunNumber >= 299337 && RunNumber <= 302029'
#    Divisions['RunD'] = 'RunNumber >= 302030 && RunNumber <= 303434'
#    Divisions['RunE'] = 'RunNumber >= 303435 && RunNumber <= 304826'
    #Divisions['Medium'] = 'tMVAIsoMedium == 1 && tMVAIsoTight != 1'
    #Divisions['Tight'] = 'tMVAIsoTight == 1 && tMVAIsoVTight != 1'
    #Divisions['VTight'] = 'tMVAIsoVTight == 1'
    #Divisions['nvtx0to15'] = 'nvtx >= 0 && nvtx < 15'
    #Divisions['nvtx15to25'] = 'nvtx >= 15 && nvtx < 25'
    #Divisions['nvtx25to35'] = 'nvtx >= 25 && nvtx < 35'
    #Divisions['nvtx35plus'] = 'nvtx >= 35'
    #Divisions['2017 RunD 0 <= nvtx <= 25'] = 'nvtx >= 0 && nvtx < 25 && RunNumber >= 302030 && RunNumber <= 303434'
    #Divisions['2017 RunD nvtx > 25'] = 'nvtx >= 25 && RunNumber >= 302030 && RunNumber <= 303434'

    isolations = ['Medium','Tight','VTight']
    RunNumbers = ['DYJets','RunB','RunC','RunD','RunE']
    nvtxs = ['nvtx0to15','nvtx15to25','nvtx25to35','nvtx35plus',]
    nvtxsRunD = ['2017 RunD 0 <= nvtx <= 25','2017 RunD nvtx > 25',]
    #all2017 = ['All 2017 Data','ggH125','qqH125','DYJets']
    all2017 = ['DYJets','All 2017 Data']
    #all2017nvtx = ['All 2017 Data - nvtx','ggH125 - nvtx','qqH125 - nvtx','DYJets - nvtx']
    all2017nvtx = ['DYJets - nvtx','All 2017 Data - nvtx']
    nvtxByRun = ['DYJets - nvtx', 'RunB - nvtx', 'RunC - nvtx', 'RunD - nvtx', 'RunE - nvtx']

    if 'Medium' not in Divisions.keys() : isolations = []
    if 'RunB' not in Divisions.keys() : RunNumbers = []
    if 'nvtx0to15' not in Divisions.keys() : nvtxs = []
    if '2017 RunD 0 <= nvtx <= 25' not in Divisions.keys() : nvtxsRunD = []
    if 'All 2017 Data' not in Divisions.keys() : all2017 = []
    if 'All 2017 Data - nvtx' not in Divisions.keys() : all2017nvtx = []
    if 'RunB - nvtx' not in Divisions.keys() : nvtxByRun = []


    saveMap = {}
    #isolations = ['Tight',]
    for trigger in triggers :
        print "\n\nHLT Trigger: ",trigger
        effPlots = {}
        #for iso in isolations :
        for division in Divisions :
            binning = getBinning( trigger, division )
            print division
            effPlots[division] = {}

            baselineCut = 'muonPt > 24 && tMVAIsoMedium == 1 && HLT_IsoMu27 == 1 && m_vis > 40 && m_vis < 80 && transMass < 30 && passingMuons == 1 && nVetoMuons == 1 && passingElectrons == 0 && nBTag == 0'

            # If 1pt, it wasn't in Run B
            if "Trk30_eta2p1_1pr" in trigger and 'All 2017 Data' in division :
                # lower is bottom of RunC, top is top of RunD
                baselineCut += ' && RunNumber >= 299337'
            else :
                baselineCut += ' && '+Divisions[division]

            # For 1pr HLT Paths
            if "Trk30_eta2p1_1pr" in trigger :
                 #baselineCut += ' && tauDM < 2'
                 baselineCut += ' && tauDM == 1'

            cuts = {
                'SSPass': baselineCut+' && SS == 1 \
                    && tTrigMatch>0.5 && %s > 0.5' % trigger,
                'OSPass': baselineCut+' && SS == 0 \
                    && tTrigMatch>0.5 && %s > 0.5' % trigger,
                'SSAll': baselineCut+' && SS == 1',
                'OSAll': baselineCut+' && SS == 0'
            }


            hists = {}
            for name, cut in cuts.iteritems() :
                print name, cut
                xCut = '('+cut+')*puweight'
                if ' - nvtx' in division :
                    if 'PFTau20' in trigger : xCut += '*(tauPt > 25)'
                    if 'PFTau35' in trigger : xCut += '*(tauPt > 40)'
                    if 'PFTau50' in trigger : xCut += '*(tauPt > 55)'
                    hists[ name ] = getHist( trees, 'nvtx', xCut, name, division, trigger )
                else : # normal hists via tau pt
                    hists[ name ] = getHist( trees, 'tauPt', xCut, name, division, trigger )
                
            ### Do OS - SS
            #groups = ['Pass','Fail','All']
            groups = ['Pass','All']
            subMap = {}
            for group in groups :
                subMap[ group ] = subtractTH1( hists['OS'+group], hists['SS'+group] )


            ### Make Eff Plot
            g = divideTH1( subMap['Pass'], subMap['All'], binning )    
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


        # Do MVA ID/Iso comparison
        if isolations != [] :
            print "Tau MVA ID/Iso Comparison"
            c.SetName(trigger+'_allIsos')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, isolations, 'Tau MVA Iso ' )
        # Do Run comparison
        if RunNumbers != [] :
            print "Run Comparison"
            c.SetName(trigger+'_allRuns')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, RunNumbers, '2017 ' )

        # Do NVTX comparison
        if nvtxs != [] :
            print "NVTX Comparison"
            c.SetName(trigger+'_nvtx')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, nvtxs, '' )

        # Do NVTX comparison for Run D
        if nvtxsRunD != [] :
            print "NVTX Comparison for Run D"
            c.SetName(trigger+'_nvtxRunD')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, nvtxsRunD, '' )

        # Do all data
        if all2017 != [] :
            print "All 2017 Data"
            c.SetName(trigger+'_combined')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017, '' )

        # Do NVTX comparison for all 2017
        if all2017nvtx != [] :
            print "All 2017 Data NVTX"
            c.SetName(trigger+'_nvtxAll')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, all2017nvtx, '' )
            #if doNvtxComb :
            #    effPlots[0].SetTitle(trigger+all2017nvtx[0]+' - nvtx')
            #    saveMap[trigger+all2017nvtx[0]] = effPlots[0]

        # Do NVTX comparison by RunNumber
        if all2017nvtx != [] :
            print "All 2017 Data By Run NVTX"
            c.SetName(trigger+'_nvtxByRun')
            makeFinalEfficiencyPlot( c, trigger, Divisions, effPlots, nvtxByRun, '' )

    ## Do NVTX comparison for all 2017 and all triggers
    #if doNvtxComb and all2017nvtx != [] :
    #    Divisions = OrderedDict()
    #    Divisions['PFTau20, All 2017 Data - nvtx'] = ''
    #    Divisions['PFTau35, All 2017 Data - nvtx'] = ''
    #    Divisions['PFTau50, All 2017 Data - nvtx'] = ''

    #    print "All 2017 Data NVTX"
    #    c.SetName('all_triggers_all_data_nvtxAll')
    #    makeFinalEfficiencyPlot( c, trigger, Divisions, saveMap, Divisions.keys(), '' )







