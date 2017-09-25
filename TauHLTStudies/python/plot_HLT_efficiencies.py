#!/usr/bin/env python

mt_triggers = [
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
#   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
#   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   #"HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
]

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array
from collections import OrderedDict



def buildLegend( items, names ) :
    legend = ROOT.TLegend(0.45, 0.73, 0.83, 0.88)
    legend.SetMargin(0.3)
    legend.SetBorderSize(0)
    for item, name in zip(items, names) : #range(0, stack.GetStack().GetLast() + 1) :
        legend.AddEntry( item, name, 'lep')
    return legend

def decorate(cmsLumi) :
    logo = ROOT.TText(.2, .85,"CMS Preliminary")
    logo.SetTextSize(0.03)
    logo.DrawTextNDC(.2, .85,"CMS Preliminary")
    
    lumi = ROOT.TText(.7,1.05,"X fb^{-1} (13 TeV)")
    lumi.SetTextSize(0.03)
    lumi.DrawTextNDC(.67,.91,"%.1f / fb (13 TeV)" % cmsLumi )


def getHist( tree, var, cut, name, iso, trigger ) :
    #if 'IsoPFTau20' in trigger :
    #    binning = array('d', [])
    #    for i in range( 20, 45, 2 ) :
    #        binning.append( i )
    #    for i in range( 45, 60, 3 ) :
    #        binning.append( i )
    #    for i in range( 60, 80, 5 ) :
    #        binning.append( i )
    #    binning.append( 80 )
    #    binning.append( 90 )
    #    binning.append( 100 )
    #    binning.append( 150 )
    #    binning.append( 250 )
    #    binning.append( 400 )
    #    binning.append( 1000 )
    if 'IsoPFTau20' in trigger or 'IsoPFTau35' in trigger :
        binning = array('d', [])
        for i in range( 20, 45, 2 ) :
            binning.append( i )
        for i in range( 45, 60, 5 ) :
            binning.append( i )
        for i in range( 60, 110, 20 ) :
            binning.append( i )
        #binning.append( 80 )
        #binning.append( 90 )
        #binning.append( 100 )
        binning.append( 150 )
        binning.append( 250 )
        binning.append( 400 )
        binning.append( 1000 )
    elif 'IsoPFTau50' in trigger :
        binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
            42.5,45,47.5,50,55,60,67.5,80,100,150,250,400,1000])
    else :
        binning = array('d', [20,22.5,25,27.5,30,32.5,35,37.5,40,\
            42.5,45,47.5,50,55,60,67.5,80,100,150,250,400,1000])
    #binning = array('d', [20,25,30,35,40,45,\
    #    50,60,70,80,100,150,200,300,1000])
    #h = ROOT.TH1F( name, name, 20, 0, 100)
    h = ROOT.TH1F( name, name+trigger, len(binning)-1, binning)
    doCut = ''
    doCut += cut

    tree.Draw( var+' >> '+name, doCut )
    print name, h.Integral()
    h.GetXaxis().SetTitle('#tau p_{T} (GeV)')
    h.GetYaxis().SetTitle('Number of Events')
    h.SetDirectory( 0 )
    return h

def subtractTH1( h1, h2 ) :
    h3 = h1
    h3.Add( -1 * h2 )
    h3.SetTitle( h1.GetTitle()+'_Minus_'+h2.GetTitle() )
    return h3



def divideTH1( h1, h2 ) :
    ### FIXME Check bins to make sure Pass <= All
    for b in range( 1, h1.GetNbinsX()+1 ) :
        b1 =  h1.GetBinContent( b )
        b2 =  h2.GetBinContent( b )
        if b1 > b2 :
            print "Bin in Numerator > Bin in Denominator",b1,b2
            print "Setting Numerator == Denominator bin"
            h2.SetBinContent( b, b1 )
            h2.SetBinError( b, h1.GetBinError( b ) )
    g = ROOT.TGraphAsymmErrors( h1, h2 )
    return g


def makeFinalEfficiencyPlot( c, divisions, effPlots, matchList, legendApp='' ) :
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen+1, ROOT.kBlue, ROOT.kMagenta]
    legItems = []
    legNames = []
    cnt = 0
    mg = ROOT.TMultiGraph()
    xMax = 0.
    for i, division in enumerate(divisions) :
        if division not in matchList : continue
        if effPlots[division].Integral() == 0.0 : continue
        print i, cnt, division, effPlots[division].Integral(), "color:",colors[cnt]
        #effPlots[division].SetLineColor( colors[cnt] )
        effPlots[division].SetLineColor( ROOT.kBlack )
        effPlots[division].SetLineWidth( 1 )
        effPlots[division].SetMarkerSize( 1 )
        effPlots[division].SetMarkerStyle( 20+cnt )
        #effPlots[division].SetMarkerColor( colors[cnt] )
        effPlots[division].SetMarkerColor( cnt+1 )
        effPlots[division].GetXaxis().SetLimits( 20., 250. )
        mg.Add( effPlots[division] )
        legItems.append( effPlots[division] )
        legNames.append( legendApp+division )
        cnt += 1
    mg.Draw('ap')
    mg.SetMaximum( 1.3 )
    mg.SetMinimum( 0. )
    mg.GetXaxis().SetLimits( 20., 250. )
    mg.GetXaxis().SetMoreLogLabels()
    leg = buildLegend( legItems, legNames )
    leg.Draw()
    ROOT.gPad.Update()
    decorate(17.8)
    c.SaveAs(plotBase+c.GetName()+'.png')
    c.SaveAs(plotBase+c.GetName()+'.pdf')
    del leg
    c.Clear()

