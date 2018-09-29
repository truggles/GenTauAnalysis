

import ROOT
from array import array
import os


def add_lumi(lumi_):
    lowX=0.52
    lowY=0.82
    lumi  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.30, lowY+0.16, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    lumi.AddText("2018, %s fb^{-1} (13 TeV)" % lumi_)
    return lumi

def add_CMS():
    lowX=0.125
    lowY=0.82
    cms  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    cms.SetTextFont(61)
    cms.SetTextSize(0.06)
    cms.SetBorderSize(   0 )
    cms.SetFillStyle(    0 )
    cms.SetTextAlign(   12 )
    cms.SetTextColor(    1 )
    cms.AddText("CMS")
    return cms

def add_Preliminary():
    lowX=0.24
    lowY=0.815
    prelim  = ROOT.TPaveText(lowX, lowY+0.06, lowX+0.15, lowY+0.16, "NDC")
    prelim.SetTextFont(52)
    prelim.SetTextSize(0.05)
    prelim.SetBorderSize(   0 )
    prelim.SetFillStyle(    0 )
    prelim.SetTextAlign(   12 )
    prelim.SetTextColor(    1 )
    prelim.AddText("Preliminary")
    return prelim


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
    leg = buildLegend( [h1, h2], ['HPS', 'Default'] )
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

def saveHists( c, th2, name ) :
    ROOT.gStyle.SetOptStat(0)

    ROOT.gStyle.SetPaintTextFormat("4.0f")
    ROOT.gPad.SetLogz()
    th2.Draw("COLZ TEXT")
    c.SaveAs( name+'.png' )
    
    ROOT.gStyle.SetPaintTextFormat("4.2f")
    ROOT.gPad.SetLogz(0)
    
    normalize2D( th2 )
    c.SaveAs( name+'_norm.png' )
