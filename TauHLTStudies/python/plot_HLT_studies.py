#!/usr/bin/env python

mt_triggers = [
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",
   "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
   "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
   "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
   "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
]

mt_trigger_groups = {
"SingleL1" : [
    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",
    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",
    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",
],
"TightID_SingleL1" : [
    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",
    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",
    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",
],
"Reg_CrossL1" : [
    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",
],
"TightID_Reg_CrossL1" : [
    "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
    "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
    "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",
],
}

tt_triggers = [
   "HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg",
   "HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg",
   "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg",
   "HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
   "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
]

# 
# categories
# mt: SS, OS
# tt: SS, OS

# include total n events in text
# 
# mt want :
#     for given trigger, show 2d with Cut Based vs MVA
# 

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
from array import array

# return x, y postion for filling
# x = tau1 MVA
# y = tau2 MVA
def getTauTau2D( row, iso ) :
    assert( iso == 'MVA' or iso == 'CmbIso' or iso == 'Mix' ), "Poor isolation choice %s" % iso
    if iso == 'MVA' :
        x = getIsoCodeMVA( row, 't' )
        y = getIsoCodeMVA( row, 't2' )
    elif iso == 'CmbIso' :
        x = getIsoCodeCmbIso( row, 't' )
        y = getIsoCodeCmbIso( row, 't2' )
    elif iso == 'Mix' :
        # For Mixed, only to tau1, this is for mt channel mainly
        x = getIsoCodeMVA( row, 't' )
        y = getIsoCodeCmbIso( row, 't' )
    return [x, y]


# return a value which fills with the tighest iso WP passed
def getIsoCodeMVA( row, lep ) :
    # None = 0, VL = 1, L = 2, M = 3, T = 4, VT = 5, VVT = 6
    #if getattr( row, lep+'MVAIsoVLoose' ) == 0 :   return 0
    #if getattr( row, lep+'MVAIsoLoose' ) == 0 :    return 1
    #if getattr( row, lep+'MVAIsoMedium' ) == 0 :   return 2
    #if getattr( row, lep+'MVAIsoTight' ) == 0 :    return 3
    #if getattr( row, lep+'MVAIsoVTight' ) == 0 :   return 4
    #if getattr( row, lep+'MVAIsoVVTight' ) == 0 :  return 5
    #if getattr( row, lep+'MVAIsoVVTight' ) == 1 :      return 6
    if getattr( row, lep+'MVAIsoLoose' ) == 0 :    return 0
    if getattr( row, lep+'MVAIsoMedium' ) == 0 :   return 1
    if getattr( row, lep+'MVAIsoTight' ) == 0 :    return 2
    if getattr( row, lep+'MVAIsoVTight' ) == 0 :   return 3
    if getattr( row, lep+'MVAIsoVVTight' ) == 0 :  return 4
    if getattr( row, lep+'MVAIsoVVTight' ) == 1 :      return 5
    else : return 0



# return a value which fills with the tighest iso WP passed
def getIsoCodeCmbIso( row, lep ) :
    # None = 0, L = 1, M = 2, T = 3
    if getattr( row, lep+'IsoCmbLoose' ) == 0 :  return 0
    if getattr( row, lep+'IsoCmbMedium' ) == 0 : return 1
    if getattr( row, lep+'IsoCmbTight' ) == 0 :  return 2
    if getattr( row, lep+'IsoCmbTight' ) == 1 :  return 3
    else : return 0


def getTrigAndTau2D( row, iso, orderedTriggers ) :
    assert( iso == 'MVA' or iso == 'CmbIso' ), "Poor isolation choice %s" % iso
    if iso == 'MVA' :
        x = getTrigCode( row, orderedTriggers )
        y = getIsoCodeMVA( row, 't' )
    elif iso == 'CmbIso' :
        x = getTrigCode( row, orderedTriggers )
        y = getIsoCodeCmbIso( row, 't' )
    return [x, y]


# return a value which fills with HLT Trigger related values
def getTrigCode( row, orderedTriggers ) :
    # None = 0, 1 = passing trig1, 2 = passing trig2...
    # XXX 0 = passing trig1, 1 = passing trig2...   do j instead of j+1 for return
    if getattr( row, orderedTriggers[0] ) == 0 :  return 0
    for j in range( len(orderedTriggers) ) :
        if j == len(orderedTriggers)-1 :
            if getattr( row, orderedTriggers[j] ) == 1 :  return j+1
        else : # all the frst triggers, check first and 1 above
            if getattr( row, orderedTriggers[j] ) == 1 and \
                getattr( row, orderedTriggers[j+1] ) == 0 :  return j+1
    # print orderedTriggers[-1], getattr( row, orderedTriggers[-1] )
    #if getattr( row, orderedTriggers[-1] ) == 1 : return i
    else : return -1


