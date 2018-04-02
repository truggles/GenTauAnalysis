
import ROOT
from array import array
import os
from helpers import *
ROOT.gROOT.SetBatch(True)


name = 'rate_feb16_v60per'
#name = 'rate_feb15_default'
#name = 'rate_feb16_v60pMT30pL_pTreset'
name = 'rate_feb17'
name = 'rate_feb17_full'
name = 'rate_feb20'
name = 'rate_feb20_cut'
name = 'rate_feb25_cut'
name = 'rate_feb25'
name = 'rate_feb27'
name = 'rate_feb27_nonReg'
name = 'rate_april02_cut'


plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )


iFile = ROOT.TFile(name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )



def getRateAndPlot( iTree, plotBase, hpsTrigger, cut, saveName ) :
    c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
    p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
    p.Draw()
    p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
    p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
    p.Draw()
    p.cd()
    axes = ';HPS-enabled Trigger;Current Trigger'
    h = ROOT.TH2D( saveName, saveName+' HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
    if 'HLT_VBF' in hpsTrigger :
        iTree.Draw('%s:%s >> %s' % (hpsTrigger.replace('HPS','').replace('_Reg',''), hpsTrigger, saveName), cut, "COLZ TEXT")
    else :
        iTree.Draw('%s:%s >> %s' % (hpsTrigger.replace('HPS',''), hpsTrigger, saveName), cut, "COLZ TEXT")
    c.SaveAs( plotBase+saveName.replace(' ','_')+'.png' )
    print "%s %i %i %i" % (hpsTrigger.replace('HPS',''), h.GetBinContent(1, 2), h.GetBinContent(2, 1), h.GetBinContent(2, 2) )
    
    del h, c, p




#runLumiCut = "( (RunNumber == 305636 && ( (lumi >= 60 && lumi < 167) || (lumi >= 199 && lumi < 673) )) || (RunNumber == 305186 && (lumi >= 232 && lumi < 407) ) )"
runLumiCut = "RunNumber == 305636 && lumi >= 199 && lumi < 528"

# Missing
# Add ETau
# Tau+MET
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauTrigger#Trigger_table_for_2017

trigMap = {
    'di-Tau35_Medium' : 'HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg',
    #'di-Tau35_Tight' : 'HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg',
    #'di-Tau35_Medium_TightID' : 'HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg',
    #'di-Tau35_Tight_TightID' : 'HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg',
    #'di-Tau40_Medium' : 'HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_eta2p1_Reg',
    #'di-Tau40_Tight' : 'HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg',
    #'di-Tau40_Medium_TightID' : 'HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg',
    #'di-Tau40_Tight_TightID' : 'HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg',
    'mu20Tau27_Loose' : 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1',
    #'mu20Tau27_Medium' : 'HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1',
    #'mu20Tau27_Tight' : 'HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_CrossL1',
    #'mu20Tau27_Loose_TightID' : 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1',
    #'mu20Tau27_Medium_TightID' : 'HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1',
    #'mu20Tau27_Tight_TightID' : 'HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1',
    'vbf_Loose' : 'HLT_VBF_DoubleLooseChargedIsoPFTauHPS20_Trk1_eta2p1_Reg',
    #'vbf_Medium' : 'HLT_VBF_DoubleMediumChargedIsoPFTauHPS20_Trk1_eta2p1_Reg',
    #'vbf_Tight' : 'HLT_VBF_DoubleTightChargedIsoPFTauHPS20_Trk1_eta2p1_Reg',
    #'Tau50Med_1pr' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr',
    #'singleTau180' : 'HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1',
    #'singleTau180_1pr' : 'HLT_MediumChargedIsoPFTauHPS180HighPtRelaxedIso_Trk50_eta2p1_1pr',

    #'mon_Tau50_Medium_1pr' : 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr',
    #'mon_di-Tau35_Medium' : 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1',
    #'mon_di-Tau35_Tight' : 'HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1',
    #'mon_di-Tau35_Medium_TightID' : 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1',
    #'mon_di-Tau35_Tight_TightID' : 'HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1',

    'singleTau50_Medium_1pr' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr',

    #'tau50_MET90' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr_MET90',
    #'tau50_MET100' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr_MET100',
    #'tau50_MET110' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr_MET110',
    #'tau50_MET130' : 'HLT_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr_MET130',

    'Elec24_Tau30_Loose' : 'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1',
    #'Elec24_Tau30_Loose_tightID' : 'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1',
    #'Elec24_Tau30_Medium' : 'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTauHPS30_eta2p1_CrossL1',
    #'Elec24_Tau30_Medium_tightID' : 'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1',
    #'Elec24_Tau30_Tight' : 'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTauHPS30_eta2p1_CrossL1',
    #'Elec24_Tau30_Tight_tightID' : 'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1',
}


print "Trigger Pure_Default Pure_HPS Shared"
for saveName, hpsTrigger in trigMap.iteritems() :
    getRateAndPlot( iTree, plotBase, hpsTrigger, runLumiCut, saveName )

c = ROOT.TCanvas( 'c', 'c', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

h_dm_hps_conebased = make_DM_plot( 'Online HPS', 'Online Cone-based' )
h_dm_hps_conebased30to80 = make_DM_plot( 'Online HPS pt30to80', 'Online Cone-based' )
h_dm_hps_conebased80to150 = make_DM_plot( 'Online HPS pt80to150', 'Online Cone-based' )
h_dm_hps_conebased150plus = make_DM_plot( 'Online HPS pt150plus', 'Online Cone-based' )

h_dm_hps_conebased_DRMatch = make_DM_plot( 'Online HPS DR Matched', 'Online Cone-based' )
h_dm_hps_conebased_DRMatch30to80 = make_DM_plot( 'Online HPS DR Matched pt30to80', 'Online Cone-based' )
h_dm_hps_conebased_DRMatch80to150 = make_DM_plot( 'Online HPS DR Matched pt80to150', 'Online Cone-based' )
h_dm_hps_conebased_DRMatch150plus = make_DM_plot( 'Online HPS DR Matched pt150plus', 'Online Cone-based' )

trigger1 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1'
trigger2 = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1'
trigger1 = 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS50_Trk30_eta2p1_1pr'
trigger2 = 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr'

cnt = 0
for row in iTree :
    cnt += 1
    #if row.RunNumber != 305636 : continue
    #if row.lumi < 199 : continue
    #if row.lumi > 527 : continue
    if cnt%1000 == 0 :
        print "RunNumber",row.RunNumber,row.lumi,cnt
    #if getattr( row, trigger1 ) < 0.5 and getattr( row, trigger2 ) < 0.5 : continue 

    if row.defaultTauSize < 1 and row.hpsTauSize < 1 : continue

    if row.defaultTauPt < 30 and row.hpsTauPt < 30 : continue


    hpsDM = row.hpsTauDM
    defaultDM = row.defaultTauDM

    hpsCode = getDMCode( hpsDM )
    defaultCode = getDMCode( defaultDM )

    h_dm_hps_conebased.Fill( hpsCode, defaultCode )
    if row.hpsTauPt > 30 and row.hpsTauPt < 80 :
        h_dm_hps_conebased30to80.Fill( hpsCode, defaultCode )
    elif row.hpsTauPt > 80 and row.hpsTauPt < 150 :
        h_dm_hps_conebased80to150.Fill( hpsCode, defaultCode )
    elif row.hpsTauPt > 150 :
        h_dm_hps_conebased150plus.Fill( hpsCode, defaultCode )

    if row.hpsTauDRDefault > 0.5 : continue
    if row.hpsTauDRDefault < 0.0 : continue
    h_dm_hps_conebased_DRMatch.Fill( hpsCode, defaultCode )
    if row.hpsTauPt > 30 and row.hpsTauPt < 80 :
        h_dm_hps_conebased_DRMatch30to80.Fill( hpsCode, defaultCode )
    elif row.hpsTauPt > 80 and row.hpsTauPt < 150 :
        h_dm_hps_conebased_DRMatch80to150.Fill( hpsCode, defaultCode )
    elif row.hpsTauPt > 150 :
        h_dm_hps_conebased_DRMatch150plus.Fill( hpsCode, defaultCode )

print "hpsVsConeBased"
saveHists( c, h_dm_hps_conebased, plotBase+'hpsVsConebased' )
saveHists( c, h_dm_hps_conebased30to80, plotBase+'hpsVsConebased30to80' )
saveHists( c, h_dm_hps_conebased80to150, plotBase+'hpsVsConebased80to150' )
saveHists( c, h_dm_hps_conebased150plus, plotBase+'hpsVsConebased150plus' )

saveHists( c, h_dm_hps_conebased_DRMatch, plotBase+'hpsVsConebased_DRMatch' )
saveHists( c, h_dm_hps_conebased_DRMatch30to80, plotBase+'hpsVsConebased_DRMatch30to80' )
saveHists( c, h_dm_hps_conebased_DRMatch80to150, plotBase+'hpsVsConebased_DRMatch80to150' )
saveHists( c, h_dm_hps_conebased_DRMatch150plus, plotBase+'hpsVsConebased_DRMatch150plus' )

