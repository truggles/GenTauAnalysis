
import ROOT
from array import array
import os
ROOT.gROOT.SetBatch(True)


name = 'rate_feb16_v60per'
#name = 'rate_feb15_default'
#name = 'rate_feb16_v60pMT30pL_pTreset'
name = 'rate_feb17'
name = 'rate_feb17_full'


plotBase='/afs/cern.ch/user/t/truggles/www/hps_at_hlt/plotting/'+name+'/'
if not os.path.exists( plotBase ) : os.makedirs( plotBase )


iFile = ROOT.TFile(name+'.root','r')
print iFile
iTree = iFile.Get( 'hpsTauHLTStudies/tagAndProbe/Ntuple' )


c = ROOT.TCanvas( 'c1', 'c1', 600, 600 ) 
p = ROOT.TPad( 'p1', 'p1', 0, 0, 1, 1 )
p.Draw()
p.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.5 )
p.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.5 )
p.Draw()
p.cd()

axes = ';HPS-enabled Trigger;Current Trigger'
h_med = ROOT.TH2D('med', 'di-Tau 35 Med HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
h_med_muTau = ROOT.TH2D('med_muTau', 'muTau 27 Med HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
h_loose_vbf = ROOT.TH2D('loose_vbf', 'VBF Loose HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
h_loose_muTau = ROOT.TH2D('loose_muTau', 'muTau Loose HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
h_tight = ROOT.TH2D('tight', 'di-Tau 35 Tight HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )
h_tight_muTau = ROOT.TH2D('tight_muTau', 'muTau 27 Tight HLT Acceptance'+axes, 2, -0.5, 1.5, 2, -0.5, 1.5 )

#runLumiCut = "( (RunNumber == 305636 && ( (lumi >= 60 && lumi < 167) || (lumi >= 199 && lumi < 673) )) || (RunNumber == 305186 && (lumi >= 232 && lumi < 407) ) )"
runLumiCut = "RunNumber == 305636 && lumi >= 199 && lumi < 528"

iTree.Draw("HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg:HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg >> med", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'di-TauMed.png' )

iTree.Draw("HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1:HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1 >> med_muTau", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'muTauMed.png' )

iTree.Draw("HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg:HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg >> tight", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'di-TauTight.png' )

iTree.Draw("HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1:HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_CrossL1 >> tight_muTau", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'muTauTight.png' )

iTree.Draw("HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg:HLT_VBF_DoubleLooseChargedIsoPFTauHPS20_Trk1_eta2p1_Reg >> loose_vbf", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'VBF_Loose.png' )

iTree.Draw("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 >> loose_muTau", runLumiCut, "COLZ TEXT")
c.SaveAs( plotBase+'MuTau_Loose.png' )