def passes_basic_mt_cuts( row ) :
    if getattr( row, 'transMass' ) > 30 : return 0
    if getattr( row, 'SS' ) == 0 :        return 0
    #if getattr( row, 'SS' ) == 1 :        return 0
    if getattr( row, 'm_vis' ) < 40 :     return 0
    if getattr( row, 'm_vis' ) > 80 :     return 0
    if getattr( row, 'mTrigMatch' ) < 0.5 :  return 0
    if getattr( row, 'tTrigMatch' ) < 0.5 :  return 0
    if getattr( row, 'tMVAIsoVLoose' ) < 0.5 :  return 0
    if getattr( row, 'HLT_IsoMu24_eta2p1' ) < 0.5 : return 0
    return 1


def passes_basic_tt_cuts( row ) :
    if getattr( row, 'SS' ) == 1 :           return 0
    if getattr( row, 'tPt' ) < 40 :          return 0
    if getattr( row, 't2Pt' ) < 40 :         return 0
    if getattr( row, 'tTrigMatch' ) < 0.5 :  return 0
    if getattr( row, 't2TrigMatch' ) < 0.5 : return 0
    if getattr( row, 'tMVAIsoVLoose' ) < 0.5 :  return 0
    if getattr( row, 't2MVAIsoVLoose' ) < 0.5 :  return 0
    return 1


def loop( c, tree, data_set, h_mvas, h_cmbs, h_mixs, h_trigs ) :
    for row in tree :
        mva_vals = getTauTau2D( row, 'MVA' ) 
        cmb_vals = getTauTau2D( row, 'CmbIso' )
        mix_vals = getTauTau2D( row, 'Mix' )
        #print i
        #print " -- %i %i" % (mva_vals[0], mva_vals[1])
        #print " -- %i %i" % (cmb_vals[0], cmb_vals[1])
    
        if data_set == 'mt' :
            if not passes_basic_mt_cuts( row ) : continue
        if data_set == 'tt' :
            if not passes_basic_tt_cuts( row ) : continue
    
        for trig, hist in h_mvas.iteritems() :
            if getattr( row, trig ) > 0.5 :
                hist.Fill( mva_vals[0], mva_vals[1], 1 ) 
                # Map to cmb WPs
                h_cmbs[trig].Fill( cmb_vals[0], cmb_vals[1], 1 ) 
                h_mixs[trig].Fill( mix_vals[0], mix_vals[1], 1 ) 

        if data_set == 'mt' :
            for trigGroup, hist in h_trigs.iteritems() :
                trig_vals = getTrigAndTau2D( row, 'MVA', mt_trigger_groups[ trigGroup ] )
                hist.Fill( trig_vals[0], trig_vals[1] )
    
        #h_cmb.Fill( cmb_vals[0], cmb_vals[1], 1 )
    dumpNameAndInt = {}
    plotBase='/afs/cern.ch/user/t/truggles/www/HLT_Studies/july09/'
    for trig, hist in h_mvas.iteritems() :
        c.Clear()
        dumpNameAndInt[trig] = hist.Integral()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        ROOT.gPad.SetLogz(1)
        c.SaveAs(plotBase+'%s_mva_%s.png' % (data_set, trig) )
    for trig, hist in h_cmbs.iteritems() :
        c.Clear()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        c.SaveAs(plotBase+'%s_cmb_%s.png' % (data_set, trig) )
    for trig, hist in h_mixs.iteritems() :
        c.Clear()
        if hist.Integral() > 0 :
            hist.Scale( 1. / hist.Integral() )
        hist.Draw('COLZ')
        c.SaveAs(plotBase+'%s_mix_%s.png' % (data_set, trig) )
    if data_set == 'mt' :
        for trigGroup, hist in h_trigs.iteritems() :
            c.Clear()
            if hist.Integral() > 0 :
                hist.Scale( 1. / hist.Integral() )
            hist.Draw('COLZ')
            ROOT.gPad.SetLogz(1)
            c.SaveAs(plotBase+'%s_trigger_%s.png' % (data_set, trigGroup) )
            ROOT.gPad.SetLogz(0)

            # Save an 'efficiency' version
            c.Clear()
            fill_for_efficiency( hist )
            hist.Draw('COLZ TEXT')
            c.SaveAs(plotBase+'%s_trigger_eff_%s.png' % (data_set, trigGroup) )
    for k, v in dumpNameAndInt.iteritems() :
        print k, v

bin_label_map_mva = {
    #1 : 'None',
    #2 : 'VLoose',
    #3 : 'Loose',
    #4 : 'Medium',
    #5 : 'Tight',
    #6 : 'VTight',
    #7 : 'VVTight',
    1 : 'VLoose',
    2 : 'Loose',
    3 : 'Medium',
    4 : 'Tight',
    5 : 'VTight',
    6 : 'VVTight',
}

bin_label_map_cmb = {
    1 : 'None',
    2 : 'Loose',
    3 : 'Medium',
    4 : 'Tight',
}

def make_mva2d_plot( trigger='' ) :
    h_mva = ROOT.TH2D( 'Tau MVA'+trigger, 'Tau MVA ID/Iso WPs %s;Tau1 MVA WP;Tau2 MVA WP' % trigger, 6,-0.5,5.5,6,-0.5,5.5 )
    for k, v in bin_label_map_mva.iteritems() :
        h_mva.GetXaxis().SetBinLabel( k, v )
        h_mva.GetYaxis().SetBinLabel( k, v )
    h_mva.SetDirectory(0)
    return h_mva