for channel in ['mt',] :

    plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/sept25/'

    triggers = mt_triggers
    f = ROOT.TFile('/data/truggles/tau_trigger_eff_MuTauSkim_20170925v1.root', 'r')
    tree = f.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')

    print f
    print tree
    
    c = ROOT.TCanvas( 'c1', 'c1', 800, 800 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    
    

    divisions = OrderedDict()

    divisions['RunB'] = '*(run >= 297020 && run <= 299329)'
    divisions['RunC'] = '*(run >= 299337 && run <= 302029)'
    divisions['RunD'] = '*(run >= 302030 && run <= 303434)'
    #divisions['Medium'] = '*(tMVAIsoMedium == 1)'
    #divisions['Tight'] = '*(tMVAIsoTight == 1)'
    #divisions['VTight'] = '*(tMVAIsoVTight == 1)'
    #divisions['nvtx0to15'] = '*(nvtx >= 0 && nvtx < 15)'
    #divisions['nvtx15to25'] = '*(nvtx >= 15 && nvtx < 25)'
    #divisions['nvtx25to35'] = '*(nvtx >= 25 && nvtx < 35)'
    #divisions['nvtx35plus'] = '*(nvtx >= 35)'

    isolations = ['Medium','Tight','VTight']
    runs = ['RunB','RunC','RunD']
    nvtxs = ['nvtx0to15','nvtx15to25','nvtx25to35','nvtx35plus',]

    divisions['nvtx0to25_runD'] = '*(nvtx >= 0 && nvtx < 25)*(run >= 302030 && run <= 303434)'
    divisions['nvtx25plus_runD'] = '*(nvtx >= 25)*(run >= 302030 && run <= 303434)'
    nvtxsRunD = ['nvtx0to25_runD','nvtx25plus_runD',]

    if 'Medium' not in divisions.keys() : isolations = []
    if 'RunB' not in divisions.keys() : runs = []
    if 'nvtx0to15' not in divisions.keys() : nvtxs = []
    if 'nvtx0to25_runD' not in divisions.keys() : nvtxsRunD = []


    #isolations = ['Tight',]
    for trigger in triggers :
        print "\n\nHLT Trigger: ",trigger
        effPlots = {}
        #for iso in isolations :
        for division in divisions :
            print division
            effPlots[division] = {}

            onePr = '*(1)'
            baselineCut = '(mPt > 27 && tMVAIsoMedium == 1 && HLT_IsoMu27 == 1 && m_vis > 40 && m_vis < 80 && transMass < 30)'
            baselineCut += divisions[division]
            if "Trk30_eta2p1_1pr" in trigger :
                 onePr = '*(tDecayMode < 2)'
            cuts = {
                'SSPass': baselineCut+'*(SS == 1 \
                    && tTrigMatch>0.5 && %s > 0.5)%s' % (trigger, onePr),
                'OSPass': baselineCut+'*(SS == 0 \
                    && tTrigMatch>0.5 && %s > 0.5)%s' % (trigger, onePr),
                'SSAll': baselineCut+'*(SS == 1)%s' % (onePr),
                'OSAll': baselineCut+'*(SS == 0)%s' % (onePr)
                }


            hists = {}
            for name, cut in cuts.iteritems() :
                print name, cut
                hists[ name ] = getHist( tree, 'tPt', cut, name, division, trigger )
                
            ### Do OS - SS
            #groups = ['Pass','Fail','All']
            groups = ['Pass','All']
            subMap = {}
            for group in groups :
                subMap[ group ] = subtractTH1( hists['OS'+group], hists['SS'+group] )


            ### Make Eff Plot
            g = divideTH1( subMap['Pass'], subMap['All'] )    
            c.SetGrid()
            g.GetXaxis().SetTitle('#tau p_{T} (GeV)')
            g.GetYaxis().SetTitle('L1 + HLT Efficiency')
            g.SetTitle(trigger)
            g.SetLineWidth(2)
            g.Draw()
            c.Clear()
            effPlots[division] = g

        ROOT.gPad.SetLogx()

        # Do MVA ID/Iso comparison
        if isolations != [] :
            print "Tau MVA ID/Iso Comparison"
            c.SetName(trigger+'_allIsos')
            makeFinalEfficiencyPlot( c, divisions, effPlots, isolations, 'Tau MVA Iso ' )
        # Do Run comparison
        if runs != [] :
            print "Run Comparison"
            c.SetName(trigger+'_allRuns')
            makeFinalEfficiencyPlot( c, divisions, effPlots, runs, '2017 ' )

        # Do NVTX comparison
        if nvtxs != [] :
            print "NVTX Comparison"
            c.SetName(trigger+'_nvtx')
            makeFinalEfficiencyPlot( c, divisions, effPlots, nvtxs, '' )

        # Do NVTX comparison for Run D
        if nvtxsRunD != [] :
            print "NVTX Comparison for Run D"
            c.SetName(trigger+'_nvtxRunD')
            makeFinalEfficiencyPlot( c, divisions, effPlots, nvtxsRunD, '' )










