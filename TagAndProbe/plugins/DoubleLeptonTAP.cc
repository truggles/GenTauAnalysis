// -*- C++ -*-
//
// Package:    THRAnalysis/TagAndProbe
// Class:      DoubleLeptonTAP
// 
/**\class DoubleLeptonTAP DoubleLeptonTAP.cc THRAnalysis/TagAndProbe/plugins/DoubleLeptonTAP.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tyler Henry Ruggles
//         Created:  Sun, 18 June 2017
//
//
// Modified off of THRAnalysis/TauHLTStudies/plugins/TauHLTStudiesMiniAODAnalyzer.cc
// for use with double electron / double muon triggers


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

// Added
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "TLorentzVector.h"
#include "TMath.h"
#include "TTree.h"
#include "TH1D.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminator.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/deltaR.h"

// Trigger stuff...
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"
#include "DataFormats/L1Trigger/interface/Tau.h"

// Electron missing hits
#include "DataFormats/TrackReco/interface/HitPattern.h"

// Lepton track extractor
//#include "FinalStateAnalysis/PatTools/interface/PATLeptonTrackVectorExtractor.h"
#include "THRAnalysis/TagAndProbe/include/PATLeptonTrackVectorExtractor.h"

#include <algorithm>
#include <map>

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class DoubleLeptonTAP : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit DoubleLeptonTAP(const edm::ParameterSet&);
      ~DoubleLeptonTAP();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      //bool isData;
      //bool doDoubleMu;
      //bool doDoubleE;
      bool verbose;
      edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;
      edm::EDGetTokenT<std::vector<pat::Muon>> muonToken_;
      edm::EDGetTokenT<std::vector<pat::Electron>> electronToken_;
      edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
      edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
      edm::EDGetTokenT<std::vector<reco::Vertex>> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
      ek::PATLeptonTrackVectorExtractor<pat::Electron> trackExtractorElec_;
      ek::PATLeptonTrackVectorExtractor<pat::Muon> trackExtractorMuon_;

      TTree *tree;
      TH1D *nEvents;
      TH1D *cutFlow;
      double eventD;
      float run, lumi, nTruePU, nvtx, nvtxCleaned, passingMuons, passingElectrons,
        l1Pt, l1Eta, l1Phi, l1Iso, l1hltPt,
        l1LooseMuon, l1MediumMuon, l1ElecWP90, l1ElecWP80,
        l2Pt, l2Eta, l2Phi, l2Iso, l2hltPt,
        l2LooseMuon, l2MediumMuon, l2ElecWP90, l2ElecWP80,
        m_vis, transMass, met, metPhi, SS, nBTags,
        leptonDR_l11_l22;
      std::map<std::string, int*> triggers;
      std::map<std::string, int*> l1MatchTriggers;
      std::map<std::string, int*> l2MatchTriggers;
      std::map<std::string, int>::iterator triggerIterator;
      int l1Match_HLT_IsoMu27;
      int l1Match_HLT_IsoMu24;
      int l1Match_HLT_IsoTkMu24;
      int l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
      int l1Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
      int l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
      int l1Match_HLT_Mu17_TrkIsoVVL;
      int l1Match_HLT_Mu8;
      int l1Match_HLT_Mu8_TrkIsoVVL;
      int l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
      int l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
      int l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
      int l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
      int l1Match_HLT_Ele27_WPTight_Gsf;
      int l2Match_HLT_IsoMu27;
      int l2Match_HLT_IsoTkMu24;
      int l2Match_HLT_IsoMu24;
      int l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
      int l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
      int l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
      int l2Match_HLT_Mu17_TrkIsoVVL;
      int l2Match_HLT_Mu8;
      int l2Match_HLT_Mu8_TrkIsoVVL;
      int l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
      int l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
      int l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
      int l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
      int l2Match_HLT_Ele27_WPTight_Gsf;
      int HLT_IsoMu27;
      int HLT_IsoMu24;
      int HLT_IsoTkMu24;
      int HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
      int HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
      int HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
      int HLT_Mu17_TrkIsoVVL;
      int HLT_Mu8;
      int HLT_Mu8_TrkIsoVVL;
      int HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
      int HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
      int HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
      int HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
      int HLT_Ele27_WPTight_Gsf;

};

//
// constants, enums and typedefs
typedef std::map<std::string, int>::iterator iter;
//

//
// static data member definitions
//

//
// constructors and destructor
//
DoubleLeptonTAP::DoubleLeptonTAP(const edm::ParameterSet& iConfig) :
    //isData(iConfig.getUntrackedParameter<bool>("isData", false)),
    //doDoubleMu(iConfig.getUntrackedParameter<bool>("doDoubleMu", false)),
    //doDoubleE(iConfig.getUntrackedParameter<bool>("doDoubleE", false)),
    verbose(iConfig.getUntrackedParameter<bool>("verbose", false)),
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc"))),
    muonToken_(consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muonSrc"))),
    electronToken_(consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
    jetToken_(consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
    metToken_(consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metSrc"))),
    vertexToken_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("pvSrc"))),
    triggerToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerSrc"))),
    triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjectsSrc")))
{
   //now do what ever initialization is needed
   //usesResource("TFileService");
   edm::Service<TFileService> fs;

   l1MatchTriggers["HLT_IsoMu27_v"]                                              = &l1Match_HLT_IsoMu27;
   l1MatchTriggers["HLT_IsoMu24_v"]                                              = &l1Match_HLT_IsoMu24;
   l1MatchTriggers["HLT_IsoTkMu24_v"]                                            = &l1Match_HLT_IsoTkMu24;
   l1MatchTriggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v"]                    = &l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
   l1MatchTriggers["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"]                      = &l1Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
   l1MatchTriggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v"]                       = &l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
   l1MatchTriggers["HLT_Mu17_TrkIsoVVL_v"]                                       = &l1Match_HLT_Mu17_TrkIsoVVL;
   l1MatchTriggers["HLT_Mu8_v"]                                                  = &l1Match_HLT_Mu8;
   l1MatchTriggers["HLT_Mu8_TrkIsoVVL_v"]                                        = &l1Match_HLT_Mu8_TrkIsoVVL;
   l1MatchTriggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"]                = &l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
   l1MatchTriggers["HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v"]                         = &l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
   l1MatchTriggers["HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                         = &l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
   l1MatchTriggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                   = &l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
   l1MatchTriggers["HLT_Ele27_WPTight_Gsf_v"]                                    = &l1Match_HLT_Ele27_WPTight_Gsf;

   l2MatchTriggers["HLT_IsoMu27_v"]                                              = &l2Match_HLT_IsoMu27;
   l2MatchTriggers["HLT_IsoMu24_v"]                                              = &l2Match_HLT_IsoMu24;
   l2MatchTriggers["HLT_IsoTkMu24_v"]                                            = &l2Match_HLT_IsoTkMu24;
   l2MatchTriggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v"]                    = &l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
   l2MatchTriggers["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"]                      = &l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
   l2MatchTriggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v"]                       = &l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
   l2MatchTriggers["HLT_Mu17_TrkIsoVVL_v"]                                       = &l2Match_HLT_Mu17_TrkIsoVVL;
   l2MatchTriggers["HLT_Mu8_v"]                                                  = &l2Match_HLT_Mu8;
   l2MatchTriggers["HLT_Mu8_TrkIsoVVL_v"]                                        = &l2Match_HLT_Mu8_TrkIsoVVL;
   l2MatchTriggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"]                = &l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
   l2MatchTriggers["HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v"]                         = &l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
   l2MatchTriggers["HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                         = &l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
   l2MatchTriggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                   = &l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
   l2MatchTriggers["HLT_Ele27_WPTight_Gsf_v"]                                    = &l2Match_HLT_Ele27_WPTight_Gsf;

   triggers["HLT_IsoMu27_v"]                                              = &HLT_IsoMu27;
   triggers["HLT_IsoMu24_v"]                                              = &HLT_IsoMu24;
   triggers["HLT_IsoTkMu24_v"]                                            = &HLT_IsoTkMu24;
   triggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v"]                    = &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ;
   triggers["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v"]                      = &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ;
   triggers["HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v"]                       = &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL;
   triggers["HLT_Mu17_TrkIsoVVL_v"]                                       = &HLT_Mu17_TrkIsoVVL;
   triggers["HLT_Mu8_v"]                                                  = &HLT_Mu8;
   triggers["HLT_Mu8_TrkIsoVVL_v"]                                        = &HLT_Mu8_TrkIsoVVL;
   triggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v"]                = &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ;
   triggers["HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v"]                         = &HLT_Ele23_CaloIdL_TrackIdL_IsoVL;
   triggers["HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                         = &HLT_Ele12_CaloIdL_TrackIdL_IsoVL;
   triggers["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v"]                   = &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL;
   triggers["HLT_Ele27_WPTight_Gsf_v"]                                    = &HLT_Ele27_WPTight_Gsf;

   TFileDirectory subDir = fs->mkdir( "tagAndProbe" );
   nEvents = subDir.make<TH1D>("nEvents","nEvents",1,-0.5,0.5);
   cutFlow = subDir.make<TH1D>("cutFlow","cutFlow",10,-0.5,9.5);
   tree = subDir.make<TTree>("Ntuple","My T-A-P Ntuple");
   tree->Branch("run",&run,"run/F");
   tree->Branch("lumi",&lumi,"lumi/F");
   tree->Branch("eventD",&eventD,"eventD/D");
   tree->Branch("nTruePU",&nTruePU,"nTruePU/F");
   tree->Branch("nvtx",&nvtx,"nvtx/F");
   tree->Branch("nvtxCleaned",&nvtxCleaned,"nvtxCleaned/F");
   tree->Branch("passingElectrons",&passingElectrons,"passingElectrons/F");
   tree->Branch("passingMuons",&passingMuons,"passingMuons/F");
   tree->Branch("l1Pt",&l1Pt,"l1Pt/F");
   tree->Branch("l1Eta",&l1Eta,"l1Eta/F");
   tree->Branch("l1Phi",&l1Phi,"l1Phi/F");
   tree->Branch("l1Iso",&l1Iso,"l1Iso/F");
   tree->Branch("l1hltPt",&l1hltPt,"l1hltPt/F");
   tree->Branch("l1LooseMuon",&l1LooseMuon,"l1LooseMuon/F");
   tree->Branch("l1MediumMuon",&l1MediumMuon,"l1MediumMuon/F");
   tree->Branch("l1ElecWP90",&l1ElecWP90,"l1ElecWP90/F");
   tree->Branch("l1ElecWP80",&l1ElecWP80,"l1ElecWP80/F");
   tree->Branch("l2Pt",&l2Pt,"l2Pt/F");
   tree->Branch("l2Eta",&l2Eta,"l2Eta/F");
   tree->Branch("l2Phi",&l2Phi,"l2Phi/F");
   tree->Branch("l2Iso",&l2Iso,"l2Iso/F");
   tree->Branch("l2hltPt",&l2hltPt,"l2hltPt/F");
   tree->Branch("l2LooseMuon",&l2LooseMuon,"l2LooseMuon/F");
   tree->Branch("l2MediumMuon",&l2MediumMuon,"l2MediumMuon/F");
   tree->Branch("l2ElecWP90",&l2ElecWP90,"l2ElecWP90/F");
   tree->Branch("l2ElecWP80",&l2ElecWP80,"l2ElecWP80/F");
   tree->Branch("leptonDR_l11_l22",&leptonDR_l11_l22,"leptonDR_l11_l22/F");
   tree->Branch("m_vis",&m_vis,"m_vis/F");
   tree->Branch("transMass",&transMass,"transMass/F");
   tree->Branch("met",&met,"met/F");
   tree->Branch("metPhi",&metPhi,"metPhi/F");
   tree->Branch("SS",&SS,"SS/F");
   tree->Branch("nBTags",&nBTags,"nBTags/F");

   tree->Branch("HLT_IsoMu27",                                 &HLT_IsoMu27,                                  "HLT_IsoMu27/I");
   tree->Branch("HLT_IsoMu24",                                 &HLT_IsoMu24,                                  "HLT_IsoMu24/I");
   tree->Branch("HLT_IsoTkMu24",                               &HLT_IsoTkMu24,                                "HLT_IsoTkMu24/I");
   tree->Branch("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",       &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,        "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ/I");
   tree->Branch("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",         &HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,          "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ/I");
   tree->Branch("HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",          &HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,           "HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL/I");
   tree->Branch("HLT_Mu17_TrkIsoVVL",                          &HLT_Mu17_TrkIsoVVL,                           "HLT_Mu17_TrkIsoVVL/I");
   tree->Branch("HLT_Mu8",                                     &HLT_Mu8,                                      "HLT_Mu8/I");
   tree->Branch("HLT_Mu8_TrkIsoVVL",                           &HLT_Mu8_TrkIsoVVL,                            "HLT_Mu8_TrkIsoVVL/I");
   tree->Branch("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",   &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,    "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ/I");
   tree->Branch("HLT_Ele23_CaloIdL_TrackIdL_IsoVL",            &HLT_Ele23_CaloIdL_TrackIdL_IsoVL,             "HLT_Ele23_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("HLT_Ele12_CaloIdL_TrackIdL_IsoVL",            &HLT_Ele12_CaloIdL_TrackIdL_IsoVL,             "HLT_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",      &HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,       "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("HLT_Ele27_WPTight_Gsf",                       &HLT_Ele27_WPTight_Gsf,                        "HLT_Ele27_WPTight_Gsf/I");

   tree->Branch("l1Match_HLT_IsoMu27",                                 &l1Match_HLT_IsoMu27,                                  "l1Match_HLT_IsoMu27/I");
   tree->Branch("l1Match_HLT_IsoMu24",                                 &l1Match_HLT_IsoMu24,                                  "l1Match_HLT_IsoMu24/I");
   tree->Branch("l1Match_HLT_IsoTkMu24",                               &l1Match_HLT_IsoTkMu24,                                "l1Match_HLT_IsoTkMu24/I");
   tree->Branch("l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",       &l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,        "l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ/I");
   tree->Branch("l1Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",         &l1Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,          "l1Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ/I");
   tree->Branch("l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",          &l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,           "l1Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL/I");
   tree->Branch("l1Match_HLT_Mu17_TrkIsoVVL",                          &l1Match_HLT_Mu17_TrkIsoVVL,                           "l1Match_HLT_Mu17_TrkIsoVVL/I");
   tree->Branch("l1Match_HLT_Mu8",                                     &l1Match_HLT_Mu8,                                      "l1Match_HLT_Mu8/I");
   tree->Branch("l1Match_HLT_Mu8_TrkIsoVVL",                           &l1Match_HLT_Mu8_TrkIsoVVL,                            "l1Match_HLT_Mu8_TrkIsoVVL/I");
   tree->Branch("l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",   &l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,    "l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ/I");
   tree->Branch("l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL",            &l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL,             "l1Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL",            &l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL,             "l1Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",      &l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,       "l1Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l1Match_HLT_Ele27_WPTight_Gsf",                       &l1Match_HLT_Ele27_WPTight_Gsf,                        "l1Match_HLT_Ele27_WPTight_Gsf/I");

   tree->Branch("l2Match_HLT_IsoMu27",                                 &l2Match_HLT_IsoMu27,                                  "l2Match_HLT_IsoMu27/I");
   tree->Branch("l2Match_HLT_IsoMu24",                                 &l2Match_HLT_IsoMu24,                                  "l2Match_HLT_IsoMu24/I");
   tree->Branch("l2Match_HLT_IsoTkMu24",                               &l2Match_HLT_IsoTkMu24,                                "l2Match_HLT_IsoTkMu24/I");
   tree->Branch("l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ",       &l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ,        "l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ/I");
   tree->Branch("l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",         &l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ,          "l2Match_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ/I");
   tree->Branch("l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL",          &l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL,           "l2Match_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL/I");
   tree->Branch("l2Match_HLT_Mu17_TrkIsoVVL",                          &l2Match_HLT_Mu17_TrkIsoVVL,                           "l2Match_HLT_Mu17_TrkIsoVVL/I");
   tree->Branch("l2Match_HLT_Mu8",                                     &l2Match_HLT_Mu8,                                      "l2Match_HLT_Mu8/I");
   tree->Branch("l2Match_HLT_Mu8_TrkIsoVVL",                           &l2Match_HLT_Mu8_TrkIsoVVL,                            "l2Match_HLT_Mu8_TrkIsoVVL/I");
   tree->Branch("l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",   &l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ,    "l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ/I");
   tree->Branch("l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL",            &l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL,             "l2Match_HLT_Ele23_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL",            &l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL,             "l2Match_HLT_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",      &l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL,       "l2Match_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL/I");
   tree->Branch("l2Match_HLT_Ele27_WPTight_Gsf",                       &l2Match_HLT_Ele27_WPTight_Gsf,                        "l2Match_HLT_Ele27_WPTight_Gsf/I");

}


DoubleLeptonTAP::~DoubleLeptonTAP()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
DoubleLeptonTAP::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  // First thing, fill the nEvents
  nEvents->Fill(0.);

  eventD = iEvent.eventAuxiliary().event();
  lumi = iEvent.eventAuxiliary().luminosityBlock();
  run = iEvent.eventAuxiliary().run();
  if (verbose) printf("Run: %.0f    Evt: %.0f   Lumi: %.0f\n", run, eventD, lumi);


  cutFlow->Fill(0., 1.);

  edm::Handle<std::vector<reco::Vertex>> vertices;   
  iEvent.getByToken(vertexToken_, vertices);
  if (vertices->empty()) return; // skip the event if no PV found
  const reco::Vertex &PV = vertices->front();
  if (PV.ndof() < 4) return; // bad vertex
  nvtx = vertices.product()->size();
  nvtxCleaned = 0;
  for (const reco::Vertex &vertex : *vertices)
      if (!vertex.isFake()) ++nvtxCleaned;

  // Get the number of true events
  // This is used later for pile up reweighting
  edm::Handle<std::vector<PileupSummaryInfo>> puInfo;   
  iEvent.getByToken(puToken_, puInfo);
  nTruePU = -99;
  if (puInfo.isValid()) {
      if (puInfo->size() > 0) {
          nTruePU = puInfo->at(1).getTrueNumInteractions();
      }
  }

  cutFlow->Fill(1., 1.); // Good vertex





  edm::Handle<std::vector<pat::Muon>> muons; 
  iEvent.getByToken(muonToken_, muons);
  // Storage for the good Muons
  std::vector<pat::MuonRef> passingMuonsV;

  float mIso;
  for (size_t iMuon = 0; iMuon != muons->size(); ++iMuon) {

      pat::MuonRef muonCandidate(muons, iMuon);

      if (muonCandidate->pt() < 5 || fabs(muonCandidate->eta()) > 2.4 || !muonCandidate->isLooseMuon()) continue;
      mIso = (muonCandidate->pfIsolationR04().sumChargedHadronPt
          + TMath::Max(0., muonCandidate->pfIsolationR04().sumNeutralHadronEt
          + muonCandidate->pfIsolationR04().sumPhotonEt
          - 0.5*muonCandidate->pfIsolationR04().sumPUPt))
          /muonCandidate->pt();
      if (mIso > 0.25) continue;

      // Check deltaR after we have 1 muon, throw away any within dR 0.3 of leading muon
      if (passingMuonsV.size() > 0)
         if (deltaR( passingMuonsV.at(0)->p4(), muonCandidate->p4() ) < 0.3) continue;

      passingMuonsV.push_back( muonCandidate );
  }
  // Require strictly 0 or 2 muons
  //if (doDoubleMu)
  //    if (passingMuonsV.size() != 2) return;
  //if (doDoubleE)
  //    if (passingMuonsV.size() > 0) return;
  if (!(passingMuonsV.size() == 0 || passingMuonsV.size() == 2)) return;
  cutFlow->Fill(2., 1.);
  passingMuons = passingMuonsV.size();




  // Storage for the good Electrons
  std::vector<pat::ElectronRef> passingElectronsV;
  edm::Handle<std::vector<pat::Electron>> electrons;   
  iEvent.getByToken(electronToken_, electrons);
  for (size_t iElec = 0; iElec != electrons->size(); ++iElec) {

      pat::ElectronRef electronCandidate(electrons, iElec);
      if (electronCandidate->pt() < 7 || fabs(electronCandidate->eta()) > 2.5 || 
          electronCandidate->electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp90") < 0.5) continue;
      // No isolation as it is built into MVA WP 90

      // Check conversion veto and missing hits to align with analysis
      if (electronCandidate->gsfTrack()->hitPattern().numberOfAllHits(reco::HitPattern::MISSING_INNER_HITS) >= 2) continue;
      if (electronCandidate->passConversionVeto() < 0.5) continue;

      // Check deltaR after we have 1 electron, throw away any within dR 0.3 of leading electron
      if (passingElectronsV.size() > 0)
         if (deltaR( passingElectronsV.at(0)->p4(), electronCandidate->p4() ) < 0.3) continue;

      passingElectronsV.push_back( electronCandidate );
  }
  // Require strictly 0 or 2 muons
  //if (doDoubleMu)
  //    if (passingElectronsV.size() > 0) return;
  //if (doDoubleE)
  //    if (passingElectronsV.size() != 2) return;
  if (!(passingElectronsV.size() == 0 || passingElectronsV.size() == 2)) return;
  cutFlow->Fill(3., 1.);
  passingElectrons = passingElectronsV.size();


  // Check we don't have 0 or 4 leptons
  if (passingElectronsV.size() + passingMuonsV.size() == 0) return;
  if (passingElectronsV.size() + passingMuonsV.size() == 4) return;
  cutFlow->Fill(4., 1.);



  // Check impact parameters of muons and electrons
  bool passesIPs = true;
  if (passingElectronsV.size() == 2) {
    for (auto electron : passingElectronsV) {
        std::vector<const reco::Track*> tracks = trackExtractorElec_(*electron);
        const reco::Track* track = tracks.size() ? tracks.at(0) : NULL;
        if (track == NULL) {
          passesIPs = false;
          continue;
        }
        if (track->dxy(PV.position()) > 0.045) passesIPs = false; // works for both
        if (track->dz(PV.position()) > 0.2) passesIPs = false; // works for electrons
    }
  }
  if (passingMuonsV.size() == 2) {
    for (auto muon : passingMuonsV) {
        std::vector<const reco::Track*> tracks = trackExtractorMuon_(*muon);
        const reco::Track* track = tracks.size() ? tracks.at(0) : NULL;
        if (track == NULL) {
          passesIPs = false;
          continue;
        }
        if (track->dxy(PV.position()) > 0.045) passesIPs = false; // works for both
        if (muon->muonBestTrack()->dz(PV.position()) > 0.2) passesIPs = false; // muon only
    }
  }

  if (!passesIPs) return;
  cutFlow->Fill(5., 1.);
  



  // Pt order passing reco::muons/electrons
  std::sort(passingElectronsV.begin(), passingElectronsV.end(), [](pat::ElectronRef a, pat::ElectronRef b) {
      return a->pt() > b->pt();
  });
  std::sort(passingMuonsV.begin(), passingMuonsV.end(), [](pat::MuonRef a, pat::MuonRef b) {
      return a->pt() > b->pt();
  });


  // Check for non-overlapping bjets
  // using Medium CISV value of 0.8
  edm::Handle<std::vector<pat::Jet>> jets;   
  iEvent.getByToken(jetToken_, jets);
  nBTags = 0;
  for (const pat::Jet &j : *jets) {
      if (j.pt() < 20 || fabs(j.eta()) > 2.4 || j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") < 0.8484) continue;
      if (passingMuonsV.size() == 2)
        if (deltaR(j, *passingMuonsV.at(0)) < 0.5 || deltaR(j, *passingMuonsV.at(1)) < 0.5) continue;
      if (passingElectronsV.size() == 2)
        if (deltaR(j, *passingElectronsV.at(0)) < 0.5 || deltaR(j, *passingElectronsV.at(1)) < 0.5) continue;
      ++nBTags;
  }
  // FIXME don't cut on bjets right now, curious how many there are in Zee/mm
  //if (btagged) return;
  cutFlow->Fill(6., 1.);


  
  // Get MET for transverse mass calculation 
  edm::Handle<std::vector<pat::MET>> mets;   
  iEvent.getByToken(metToken_, mets);
  const pat::MET &getMet = mets->front();

  transMass = -99;
  //transMass = TMath::Sqrt( 2. * bestMuon.pt() * met.pt() * (1. - TMath::Cos( bestMuon.phi() - met.phi())));
  met = getMet.pt();
  metPhi = getMet.phi();


  if (passingMuonsV.size() == 2) {
      l1Pt = passingMuonsV.at(0)->pt();
      l1Eta = passingMuonsV.at(0)->eta();
      l1Phi = passingMuonsV.at(0)->phi();
      l1Iso = (passingMuonsV.at(0)->pfIsolationR04().sumChargedHadronPt
          + TMath::Max(0., passingMuonsV.at(0)->pfIsolationR04().sumNeutralHadronEt
          + passingMuonsV.at(0)->pfIsolationR04().sumPhotonEt
          - 0.5*passingMuonsV.at(0)->pfIsolationR04().sumPUPt))
          /passingMuonsV.at(0)->pt();
      l1LooseMuon = passingMuonsV.at(0)->isLooseMuon();
      l1MediumMuon = passingMuonsV.at(0)->isMediumMuon();
      l1ElecWP90 = -9;
      l1ElecWP80 = -9;
      l2Pt = passingMuonsV.at(1)->pt();
      l2Eta = passingMuonsV.at(1)->eta();
      l2Phi = passingMuonsV.at(1)->phi();
      l2Iso = (passingMuonsV.at(1)->pfIsolationR04().sumChargedHadronPt
          + TMath::Max(0., passingMuonsV.at(1)->pfIsolationR04().sumNeutralHadronEt
          + passingMuonsV.at(1)->pfIsolationR04().sumPhotonEt
          - 0.5*passingMuonsV.at(1)->pfIsolationR04().sumPUPt))
          /passingMuonsV.at(1)->pt();
      l2LooseMuon = passingMuonsV.at(1)->isLooseMuon();
      l2MediumMuon = passingMuonsV.at(1)->isMediumMuon();
      l2ElecWP90 = -9;
      l2ElecWP80 = -9;

      leptonDR_l11_l22 = deltaR( *passingMuonsV.at(0), *passingMuonsV.at(1));
      // Get Visible Mass
      TLorentzVector l1 = TLorentzVector( 0., 0., 0., 0. );
      l1.SetPtEtaPhiM( passingMuonsV.at(0)->pt(), passingMuonsV.at(0)->eta(),
          passingMuonsV.at(0)->phi(), passingMuonsV.at(0)->mass() );
      TLorentzVector l2 = TLorentzVector( 0., 0., 0., 0. );
      l2.SetPtEtaPhiM( passingMuonsV.at(1)->pt(), passingMuonsV.at(1)->eta(),
          passingMuonsV.at(1)->phi(), passingMuonsV.at(1)->mass() );
      m_vis = (l1 + l2).M();

      // Same sign comparison
      if (passingMuonsV.at(0)->charge() + passingMuonsV.at(1)->charge() == 0) SS = 0;
      else SS = 1;
  }



  if (passingElectronsV.size() == 2) {
      l1Pt = passingElectronsV.at(0)->pt();
      l1Eta = passingElectronsV.at(0)->eta();
      l1Phi = passingElectronsV.at(0)->phi();
      l1Iso = (passingElectronsV.at(0)->pfIsolationVariables().sumChargedHadronPt + TMath::Max(
          passingElectronsV.at(0)->pfIsolationVariables().sumNeutralHadronEt +
          passingElectronsV.at(0)->pfIsolationVariables().sumPhotonEt -
          0.5 * passingElectronsV.at(0)->pfIsolationVariables().sumPUPt, 0.0)) / passingElectronsV.at(0)->pt();
      l1LooseMuon = -9;
      l1MediumMuon = -9;
      l1ElecWP90 = passingElectronsV.at(0)->electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp90");
      l1ElecWP80 = passingElectronsV.at(0)->electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp80");
      l2Pt = passingElectronsV.at(1)->pt();
      l2Eta = passingElectronsV.at(1)->eta();
      l2Phi = passingElectronsV.at(1)->phi();
      l2Iso = (passingElectronsV.at(1)->pfIsolationVariables().sumChargedHadronPt + TMath::Max(
          passingElectronsV.at(1)->pfIsolationVariables().sumNeutralHadronEt +
          passingElectronsV.at(1)->pfIsolationVariables().sumPhotonEt -
          0.5 * passingElectronsV.at(1)->pfIsolationVariables().sumPUPt, 0.0)) / passingElectronsV.at(1)->pt();
      l2LooseMuon = -9;
      l2MediumMuon = -9;
      l2ElecWP90 = passingElectronsV.at(1)->electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp90");
      l2ElecWP80 = passingElectronsV.at(1)->electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp80");

      leptonDR_l11_l22 = deltaR( *passingElectronsV.at(0), *passingElectronsV.at(1));
      // Get Visible Mass
      TLorentzVector l1 = TLorentzVector( 0., 0., 0., 0. );
      l1.SetPtEtaPhiM( passingElectronsV.at(0)->pt(), passingElectronsV.at(0)->eta(),
          passingElectronsV.at(0)->phi(), passingElectronsV.at(0)->mass() );
      TLorentzVector l2 = TLorentzVector( 0., 0., 0., 0. );
      l2.SetPtEtaPhiM( passingElectronsV.at(1)->pt(), passingElectronsV.at(1)->eta(),
          passingElectronsV.at(1)->phi(), passingElectronsV.at(1)->mass() );
      m_vis = (l1 + l2).M();

      // Same sign comparison
      if (passingElectronsV.at(0)->charge() + passingElectronsV.at(1)->charge() == 0) SS = 0;
      else SS = 1;
  }




  edm::Handle<edm::TriggerResults> triggerResults;   
  iEvent.getByToken(triggerToken_, triggerResults);

  for (auto& pair : triggers) {
      (*pair.second) = 0;
  }

  std::vector<std::string> usedPaths;
  const edm::TriggerNames &names = iEvent.triggerNames(*triggerResults);
  // See https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2014#Trigger
  //std::cout << "Trigger Path Length: " << triggerResults->size() << std::endl;
  for (unsigned int i = 0, n = triggerResults->size(); i < n; ++i) {
      //std::cout << " --- " << names.triggerName(i) << std::endl;
      if (triggerResults->accept(i)) {
          for (auto& pair : triggers) {
              if (names.triggerName(i).find( pair.first ) != std::string::npos) {
                  (*pair.second) += 1;
                  usedPaths.push_back( names.triggerName(i));
                  if (verbose) std::cout << " --- fired: " << names.triggerName(i) << std::endl;
              }
          }
      }
  }

  // Make sure a trigger fired
  int numFired = 0;
  for (auto pair : triggers) {
      if ((*pair.second) > 0) numFired += 1;
  }
  if (numFired == 0) return;
  cutFlow->Fill(7., 1.);



  // Do trigger object matching
  // for the moment, just record the number
  // of times our 'best' objects match
  // this can be expanded later to indivual trigs if necessary
  edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
  iEvent.getByToken(triggerObjectsToken_, triggerObjects);

  // Clear previous run
  for (auto pair : l1MatchTriggers) (*pair.second) = 0;
  for (auto pair : l2MatchTriggers) (*pair.second) = 0;
  l1hltPt = -99;
  l2hltPt = -99;

  for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
      obj.unpackPathNames(names);
      std::vector<std::string> pathNamesLast = obj.pathNames(true);
      // pathNamesLast = vector of flags, if this object was used in the final 
      // filter of a succeeding HLT path resp. in a succeeding 
      // condition of a succeeding L1 algorithm
      for (unsigned h = 0, n = pathNamesLast.size(); h < n; ++h) {
          if (std::find( usedPaths.begin(), usedPaths.end(), pathNamesLast[h]) != usedPaths.end()) {
              if (verbose) std::cout << " ---  " << pathNamesLast[h] << std::endl;
              if (verbose) std::cout << "\tTrigger object:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << std::endl;
              if (passingMuonsV.size() == 2) {
                  float drMu1 = deltaR( *passingMuonsV.at(0), obj );
                  if (drMu1 < 0.3) {
                    l1hltPt = obj.pt();
                    if (verbose) std::cout << "\tmuon1 dR: " << drMu1 << std::endl;
                    for (auto pair : l1MatchTriggers) {
                        //std::cout << pair.first << " : " << pathNamesLast[h] << std::endl;
                        if ( pathNamesLast[h].find( std::string(pair.first)) != std::string::npos ) {
                            //std::cout << "\t\tmuon1 " << pathNamesLast[h] << std::endl;
                            (*pair.second) += 1;
                        }
                    }
                  }
                  float drMu2 = deltaR( *passingMuonsV.at(1), obj );
                  if (drMu2 < 0.3) {
                    l2hltPt = obj.pt();
                    if (verbose) std::cout << "\tmuon2 dR: " << drMu2 << std::endl;
                    for (auto pair : l2MatchTriggers) {
                        if ( pathNamesLast[h].find( std::string(pair.first)) != std::string::npos ) (*pair.second) += 1;
                    }
                  }
              }
              if (passingElectronsV.size() == 2) {
                  float drElec1 = deltaR( *passingElectronsV.at(0), obj );
                  if (drElec1 < 0.3) {
                    l1hltPt = obj.pt();
                    if (verbose) std::cout << "\tmuon1 dR: " << drElec1 << std::endl;
                    for (auto pair : l1MatchTriggers) {
                        //std::cout << pair.first << " : " << pathNamesLast[h] << std::endl;
                        if ( pathNamesLast[h].find( std::string(pair.first)) != std::string::npos ) {
                            //std::cout << "\t\tmuon1 " << pathNamesLast[h] << std::endl;
                            (*pair.second) += 1;
                        }
                    }
                  }
                  float drElec2 = deltaR( *passingElectronsV.at(1), obj );
                  if (drElec2 < 0.3) {
                    l2hltPt = obj.pt();
                    if (verbose) std::cout << "\tmuon2 dR: " << drElec2 << std::endl;
                    for (auto pair : l2MatchTriggers) {
                        if ( pathNamesLast[h].find( std::string(pair.first)) != std::string::npos ) (*pair.second) += 1;
                    }
                  }
              }
          }
      }
  }



  tree->Fill();


#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
DoubleLeptonTAP::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
DoubleLeptonTAP::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
DoubleLeptonTAP::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


//define this as a plug-in
DEFINE_FWK_MODULE(DoubleLeptonTAP);