def make_cmb2d_plot( trigger='' ) :
    h_cmb = ROOT.TH2D( 'Tau Cmb'+trigger, 'Tau Cmb ID/Iso WPs %s;Tau1 CutBased WP;Tau2 CutBased WP' % trigger, 4,-0.5,3.5,4,-0.5,3.5 )
    for k, v in bin_label_map_cmb.iteritems() :
        h_cmb.GetXaxis().SetBinLabel( k, v )
        h_cmb.GetYaxis().SetBinLabel( k, v )
    h_cmb.SetDirectory(0)
    return h_cmb

def make_mva_vs_cmb2d_plot( trigger='' ) :
    h_mix = ROOT.TH2D( 'Tau MVA Cmb'+trigger, 'Tau MVA vs Cmb ID/Iso WPs %s;Tau1 MVA WP;Tau1 CutBased WP' % trigger, 6,-0.5,5.5,4,-0.5,3.5 )
    for k, v in bin_label_map_mva.iteritems() :
        h_mix.GetXaxis().SetBinLabel( k, v )
    for k, v in bin_label_map_cmb.iteritems() :
        h_mix.GetYaxis().SetBinLabel( k, v )
    h_mix.SetDirectory(0)
    return h_mix

def make_trig_vs_mva2d_plot( triggerName, orderedTriggers ) :
    h_trig = ROOT.TH2D( 'Trigger MVA'+triggerName, 'Triggers vs MVA: %s;Cross Trigger Passed;Tau MVA WP' % orderedTriggers[0].replace('Loose','X'), len(orderedTriggers)+1,-0.5,len(orderedTriggers)+1,6,-0.5,5.5 )
    h_trig.GetXaxis().SetBinLabel( 1, 'None' )
    for i, name in enumerate(orderedTriggers) :
        j = i + 2 # Use if you want first bin to be None
        #j = i + 1
        print j, name
        fillName = name.replace('HLT_IsoMu24_eta2p1_','')
        fillName = fillName.replace('ChargedIsoPFTau','')
        fillName = fillName.replace('_Trk1','')
        fillName = fillName.replace('_TightID','')
        fillName = fillName.replace('_eta2p1_Reg_CrossL1','')
        fillName = fillName.replace('_SingleL1','')
        h_trig.GetXaxis().SetBinLabel( j, fillName )
    for k, v in bin_label_map_mva.iteritems() :
        h_trig.GetYaxis().SetBinLabel( k, v )
    h_trig.GetYaxis().SetTitleOffset( h_trig.GetYaxis().GetTitleOffset() * 2 )
    h_trig.SetDirectory(0)
    return h_trig


def fill_for_efficiency( hist ) :
    nx = hist.GetXaxis().GetNbins()
    ny = hist.GetYaxis().GetNbins()
    fillMap = {}
    for x in range( nx ) :
        for y in range( ny ) :
            fillMap[x,y] = hist.Integral( x+1, nx, y+1, ny )
    for x in range( nx ) :
        for y in range( ny ) :
            hist.SetBinContent( x+1, y+1, fillMap[x,y] ) 
    # Set lower left corner == 1 (100%)
    lower_left = hist.GetBinContent( 1, 1)
    hist.Scale( 1. / lower_left )

for channel in ['mt',]:# 'tt'] :

    # Channel specific setup
    if channel == 'mt' :
        triggers = mt_triggers
        f = ROOT.TFile('/data/truggles/hlt_studies_july09_v2/miniAOD_muon.root', 'r')
        #f = ROOT.TFile('/data/truggles/hlt_studies_2/miniAOD_muon.root', 'r')
    if channel == 'tt' :
        triggers = tt_triggers
        f = ROOT.TFile('/data/truggles/hlt_studies_july09/miniAOD_tau.root', 'r') 
    tree = f.Get('tauMiniAODHLTStudies/tagAndProbe/Ntuple')

    print f
    print tree
    
    c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    
    #h_mva = make_mva2d_plot()
    #h_cmb = make_cmb2d_plot()
    h_mvas = {}
    h_cmbs = {}
    h_mixs = {}
    h_trigs = {}


    for trig in triggers :
        print trig
        h_mvas[ trig ] = make_mva2d_plot(trig)
        h_cmbs[ trig ] = make_cmb2d_plot(trig)
        h_mixs[ trig ] = make_mva_vs_cmb2d_plot(trig)
    for group, names in mt_trigger_groups.iteritems() :
        h_trigs[ group ] = make_trig_vs_mva2d_plot( group, names )
    
    
    loop( c, tree, channel, h_mvas, h_cmbs, h_mixs, h_trigs )


    for trig in triggers :
        del h_mvas[ trig ]
        del h_cmbs[ trig ]
        del h_mixs[ trig ]
    for group, names in mt_trigger_groups.iteritems() :
        del h_trigs [ group ]
    del c, p







