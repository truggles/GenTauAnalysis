// -*- C++ -*-
//
// Package:    THRAnalysis/TauHLTStudies
// Class:      TauHLTStudiesAnalyzer
// 
/**\class TauHLTStudiesAnalyzer TauHLTStudiesAnalyzer.cc THRAnalysis/TauHLTStudies/plugins/TauHLTStudiesAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tyler Henry Ruggles
//         Created:  Sun, 18 June 2017
//
//


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

class TauHLTStudiesAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit TauHLTStudiesAnalyzer(const edm::ParameterSet&);
      ~TauHLTStudiesAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      float getGenMatchNumber( reco::PFTauRef& tau,
        edm::Handle<std::vector<reco::GenJet>> genHTaus,
        edm::Handle<std::vector<reco::GenJet>> genETaus,
        edm::Handle<std::vector<reco::GenJet>> genMTaus,
        edm::Handle<std::vector<reco::GenParticle>> genParticles);
      float getL1TauMatch( reco::PFTauRef& tau,
        edm::Handle<BXVector<l1t::Tau>> l1Taus);

      // ----------member data ---------------------------
      bool isData;
      bool isRAW;
      bool doTauTau;
      bool verbose;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genHadronicTausToken_;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genElectronicTausToken_;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genMuonicTausToken_;
      edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;

      edm::EDGetTokenT<std::vector<reco::PFTau>> tauToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauDecayModeToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDVLToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDLToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDMToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDTToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDVTToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIDVVTToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbLToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbL03Token_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbMToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbM03Token_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbTToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauIsoCmbT03Token_;

      edm::EDGetTokenT<reco::PFTauDiscriminator> tauAntiEToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> tauAntiMuToken_;

      edm::EDGetTokenT<std::vector<reco::Muon>> muonToken_;
      //edm::EDGetTokenT<std::vector<reco::GsfElectron>> electronToken_;
      //edm::EDGetTokenT<std::vector<reco::Jet>> jetToken_;
      edm::EDGetTokenT<std::vector<reco::PFMET>> metToken_;
      edm::EDGetTokenT<std::vector<reco::Vertex>> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      //edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
      edm::EDGetTokenT<BXVector<l1t::Tau>> stage2TauToken_;
      edm::EDGetTokenT<std::vector<reco::GenParticle>> genToken_;
      // l1 extras
      //edm::EDGetTokenT<edm::TriggerResults> triggerToken_;

      TTree *tree;
      TH1D *nEvents;
      TH1D *cutFlow;
      double eventD;
      float run, lumi, nTruePU, nvtx, nvtxCleaned,
        mPt, mEta, mPhi,
        tPt, tEta, tPhi, tMVAIsoVLoose, tMVAIsoLoose, tMVAIsoMedium, 
        tMVAIsoTight, tMVAIsoVTight, tMVAIsoVVTight, m_vis, transMass, SS,
        tIsoCmbLoose, tIsoCmbLoose03, tIsoCmbMedium, tIsoCmbMedium03, tIsoCmbTight, tIsoCmbTight03,
        leptonDR_t1_t2, leptonDR_m_t1, leptonDR_m_t2,
        mTrigMatch, tTrigMatch, mL1Match, tL1Match,
        t1_gen_match,tDecayMode,
        t2Pt, t2Eta, t2Phi, t2MVAIsoVLoose, t2MVAIsoLoose, t2MVAIsoMedium, 
        t2MVAIsoTight, t2MVAIsoVTight, t2MVAIsoVVTight, t2_gen_match,t2DecayMode,
        t2IsoCmbLoose, t2IsoCmbLoose03, t2IsoCmbMedium, t2IsoCmbMedium03, t2IsoCmbTight, t2IsoCmbTight03,
        t2TrigMatch,t2L1Match;
      bool foundGenTau, foundGenMuon; 
      std::map<std::string, int*> triggers;
      std::map<std::string, int>::iterator triggerIterator;
      int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1;
      int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      int HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1;
      int HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      int HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1;
      int HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      int HLT_IsoMu20;
      int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1;
      int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1;
      int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr;
      int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1;
      int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1;
      int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1;
      int HLT_IsoMu24;
      int HLT_IsoMu27;
      int HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg;
      int HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg;
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
TauHLTStudiesAnalyzer::TauHLTStudiesAnalyzer(const edm::ParameterSet& iConfig) :
    isData(iConfig.getUntrackedParameter<bool>("isData", false)),
    isRAW(iConfig.getUntrackedParameter<bool>("isRAW", false)),
    doTauTau(iConfig.getUntrackedParameter<bool>("doTauTau", false)),
    verbose(iConfig.getUntrackedParameter<bool>("verbose", false)),
    genHadronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("hadronSrc"))),
    genElectronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("tauElectronSrc"))),
    genMuonicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("tauMuonSrc"))),
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc"))),

    tauToken_(consumes<std::vector<reco::PFTau>>(iConfig.getParameter<edm::InputTag>("tauSrc"))),
    tauDecayModeToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByDecayModeFindingOldDMs"))),
    tauIDVLToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByVLooseIsolationMVArun2v1DBoldDMwLT"))),
    tauIDLToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByLooseIsolationMVArun2v1DBoldDMwLT"))),
    tauIDMToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBoldDMwLT"))),
    tauIDTToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByTightIsolationMVArun2v1DBoldDMwLT"))),
    tauIDVTToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByVTightIsolationMVArun2v1DBoldDMwLT"))),
    tauIDVVTToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByVVTightIsolationMVArun2v1DBoldDMwLT"))),
    tauIsoCmbLToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits"))),
    tauIsoCmbL03Token_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3HitsdR03"))),
    tauIsoCmbMToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits"))),
    tauIsoCmbM03Token_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3HitsdR03"))),
    tauIsoCmbTToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits"))),
    tauIsoCmbT03Token_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3HitsdR03"))),

    tauAntiEToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByMVA6LooseElectronRejection"))),
    tauAntiMuToken_(consumes<reco::PFTauDiscriminator>(edm::InputTag("hpsPFTauDiscriminationByTightMuonRejection3"))),

    muonToken_(consumes<std::vector<reco::Muon>>(iConfig.getParameter<edm::InputTag>("muonSrc"))),
    //electronToken_(consumes<std::vector<reco::GsfElectron>>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
    //jetToken_(consumes<std::vector<reco::Jet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
    metToken_(consumes<std::vector<reco::PFMET>>(iConfig.getParameter<edm::InputTag>("metSrc"))),
    vertexToken_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("pvSrc"))),
    triggerToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerSrc"))),
    //triggerObjectsToken_(consumes<reco::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjectsSrc"))),
    stage2TauToken_(consumes<BXVector<l1t::Tau>>(iConfig.getParameter<edm::InputTag>("stage2TauSrc"))),
    genToken_(consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genSrc")))
{
   //now do what ever initialization is needed
   //usesResource("TFileService");
   edm::Service<TFileService> fs;

   triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v"]                   = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]           = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1_v"]                  = &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]          = &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1_v"]                   = &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]           = &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   triggers["HLT_IsoMu20_v"]                                                                = &HLT_IsoMu20;
   triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1_v"]                 = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"]  = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]          = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1_v"]                        = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1_v"]                = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"] = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]         = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_v"]                = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr;
   triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1_v"]                 = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1;
   triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"]  = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]          = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_v"]                                                         = &HLT_IsoMu24_eta2p1;
   triggers["HLT_IsoMu24_v"]                                                                = &HLT_IsoMu24;
   triggers["HLT_IsoMu27_v"]                                                                = &HLT_IsoMu27;
   triggers["HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                  = &HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                          = &HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                  = &HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                          = &HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg;

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
   tree->Branch("mPt",&mPt,"mPt/F");
   tree->Branch("mEta",&mEta,"mEta/F");
   tree->Branch("mPhi",&mPhi,"mPhi/F");
   tree->Branch("mTrigMatch",&mTrigMatch,"mTrigMatch/F");
   tree->Branch("mL1Match",&mL1Match,"mL1Match/F");
   tree->Branch("tPt",&tPt,"tPt/F");
   tree->Branch("tEta",&tEta,"tEta/F");
   tree->Branch("tPhi",&tPhi,"tPhi/F");
   tree->Branch("t1_gen_match",&t1_gen_match,"t1_gen_match/F");
   tree->Branch("tMVAIsoVLoose",&tMVAIsoVLoose,"tMVAIsoVLoose/F");
   tree->Branch("tMVAIsoLoose",&tMVAIsoLoose,"tMVAIsoLoose/F");
   tree->Branch("tMVAIsoMedium",&tMVAIsoMedium,"tMVAIsoMedium/F");
   tree->Branch("tMVAIsoTight",&tMVAIsoTight,"tMVAIsoTight/F");
   tree->Branch("tMVAIsoVTight",&tMVAIsoVTight,"tMVAIsoVTight/F");
   tree->Branch("tMVAIsoVVTight",&tMVAIsoVVTight,"tMVAIsoVVTight/F");
   tree->Branch("tIsoCmbLoose",&tIsoCmbLoose,"tIsoCmbLoose/F");
   tree->Branch("tIsoCmbLoose03",&tIsoCmbLoose03,"tIsoCmbLoose03/F");
   tree->Branch("tIsoCmbMedium",&tIsoCmbMedium,"tIsoCmbMedium/F");
   tree->Branch("tIsoCmbMedium03",&tIsoCmbMedium03,"tIsoCmbMedium03/F");
   tree->Branch("tIsoCmbTight",&tIsoCmbTight,"tIsoCmbTight/F");
   tree->Branch("tIsoCmbTight03",&tIsoCmbTight03,"tIsoCmbTight03/F");
   tree->Branch("tDecayMode",&tDecayMode,"tDecayMode/F");
   tree->Branch("tTrigMatch",&tTrigMatch,"tTrigMatch/F");
   tree->Branch("tL1Match",&tL1Match,"tL1Match/F");
   tree->Branch("t2Pt",&t2Pt,"t2Pt/F");
   tree->Branch("t2Eta",&t2Eta,"t2Eta/F");
   tree->Branch("t2Phi",&t2Phi,"t2Phi/F");
   tree->Branch("t2_gen_match",&t2_gen_match,"t2_gen_match/F");
   tree->Branch("t2MVAIsoVLoose",&t2MVAIsoVLoose,"t2MVAIsoVLoose/F");
   tree->Branch("t2MVAIsoLoose",&t2MVAIsoLoose,"t2MVAIsoLoose/F");
   tree->Branch("t2MVAIsoMedium",&t2MVAIsoMedium,"t2MVAIsoMedium/F");
   tree->Branch("t2MVAIsoTight",&t2MVAIsoTight,"t2MVAIsoTight/F");
   tree->Branch("t2MVAIsoVTight",&t2MVAIsoVTight,"t2MVAIsoVTight/F");
   tree->Branch("t2MVAIsoVVTight",&t2MVAIsoVVTight,"t2MVAIsoVVTight/F");
   tree->Branch("t2IsoCmbLoose",&t2IsoCmbLoose,"t2IsoCmbLoose/F");
   tree->Branch("t2IsoCmbLoose03",&t2IsoCmbLoose03,"t2IsoCmbLoose03/F");
   tree->Branch("t2IsoCmbMedium",&t2IsoCmbMedium,"t2IsoCmbMedium/F");
   tree->Branch("t2IsoCmbMedium03",&t2IsoCmbMedium03,"t2IsoCmbMedium03/F");
   tree->Branch("t2IsoCmbTight",&t2IsoCmbTight,"t2IsoCmbTight/F");
   tree->Branch("t2IsoCmbTight03",&t2IsoCmbTight03,"t2IsoCmbTight03/F");
   tree->Branch("t2DecayMode",&t2DecayMode,"t2DecayMode/F");
   tree->Branch("t2TrigMatch",&t2TrigMatch,"t2TrigMatch/F");
   tree->Branch("t2L1Match",&t2L1Match,"t2L1Match/F");
   tree->Branch("leptonDR_m_t1",&leptonDR_m_t1,"leptonDR_m_t1/F");
   tree->Branch("leptonDR_m_t2",&leptonDR_m_t2,"leptonDR_m_t2/F");
   tree->Branch("leptonDR_t1_t2",&leptonDR_t1_t2,"leptonDR_t1_t2/F");
   tree->Branch("m_vis_muon_tau1",&m_vis,"m_vis/F");
   tree->Branch("transMass",&transMass,"transMass/F");
   tree->Branch("SS_muon_tau1",&SS,"SS/F");

   tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",                   &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1,                  "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1",           &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1,          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1",                  &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1,                 "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1",          &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1,         "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1",                   &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1,                  "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1",           &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1,          "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   tree->Branch("HLT_IsoMu20",                                                                &HLT_IsoMu20,                                                               "HLT_IsoMu20/I");
   tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",                 &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1,                "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",  &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1, "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",          &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,         "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",                        &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1,                       "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",                &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1,               "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1", &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1,"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",         &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,        "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",                &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr,               "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr/I");
   tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",                 &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1,                "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",  &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1, "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",          &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,         "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1",                                                         &HLT_IsoMu24_eta2p1,                                                        "HLT_IsoMu24_eta2p1/I");
   tree->Branch("HLT_IsoMu24",                                                                &HLT_IsoMu24,                                                               "HLT_IsoMu24/I");
   tree->Branch("HLT_IsoMu27",                                                                &HLT_IsoMu27,                                                               "HLT_IsoMu27/I");
   tree->Branch("HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg",                           &HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg,                          "HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg",                           &HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg,                          "HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                  &HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                 "HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg",                          &HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg,                         "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                  &HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                 "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg",                          &HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg,                         "HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg",                           &HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg,                          "HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",                           &HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg,                          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg/I");

}


TauHLTStudiesAnalyzer::~TauHLTStudiesAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
TauHLTStudiesAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  // First thing, fill the nEvents
  nEvents->Fill(0.);

  eventD = iEvent.eventAuxiliary().event();
  lumi = iEvent.eventAuxiliary().luminosityBlock();
  run = iEvent.eventAuxiliary().run();
  if (verbose) printf("Run: %.0f    Evt: %.0f   Lumi: %.0f\n", run, eventD, lumi);


  if (!isRAW) {
    cutFlow->Fill(0., 1.);

    edm::Handle<std::vector<reco::Vertex>> vertices;   
    iEvent.getByToken(vertexToken_, vertices);
    if (vertices->empty()) return; // skip the event if no PV found
    const reco::Vertex &PV = vertices->front();
    if (PV.ndof() < 4) return; // bad vertex
    nvtx = vertices.product()->size();
    for (const reco::Vertex &vertex : *vertices)
        if (!vertex.isFake()) ++nvtxCleaned;

    // Get the number of true events
    // This is used later for pile up reweighting
    edm::Handle<std::vector<PileupSummaryInfo>> puInfo;   
    iEvent.getByToken(puToken_, puInfo);
    if (puInfo.isValid()) {
        if (puInfo->size() > 0) {
            nTruePU = puInfo->at(1).getTrueNumInteractions();
        }
    }

    cutFlow->Fill(1., 1.); // Good vertex


    // Grab our gen taus and other gen particles
    // Select events with 1 gen Tau and 1 gen Muon
    edm::Handle<std::vector<reco::GenJet>> genHTaus;   
    iEvent.getByToken(genHadronicTausToken_, genHTaus);
    edm::Handle<std::vector<reco::GenJet>> genETaus;   
    iEvent.getByToken(genElectronicTausToken_, genETaus);
    edm::Handle<std::vector<reco::GenJet>> genMTaus;   
    iEvent.getByToken(genMuonicTausToken_, genMTaus);
    edm::Handle<std::vector<reco::GenParticle>> genParticles; 
    iEvent.getByToken(genToken_, genParticles);
    foundGenTau = false;
    foundGenMuon = false; 
    int nGenMuon = 0;
    std::vector<reco::GenJet> genTauHV;
    if (!isData) {
        if (genParticles.isValid()) {
            if ( genParticles->size() > 0 ) {
                // See how many decent gen Muons we have
                for(size_t m = 0; m != genParticles->size(); ++m) {
                    reco::GenParticle genp = genParticles->at(m);
                    if (genp.pdgId() != 11 || genp.pt() < 15 || fabs(genp.eta()) > 2.1 || (!genp.statusFlags().isPrompt()))
                        continue;
                    ++nGenMuon;
                }
            }
            // Now see how many gen Hadronic Taus we have
            if ( genHTaus->size() > 0 ) {
                for (size_t j = 0; j != genHTaus->size(); ++j) {
                    if (fabs(genHTaus->at(j).eta()) > 2.1 || genHTaus->at(j).pt() < 20) continue;
                    // Save gen Tau H for comparison with AOD Taus later 
                    // This allwos us to remove isolation requirements later
                    genTauHV.push_back( genHTaus->at(j) );
                }
            }
        }
        if (verbose) std::cout << "nGenMuons: " << nGenMuon << "   nGenTauH: " << genTauHV.size() << std::endl;
        //FIXME if (nGenMuon != 1) return;
        cutFlow->Fill(2., 1.); // 1 gen muon
        //FIXME if (genTauHV.size() != 1) return;
        cutFlow->Fill(3., 1.); // 1 gen hadronic tau
    }




    edm::Handle<std::vector<reco::Muon>> muons; 
    iEvent.getByToken(muonToken_, muons);
    // Storage for the "best" muon
    reco::Muon bestMuon;
    int passingMuons = 0;

    for (const reco::Muon &mu : *muons) {
        //if (mu.pt() < 20 || fabs(mu.eta()) > 2.1 || !mu.isMediumMuon()) continue;
        if (mu.pt() < 20 || fabs(mu.eta()) > 2.1 || ( !mu.isGlobalMuon() || !mu.isTrackerMuon() ) ) continue;
        float mIso = (mu.pfIsolationR04().sumChargedHadronPt
            + TMath::Max(0., mu.pfIsolationR04().sumNeutralHadronEt
            + mu.pfIsolationR04().sumPhotonEt
            - 0.5*mu.pfIsolationR04().sumPUPt))
            /mu.pt();
        if (mIso > 0.1) continue;
        passingMuons++;
        bestMuon = mu;
    }
    // Require strictly 1 muon
    if (isData && !doTauTau)
        if (passingMuons == 0) return;
    if (doTauTau)
        if (passingMuons > 0) return;
    cutFlow->Fill(4., 1.);
    // Extra lepton veto (muons)
    if (isData)
        if (passingMuons > 1) return;
    cutFlow->Fill(5., 1.);


    //edm::Handle<std::vector<reco::GsfElectron>> electrons;   
    //iEvent.getByToken(electronToken_, electrons);
    //int passingElectrons = 0;
    //for (const reco::GsfElectron &el : *electrons) {
    //    if (el.pt() < 20 || fabs(el.eta()) > 2.1 || 
    //        el.electronID("mvaEleID-Spring15-25ns-nonTrig-V1-wp90") < 0.5) continue;
    //    float eIso = (el.pfIsolationVariables().sumChargedHadronPt + TMath::Max(
    //        el.pfIsolationVariables().sumNeutralHadronEt +
    //        el.pfIsolationVariables().sumPhotonEt -
    //        0.5 * el.pfIsolationVariables().sumPUPt, 0.0)) / el.pt();
    //    if (eIso > 0.1) continue;
    //    passingElectrons++;
    //}
    //// Extra lepton veto (electrons)
    //if (passingElectrons > 0) return;
    //cutFlow->Fill(4., 1.);


    edm::Handle<std::vector<reco::PFTau>> taus;
    if(!iEvent.getByToken(tauToken_, taus))
        std::cout << "Error no reco::PFTau" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauDM;
    if(!iEvent.getByToken(tauDecayModeToken_, tauDM))
        std::cout << "Error getting tau discriminator: DecayMode" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDVL;
    if(!iEvent.getByToken(tauIDVLToken_, tauIDVL))
        std::cout << "Error getting tau discriminator: IDVL" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDL;
    if(!iEvent.getByToken(tauIDLToken_, tauIDL))
        std::cout << "Error getting tau discriminator: IDL" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDM;
    if(!iEvent.getByToken(tauIDMToken_, tauIDM))
        std::cout << "Error getting tau discriminator: IDM" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDT;
    if(!iEvent.getByToken(tauIDTToken_, tauIDT))
        std::cout << "Error getting tau discriminator: IDT" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDVT;
    if(!iEvent.getByToken(tauIDVTToken_, tauIDVT))
        std::cout << "Error getting tau discriminator: IDVT" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIDVVT;
    if(!iEvent.getByToken(tauIDVVTToken_, tauIDVVT))
        std::cout << "Error getting tau discriminator: IDVT" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbL;
    if(!iEvent.getByToken(tauIsoCmbLToken_, tauIsoCmbL))
        std::cout << "Error getting tau discriminator: IsoCmbL" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbL03;
    if(!iEvent.getByToken(tauIsoCmbL03Token_, tauIsoCmbL03))
        std::cout << "Error getting tau discriminator: IsoCmbL03" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbM;
    if(!iEvent.getByToken(tauIsoCmbMToken_, tauIsoCmbM))
        std::cout << "Error getting tau discriminator: IsoCmbM" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbM03;
    if(!iEvent.getByToken(tauIsoCmbM03Token_, tauIsoCmbM03))
        std::cout << "Error getting tau discriminator: IsoCmbM03" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbT;
    if(!iEvent.getByToken(tauIsoCmbTToken_, tauIsoCmbT))
        std::cout << "Error getting tau discriminator: IsoCmbT" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauIsoCmbT03;
    if(!iEvent.getByToken(tauIsoCmbT03Token_, tauIsoCmbT03))
        std::cout << "Error getting tau discriminator: IsoCmbT03" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauAntiE;
    if(!iEvent.getByToken(tauAntiEToken_, tauAntiE))
        std::cout << "Error getting tau discriminator: AntiE" << std::endl;

    edm::Handle<reco::PFTauDiscriminator> tauAntiMu;
    if(!iEvent.getByToken(tauAntiMuToken_, tauAntiMu))
        std::cout << "Error getting tau discriminator: AntiMu" << std::endl;

    // Storage for the "best" muon
    std::vector<reco::PFTauRef> passingTausV;
    std::vector<reco::PFTauRef> passingGenMatchedTausV;

    // Inverting the ordering will leave us with the highest pt tau selected
    for (size_t iTau = 0; iTau != taus->size(); ++iTau) {

        reco::PFTauRef tauCandidate(taus, iTau);
        if (tauCandidate->pt() < 20 || fabs(tauCandidate->eta()) > 2.1) continue;
        passingTausV.push_back( tauCandidate );

        // Check if Tau is matched to gen Tau H
        // If gen matched, this is the 'bestTau'
        // Only check gen matching if isMC
        if (!isData) {
            for (auto gTau : genTauHV) {
                if (deltaR(gTau.p4(), tauCandidate->p4()) < 0.5) {
                    passingGenMatchedTausV.push_back( tauCandidate );
                    continue; // only fill once in case a tau matches 2 gen taus
                }
            }
        }
    }
    // Tau study so...
    if (passingTausV.size() == 0) return;
    cutFlow->Fill(6., 1.);
    if (verbose) std::cout << "Passing Muons: " << passingMuons << "   Passing Taus: " << passingTausV.size() << std::endl;
    if (verbose) std::cout << " --- From vector   Passing Taus: " << passingTausV.size() << " gen matched taus: " << passingGenMatchedTausV.size() << std::endl;

    // Pt order passing reco::taus
    std::sort(passingTausV.begin(), passingTausV.end(), [](reco::PFTauRef a, reco::PFTauRef b) {
        return a->pt() > b->pt();
    });

    //for (auto pTau : passingTausV) {
    //    std::cout << " ------ passed pt: " << pTau->pt() << std::endl;
    //}


    // Check for non-overlapping bjets
    // using Medium CISV value of 0.8
    //edm::Handle<std::vector<reco::Jet>> jets;   
    //iEvent.getByToken(jetToken_, jets);
    //bool btagged = false;
    //for (const reco::Jet &j : *jets) {
    //    if (j.pt() < 20 || fabs(j.eta()) > 2.4 || j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") < 0.8) continue;
    //    if (deltaR(j, bestMuon) > 0.5) continue;
    //    if (deltaR(j, passingTausV.at(0)) > 0.5) continue;
    //    btagged = true;
    //}
    //if (btagged) return;
    //cutFlow->Fill(6., 1.);


    // Save our best tau and muon variables
    mPt = bestMuon.pt();
    mEta = bestMuon.eta();
    mPhi = bestMuon.phi();
    
    tPt = passingTausV.at(0)->pt();
    tEta = passingTausV.at(0)->eta();
    tPhi = passingTausV.at(0)->phi();
    tMVAIsoVLoose = (*tauIDVL)[passingTausV.at(0)];
    tMVAIsoLoose  = (*tauIDL)[passingTausV.at(0)];
    tMVAIsoMedium = (*tauIDM)[passingTausV.at(0)];
    tMVAIsoTight  = (*tauIDT)[passingTausV.at(0)];
    tMVAIsoVTight = (*tauIDVT)[passingTausV.at(0)];
    tMVAIsoVVTight = (*tauIDVVT)[passingTausV.at(0)];
    tIsoCmbLoose = (*tauIsoCmbL)[passingTausV.at(0)];
    tIsoCmbLoose03 = (*tauIsoCmbL03)[passingTausV.at(0)];
    tIsoCmbMedium = (*tauIsoCmbM)[passingTausV.at(0)];
    tIsoCmbMedium03 = (*tauIsoCmbM03)[passingTausV.at(0)];
    tIsoCmbTight = (*tauIsoCmbT)[passingTausV.at(0)];
    tIsoCmbTight03 = (*tauIsoCmbT03)[passingTausV.at(0)];
    tDecayMode = (*tauDM)[passingTausV.at(0)];
    leptonDR_m_t1 = deltaR( bestMuon, *passingTausV.at(0) );

    // In data these tend to overlap, so just skip these events
    if (isData)
        if (leptonDR_m_t1 < 0.5) return;

    if (passingTausV.size() > 1) {
        t2Pt = passingTausV.at(1)->pt();
        t2Eta = passingTausV.at(1)->eta();
        t2Phi = passingTausV.at(1)->phi();
        t2MVAIsoVLoose = (*tauIDVL)[passingTausV.at(1)];
        t2MVAIsoLoose  = (*tauIDL)[passingTausV.at(1)];
        t2MVAIsoMedium = (*tauIDM)[passingTausV.at(1)];
        t2MVAIsoTight  = (*tauIDT)[passingTausV.at(1)];
        t2MVAIsoVTight = (*tauIDVT)[passingTausV.at(1)];
        t2MVAIsoVVTight = (*tauIDVVT)[passingTausV.at(1)];
        t2IsoCmbLoose = (*tauIsoCmbL)[passingTausV.at(0)];
        t2IsoCmbLoose03 = (*tauIsoCmbL03)[passingTausV.at(0)];
        t2IsoCmbMedium = (*tauIsoCmbM)[passingTausV.at(0)];
        t2IsoCmbMedium03 = (*tauIsoCmbM03)[passingTausV.at(0)];
        t2IsoCmbTight = (*tauIsoCmbT)[passingTausV.at(0)];
        t2IsoCmbTight03 = (*tauIsoCmbT03)[passingTausV.at(0)];
        t2DecayMode = (*tauDM)[passingTausV.at(1)];
        leptonDR_m_t2 = deltaR( bestMuon, *passingTausV.at(1) );
        leptonDR_t1_t2 = deltaR( *passingTausV.at(0), *passingTausV.at(1) );

        // If tau2 is overlapped, fill with -1
        if (leptonDR_m_t2 < 0.5) {
            t2Pt = -1;
            t2Eta = -1;
            t2Phi = -1;
            t2MVAIsoVLoose = -1;
            t2MVAIsoLoose  = -1;
            t2MVAIsoMedium = -1;
            t2MVAIsoTight  = -1;
            t2MVAIsoVTight = -1;
            t2MVAIsoVVTight = -1;
            t2IsoCmbLoose   = -1;
            t2IsoCmbLoose03 = -1;
            t2IsoCmbMedium  = -1;
            t2IsoCmbMedium03 = -1;
            t2IsoCmbTight   = -1;
            t2IsoCmbTight03 = -1;
            t2DecayMode = -1;
            leptonDR_m_t2 = -1;
            leptonDR_t1_t2 = -1;
        }
    }
    else {
        t2Pt = -1;
        t2Eta = -1;
        t2Phi = -1;
        t2MVAIsoVLoose = -1;
        t2MVAIsoLoose  = -1;
        t2MVAIsoMedium = -1;
        t2MVAIsoTight  = -1;
        t2MVAIsoVTight = -1;
        t2MVAIsoVVTight = -1;
        t2IsoCmbLoose   = -1;
        t2IsoCmbLoose03 = -1;
        t2IsoCmbMedium  = -1;
        t2IsoCmbMedium03 = -1;
        t2IsoCmbTight   = -1;
        t2IsoCmbTight03 = -1;
        t2DecayMode = -1;
        leptonDR_m_t2 = -1;
        leptonDR_t1_t2 = -1;
    }



    // Check for overlapping Gen Taus
    // with reconstructed gen taus of 3 types
    // and normal gen particles
    t1_gen_match = -1;
    t2_gen_match = -1;
    if (!isData) {

        t1_gen_match = getGenMatchNumber( passingTausV.at(0),
            genHTaus, genETaus, genMTaus, genParticles);

        if (passingTausV.size() > 1) {
            t2_gen_match = getGenMatchNumber( passingTausV.at(1),
                genHTaus, genETaus, genMTaus, genParticles);
        }
    }

    // Get MET for transverse mass calculation 
    edm::Handle<std::vector<reco::PFMET>> mets;   
    iEvent.getByToken(metToken_, mets);
    const reco::PFMET &met = mets->front();
    transMass = TMath::Sqrt( 2. * bestMuon.pt() * met.pt() * (1. - TMath::Cos( bestMuon.phi() - met.phi())));


    if (passingMuons > 0) {
        // Get Visible Mass
        TLorentzVector l1 = TLorentzVector( 0., 0., 0., 0. );
        l1.SetPtEtaPhiM( bestMuon.pt(), bestMuon.eta(),
            bestMuon.phi(), bestMuon.mass() );
        TLorentzVector l2 = TLorentzVector( 0., 0., 0., 0. );
        l2.SetPtEtaPhiM( passingTausV.at(0)->pt(), passingTausV.at(0)->eta(),
            passingTausV.at(0)->phi(), passingTausV.at(0)->mass() );
        m_vis = (l1 + l2).M();


        // Same sign comparison
        if (bestMuon.charge() + passingTausV.at(0)->charge() == 0) SS = 0;
        else SS = 1;
    }
    else {
        m_vis = -1;
        SS = -1;
    }


    edm::Handle<edm::TriggerResults> triggerResults;   
    iEvent.getByToken(triggerToken_, triggerResults);
    //edm::Handle<reco::TriggerObjectStandAloneCollection> triggerObjects;
    //iEvent.getByToken(triggerObjectsToken_, triggerObjects);

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


    // Do trigger object matching
    // for the moment, just record the number
    // of times our 'best' objects match
    // this can be expanded later to indivual trigs if necessary
    //mTrigMatch = 0;
    //tTrigMatch = 0;
    //for (reco::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
    //    obj.unpackPathNames(names);
    //    std::vector<std::string> pathNamesLast = obj.pathNames(true);
    //    // pathNamesLast = vector of flags, if this object was used in the final 
    //    // filter of a succeeding HLT path resp. in a succeeding 
    //    // condition of a succeeding L1 algorithm
    //    for (unsigned h = 0, n = pathNamesLast.size(); h < n; ++h) {
    //        if (std::find( usedPaths.begin(), usedPaths.end(), pathNamesLast[h]) != usedPaths.end()) {
    //            //std::cout << " ---  " << pathNamesLast[h] << std::endl;
    //            //std::cout << "\tTrigger object:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << std::endl;
    //            float drMu = deltaR( bestMuon, obj );
    //            float drTau = deltaR( passingTausV.at(0), obj );
    //            //std::cout << "\tbestMuon dR: " << drMu << std::endl;
    //            //std::cout << "\tpassingTausV.at(0) dR: " << drTau << std::endl;
    //            if (drMu < 0.5) ++mTrigMatch;
    //            if (drTau < 0.5) ++tTrigMatch;
    //        }
    //    }
    //}


    // Do l1extra object matching
    // Make sure to only consider l1 objects from the
    // intended BX.  That is the size(0) and
    // at(0,i) notation
    edm::Handle<BXVector<l1t::Tau>> l1Taus; 
    iEvent.getByToken(stage2TauToken_, l1Taus);
    
    tL1Match = getL1TauMatch( passingTausV.at(0), l1Taus);
    if (passingTausV.size() > 1) {
        t2L1Match = getL1TauMatch( passingTausV.at(1), l1Taus);
    }



    // Denominator section first, just check if there's the correct #
    // of the associated leptons
//    if (hTaus->size() >= 2) TauTauD = 1;
//    if (hTaus->size() >= 1) {
//        if(eTaus->size() >= 1) ETauD = 1;
//        if(mTaus->size() >= 1) MuTauD = 1;
//    }
//    if(eTaus->size() >= 1 && mTaus->size() >= 1) EMuD = 1;
//    if(mTaus->size() >= 2) MuMuD = 1;
//    
//    float nLeptons = 0;
//    nLeptons += hTaus->size() + eTaus->size() + mTaus->size();
//    if (nLeptons >= 3) threeLeptons = 1;
//    nLooseTaus = hTaus->size();
//    nLooseElec = eTaus->size();
//    nLooseMu = mTaus->size();
//
//
//    size_t ETau_e = 0;
//    size_t ETau_t = 0;
//    size_t MuTau_m = 0;
//    size_t MuTau_t = 0;
//    size_t EMu_e = 0;
//    size_t EMu_m = 0;
//    size_t TauTau_t1 = 0;
//    size_t TauTau_t2 = 0;
//    size_t MuMu_m1 = 0;
//    size_t MuMu_m2 = 0;
//
//    //uint32_t nHTaus = hTaus->size();
//    //if (hTaus->size() > 0)// std::cout << " --- N Hadronic Taus: "<<nHTaus<<std::endl;
//    //{
//    //const std::vector<reco::GenJet> nTaus_ = hTaus.product();
//    std::vector< float > pts;
//    for (const reco::GenJet &tau : *hTaus) {
//        pts.push_back( tau.pt() );
//        if ( TMath::Abs(tau.eta()) < 2.3 && tau.pt() > 20 ) {
//            MuTau_t += 1;
//            ETau_t += 1;}
//        if ( TMath::Abs(tau.eta()) < 2.1 && tau.pt() > 40 ) TauTau_t1 += 1;
//        if ( TMath::Abs(tau.eta()) < 2.1 && tau.pt() > 30 ) TauTau_t2 += 1;
//    }
//
//    if ( pts.size() > 0 ) tauPt1 = pts.at(0);
//    if ( pts.size() > 1 ) tauPt2 = pts.at(1);
//    if ( pts.size() > 2 ) tauPt3 = pts.at(2);
//
//    //}
//    //uint32_t nETaus = eTaus->size();
//    //if (nETaus > 0)// std::cout << " ### N Electronic Taus: "<<nETaus<<std::endl;
//    //{
//    for (const reco::GenJet &ele : *eTaus) {
//        if ( TMath::Abs(ele.eta()) < 2.5 && ele.pt() > 13 ) EMu_e += 1;
//        if ( TMath::Abs(ele.eta()) < 2.1 && ele.pt() > 24 ) ETau_e += 1;
//    //}
//    }
//    //uint32_t nMTaus = mTaus->size();
//    //if (nMTaus > 0)// std::cout << " *** N Muonic Taus: "<<nMTaus<<std::endl;
//    //{
//    for (const reco::GenJet &mu : *mTaus) {
//        if ( TMath::Abs(mu.eta()) < 2.4 && mu.pt() > 10 ) EMu_m += 1;
//        if ( TMath::Abs(mu.eta()) < 2.1 && mu.pt() > 19 ) MuTau_m += 1;
//        if ( TMath::Abs(mu.eta()) < 2.4 && mu.pt() > 20 ) MuMu_m1 += 1; // # of mu passing "leading" cut
//        if ( TMath::Abs(mu.eta()) < 2.4 && mu.pt() < 20 && mu.pt() > 10 ) MuMu_m2 += 1; // # of mu passing only "trailing" cut
//    }
//    //}
//    
//    // Check if we have matches
//    if (ETau_e > 0 && ETau_t > 0) ETauPass = 1;
//    if (MuTau_m > 0 && MuTau_t > 0) MuTauPass = 1;
//    if (EMu_e > 0 && EMu_m > 0) EMuPass = 1;
//    if (TauTau_t1 > 1) TauTauPass = 1;
//    if (TauTau_t1 == 1 && TauTau_t2 > 0) TauTau4030Pass = 1;
//    if (MuMu_m1 > 1) MuMuPass = 1;
//    if (MuMu_m1 > 0 && MuMu_m2 > 0) MuMuPass = 1;
//    
//
//    if (invmass.size() == 2) {
//        //std::cout << "Len InvMass: "<<invmass.size()<<std::endl;
//        TLorentzVector diLep = invmass[0];
//        diLep += invmass[1];
//        //std::cout << "m(ll) " << diLep.M() << std::endl;
//        genMass = diLep.M();
//
//    }
    
 
  } // is not RAW

  // Currently Data is in RAW form
  // all it has is
  // edm::TriggerResults       "TriggerResults"         ""        "HLT"
  if (isRAW) { // isRAW (only trigger results abailable)
    edm::Handle<edm::TriggerResults> triggerResults;   
    iEvent.getByToken(triggerToken_, triggerResults);
    //edm::Handle<reco::TriggerObjectStandAloneCollection> triggerObjects;
    //iEvent.getByToken(triggerObjectsToken_, triggerObjects);

    for (auto& pair : triggers) {
        (*pair.second) = 0;
    }

    //std::vector<std::string> usedPaths;
    const edm::TriggerNames &names = iEvent.triggerNames(*triggerResults);
    // See https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2014#Trigger
    //std::cout << "Trigger Path Length: " << triggerResults->size() << std::endl;
    for (unsigned int i = 0, n = triggerResults->size(); i < n; ++i) {
        //std::cout << " --- " << names.triggerName(i) << std::endl;
        if (triggerResults->accept(i)) {
            for (auto& pair : triggers) {
                if (names.triggerName(i).find( pair.first ) != std::string::npos) {
                    (*pair.second) += 1;
                    //usedPaths.push_back( names.triggerName(i));
                    if (verbose) std::cout << " --- fired: " << names.triggerName(i) << std::endl;
                }
            }
        }
    }
  } // end is RAW
    

    //LogInfo("Demo") << "number of gen taus "<<nGenTaus;
    //std::cout << genTaus << std::endl;

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
TauHLTStudiesAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TauHLTStudiesAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
TauHLTStudiesAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ for retrieving the gen_match variable used in HTT ------------------
float
TauHLTStudiesAnalyzer::getGenMatchNumber( reco::PFTauRef& tau,
        edm::Handle<std::vector<reco::GenJet>> genHTaus,
        edm::Handle<std::vector<reco::GenJet>> genETaus,
        edm::Handle<std::vector<reco::GenJet>> genMTaus,
        edm::Handle<std::vector<reco::GenParticle>> genParticles) {

  // Find the closest gen particle to our candidate
  float gen_match = -1;
  if ( genParticles->size() > 0 ) {
      reco::GenParticle closest = genParticles->at(0);
      float closestDR = 999;
      // The first two codes are based off of matching to true electrons/muons
      // Find the closest gen particle...
      for(size_t m = 0; m != genParticles->size(); ++m) {
          reco::GenParticle genp = genParticles->at(m);
          float tmpDR = deltaR( tau->p4(), genp.p4() );
          if ( tmpDR < closestDR ) { closest = genp; closestDR = tmpDR; }
      }
      float genID = abs(closest.pdgId());

      // Loop over all versions of gen taus and find closest one
      float closestDR_HTau = 999;
      float closestDR_ETau = 999;
      float closestDR_MTau = 999;
      if ( genHTaus->size() > 0 ) {
          for (size_t j = 0; j != genHTaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genHTaus->at(j).p4() );
              if (tmpDR < closestDR_HTau) closestDR_HTau = tmpDR;
          }
      }
      if ( genETaus->size() > 0 ) {
          for (size_t j = 0; j != genETaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genETaus->at(j).p4() );
              if (tmpDR < closestDR_ETau) closestDR_ETau = tmpDR;
          }
      }
      if ( genMTaus->size() > 0 ) {
          for (size_t j = 0; j != genMTaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genMTaus->at(j).p4() );
              if (tmpDR < closestDR_MTau) closestDR_MTau = tmpDR;
          }
      }

      // Now return the value based on which object is closer, the closest
      // single gen particle, or the rebuild gen taus
      // The first two codes are based off of matching to true electrons/muons
      float closestGetTau = TMath::Min(closestDR_ETau, closestDR_MTau);
      if (closestDR_HTau < closestGetTau) closestGetTau = closestDR_HTau;

      // Make sure we don't overwrite a proper value
      if (closestDR < closestGetTau && genID == 11 && closest.pt() > 8
              && closest.statusFlags().isPrompt() && closestDR < 0.2 )
                  gen_match = 1.0;
      else if (closestDR < closestGetTau && genID == 13 && closest.pt() > 8
              && closest.statusFlags().isPrompt() && closestDR < 0.2 )
                  gen_match = 2.0;
      // Other codes based off of not matching previous 2 options
      // as closest gen particle, retruns based on closest rebuilt gen tau
      else if (closestDR_ETau < 0.2 && closestDR_ETau < TMath::Min(closestDR_MTau, 
              closestDR_HTau)) gen_match = 3.0;
      else if (closestDR_MTau < 0.2 && closestDR_MTau < TMath::Min(closestDR_ETau, 
              closestDR_HTau)) gen_match = 4.0;
      else if (closestDR_HTau < 0.2 && closestDR_HTau < TMath::Min(closestDR_ETau, 
              closestDR_MTau)) gen_match = 5.0;
      else gen_match = 6.0; // No match, return 6 for "fake tau"
  }
  return gen_match;
}

float
TauHLTStudiesAnalyzer::getL1TauMatch( reco::PFTauRef& tau,
        edm::Handle<BXVector<l1t::Tau>> l1Taus) {
    float tL1Match = -1;
    if (l1Taus.isValid()) {
        tL1Match = 0;
        //std::cout << "L1 Extras is valid" << std::endl;
        for (size_t i = 0; i < l1Taus->size(0); ++i) {
            const l1t::Tau &l1Tau = l1Taus->at(0,i);
            // skip l1Tau if it's low pt b/c the trigger we want
            // actual results for is seeded by
            // L1_DoubleIsoTau28
            if (l1Tau.hwIso()<1 || l1Tau.pt()<27.5) continue; // hardware Iso bit
            float drTau = deltaR( *tau, l1Tau );
            //std::cout << " - " << i << " L1Tau pt: " << l1Tau.pt() 
            //<< " Iso: " << l1Tau.hwIso() << " dr: " << drTau << std::endl;
            if (drTau < 0.5) ++tL1Match;
        }    
    } // end l1Taus
    return tL1Match;

}

//define this as a plug-in
DEFINE_FWK_MODULE(TauHLTStudiesAnalyzer);
