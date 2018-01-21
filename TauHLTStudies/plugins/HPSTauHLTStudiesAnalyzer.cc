// -*- C++ -*-
//
// Package:    THRAnalysis/TauHLTStudies
// Class:      HPSTauHLTStudiesAnalyzer
// 
/**\class HPSTauHLTStudiesAnalyzer HPSTauHLTStudiesAnalyzer.cc THRAnalysis/TauHLTStudies/plugins/HPSTauHLTStudiesAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tyler Henry Ruggles
//         Created:  Mon, 21 November 2017
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

class HPSTauHLTStudiesAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit HPSTauHLTStudiesAnalyzer(const edm::ParameterSet&);
      ~HPSTauHLTStudiesAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      void getGenMatchNumber( 
        float &gen_match,
        float &gen_pt,
        pat::TauRef& tau,
        edm::Handle<std::vector<reco::GenJet>> genHTaus,
        edm::Handle<std::vector<reco::GenJet>> genETaus,
        edm::Handle<std::vector<reco::GenJet>> genMTaus,
        edm::Handle<std::vector<reco::GenParticle>> genParticles);
      void getL1TauMatch( pat::TauRef& tau,
        edm::Handle<BXVector<l1t::Tau>> l1Taus, float& l1TauMatch, float& l1TauPt, float& l1TauIso );

      // ----------member data ---------------------------
      bool isData;
      bool isRAW;
      bool doTauTau;
      bool requireMediumTauMVA;
      bool verbose;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genHadronicTausToken_;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genElectronicTausToken_;
      edm::EDGetTokenT<std::vector<reco::GenJet>> genMuonicTausToken_;
      edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;

      edm::EDGetTokenT<std::vector<pat::Tau>> slimmedTauToken_;
      edm::EDGetTokenT<std::vector<reco::PFTau>> hpsTauToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> hpsTauDecayModeToken_;
      edm::EDGetTokenT<std::vector<reco::PFTau>> defaultTauToken_;
      edm::EDGetTokenT<reco::PFTauDiscriminator> defaultTauDecayModeToken_;

      edm::EDGetTokenT<std::vector<pat::Muon>> muonToken_;
      edm::EDGetTokenT<edm::View<reco::GsfElectron> > electronToken_;
      edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
      edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
      edm::EDGetTokenT<std::vector<reco::Vertex>> vertexToken_;
      edm::EDGetTokenT<edm::TriggerResults> triggerToken_;
      edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
      edm::EDGetTokenT<BXVector<l1t::Tau>> stage2TauToken_;
      edm::EDGetTokenT<std::vector<reco::GenParticle>> genToken_;

      edm::EDGetTokenT<edm::ValueMap<bool> > eleLooseIdMapTag_;


      // l1 extras
      //edm::EDGetTokenT<edm::TriggerResults> triggerToken_;

      TTree *tree;
      TH1D *nEvents;
      TH1D *cutFlow;
      double event;
      float run, lumi, nTruePU, nvtx, nvtxCleaned, passingTaus, passingMuons, nVetoMuons, nSlimmedMuons,
        mPt, mEta, mPhi, mIso,
        tmpPt, tmpEta, tmpPhi, tmpIso,
        l1TauPt, l1TauIso,
        tPt, tEta, tPhi, tMVAIsoVLoose, tMVAIsoLoose, tMVAIsoMedium, 
        tMVAIsoTight, tMVAIsoVTight, tMVAIsoVVTight, m_vis, transMass, SS, isOS, pfMet,
        nBTag, nBTagAll, passingElectrons,
        //tIsoCmbLoose, tIsoCmbLoose03, tIsoCmbMedium, tIsoCmbMedium03, tIsoCmbTight, tIsoCmbTight03,
        tIsoCmbLoose, tIsoCmbMedium, tIsoCmbTight,
        leptonDR_t1_t2, leptonDR_m_t1, leptonDR_m_t2,
        mTrigMatch, tTrigMatch, mL1Match, tL1Match,
        t1_gen_match,genTauPt,tDecayMode, tDMFinding,
        t2Pt, t2Eta, t2Phi, t2MVAIsoVLoose, t2MVAIsoLoose, t2MVAIsoMedium, 
        t2MVAIsoTight, t2MVAIsoVTight, t2MVAIsoVVTight, t2_gen_match,t2DecayMode,
        //t2IsoCmbLoose, t2IsoCmbLoose03, t2IsoCmbMedium, t2IsoCmbMedium03, t2IsoCmbTight, t2IsoCmbTight03,
        t2IsoCmbLoose, t2IsoCmbMedium, t2IsoCmbTight,
        t2TrigMatch,t2genPt,t2L1Match, emptyVertices, failNdof,
        hpsTauSize, hpsTauPt, hpsTauEta, hpsTauPhi, hpsTauDM, hpsTauDMFinding, hpsTauDR,
        hpsTau2Pt, hpsTau2Eta, hpsTau2Phi, hpsTau2DM,
        defaultTauSize, defaultTauPt, defaultTauEta, defaultTauPhi, defaultTauDM, defaultTauDMFinding, defaultTauDR,
        defaultTau2Pt, defaultTau2Eta, defaultTau2Phi, defaultTau2DM;
      bool foundGenTau, foundGenMuon; 
      std::map<std::string, int*> triggers;
      std::map<std::string, int>::iterator triggerIterator;
      int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1;
      int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM;
      int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1;
      //int HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      //int HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1;
      //int HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      //int HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1;
      //int HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1;
      int HLT_IsoMu20;
      //int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1;
      //int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1;
      //int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1;
      //int HLT_IsoMu24_eta2p1;
      int HLT_IsoMu24;
      //int HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1;
      //int HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1;
      //int HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1;
      int HLT_IsoMu27;
      //int HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      //int HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg;
      //int HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      //int HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg;
      //int HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg;
      //int HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg;
      //int HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg;
      //int HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg;
      int HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg;
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
HPSTauHLTStudiesAnalyzer::HPSTauHLTStudiesAnalyzer(const edm::ParameterSet& iConfig) :
    isData(iConfig.getUntrackedParameter<bool>("isData", false)),
    isRAW(iConfig.getUntrackedParameter<bool>("isRAW", false)),
    doTauTau(iConfig.getUntrackedParameter<bool>("doTauTau", false)),
    requireMediumTauMVA(iConfig.getUntrackedParameter<bool>("requireMediumTauMVA", false)),
    verbose(iConfig.getUntrackedParameter<bool>("verbose", false)),
    genHadronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("hadronSrc"))),
    genElectronicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("tauElectronSrc"))),
    genMuonicTausToken_(consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("tauMuonSrc"))),
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc"))),

    slimmedTauToken_(consumes<std::vector<pat::Tau>>(iConfig.getParameter<edm::InputTag>("slimmedTauSrc"))),
    hpsTauToken_(consumes<std::vector<reco::PFTau>>(iConfig.getParameter<edm::InputTag>("hpsTauSrc"))),
    hpsTauDecayModeToken_(consumes<reco::PFTauDiscriminator>(iConfig.getParameter<edm::InputTag>("hpsTauDM"))),
    defaultTauToken_(consumes<std::vector<reco::PFTau>>(iConfig.getParameter<edm::InputTag>("defaultTauSrc"))),
    defaultTauDecayModeToken_(consumes<reco::PFTauDiscriminator>(iConfig.getParameter<edm::InputTag>("defaultTauDM"))),

    muonToken_(consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muonSrc"))),
    electronToken_(consumes<edm::View<reco::GsfElectron>>(iConfig.getParameter<edm::InputTag>("electronSrc"))),
    jetToken_(consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
    metToken_(consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metSrc"))),
    vertexToken_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("pvSrc"))),
    triggerToken_(consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("triggerSrc"))),
    triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjectsSrc"))),
    stage2TauToken_(consumes<BXVector<l1t::Tau>>(iConfig.getParameter<edm::InputTag>("stage2TauSrc"))),
    genToken_(consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genSrc"))),
    eleLooseIdMapTag_(consumes<edm::ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("eleLooseIdMap")))
{
   //now do what ever initialization is needed
   //usesResource("TFileService");
   edm::Service<TFileService> fs;

   triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v"]                   = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1;
   triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM_v"]                   = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM;
   triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v"]                = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1;
   //triggers["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]           = &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   //triggers["HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1_v"]                  = &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1;
   //triggers["HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]          = &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   //triggers["HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1_v"]                   = &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1;
   //triggers["HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1_v"]           = &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1;
   triggers["HLT_IsoMu20_v"]                                                                = &HLT_IsoMu20;
   //triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1_v"]                 = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"]  = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]          = &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1_v"]                        = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1_v"]                = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"] = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]         = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v"]         = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1_v"] = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1_v"]         = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_v"]                = &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1_v"]                 = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1_v"]  = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1_v"]          = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1_v"]  = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1_v"]          = &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1;
   //triggers["HLT_IsoMu24_eta2p1_v"]                                                         = &HLT_IsoMu24_eta2p1;
   triggers["HLT_IsoMu24_v"]                                                                = &HLT_IsoMu24;
   //triggers["HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1;
   //triggers["HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1_v"]                        = &HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1;
   //triggers["HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1_v"]                         = &HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1;
   triggers["HLT_IsoMu27_v"]                                                                = &HLT_IsoMu27;
   //triggers["HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   //triggers["HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg;
   //triggers["HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   //triggers["HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg;
   //triggers["HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                  = &HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                          = &HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v"]                          = &HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                  = &HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v"]                  = &HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg;
   //triggers["HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                          = &HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg;
   //triggers["HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg;
   //triggers["HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v"]                   = &HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg;
   triggers["HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v"]                           = &HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg;

   TFileDirectory subDir = fs->mkdir( "tagAndProbe" );
   nEvents = subDir.make<TH1D>("nEvents","nEvents",1,-0.5,0.5);
   cutFlow = subDir.make<TH1D>("cutFlow","cutFlow",10,-0.5,9.5);
   tree = subDir.make<TTree>("Ntuple","My T-A-P Ntuple");
   tree->Branch("RunNumber",&run,"RunNumber/F");
   tree->Branch("lumi",&lumi,"lumi/F");
   tree->Branch("EventNumber",&event,"EventNumber/D");
   tree->Branch("nTruePU",&nTruePU,"nTruePU/F");
   tree->Branch("nvtx",&nvtx,"nvtx/F");
   tree->Branch("nvtxCleaned",&nvtxCleaned,"nvtxCleaned/F");
   tree->Branch("passingTaus",&passingTaus,"passingTaus/F");
   tree->Branch("passingMuons",&passingMuons,"passingMuons/F");
   tree->Branch("nVetoMuons",&nVetoMuons,"nVetoMuons/F");
   tree->Branch("nSlimmedMuons",&nSlimmedMuons,"nSlimmedMuons/F");
   tree->Branch("passingElectrons",&passingElectrons,"passingElectrons/F");
   tree->Branch("muonPt",&mPt,"muonPt/F");
   tree->Branch("muonEta",&mEta,"muonEta/F");
   tree->Branch("muonPhi",&mPhi,"muonPhi/F");
   tree->Branch("muonIso",&mIso,"muonIso/F");
   tree->Branch("tmpMuonPt",&tmpPt,"tmpMuonPt/F");
   tree->Branch("tmpMuonEta",&tmpEta,"tmpMuonEta/F");
   tree->Branch("tmpMuonPhi",&tmpPhi,"tmpMuonPhi/F");
   tree->Branch("tmpMuonIso",&tmpIso,"tmpMuonIso/F");
   tree->Branch("mTrigMatch",&mTrigMatch,"mTrigMatch/F");
   tree->Branch("mL1Match",&mL1Match,"mL1Match/F");
   tree->Branch("tauPt",&tPt,"tauPt/F");
   tree->Branch("tauEta",&tEta,"tauEta/F");
   tree->Branch("tauPhi",&tPhi,"tauPhi/F");
   tree->Branch("l1TauPt",&l1TauPt,"l1TauPt/F");
   tree->Branch("l1TauIso",&l1TauIso,"l1TauIso/F");
   tree->Branch("tL1Match",&tL1Match,"tL1Match/F");
   tree->Branch("t1_gen_match",&t1_gen_match,"t1_gen_match/F");
   tree->Branch("genTauPt",&genTauPt,"genTauPt/F");
   tree->Branch("tMVAIsoVLoose",&tMVAIsoVLoose,"tMVAIsoVLoose/F");
   tree->Branch("tMVAIsoLoose",&tMVAIsoLoose,"tMVAIsoLoose/F");
   tree->Branch("tMVAIsoMedium",&tMVAIsoMedium,"tMVAIsoMedium/F");
   tree->Branch("tMVAIsoTight",&tMVAIsoTight,"tMVAIsoTight/F");
   tree->Branch("tMVAIsoVTight",&tMVAIsoVTight,"tMVAIsoVTight/F");
   tree->Branch("tMVAIsoVVTight",&tMVAIsoVVTight,"tMVAIsoVVTight/F");
   tree->Branch("tIsoCmbLoose",&tIsoCmbLoose,"tIsoCmbLoose/F");
   //tree->Branch("tIsoCmbLoose03",&tIsoCmbLoose03,"tIsoCmbLoose03/F");
   tree->Branch("tIsoCmbMedium",&tIsoCmbMedium,"tIsoCmbMedium/F");
   //tree->Branch("tIsoCmbMedium03",&tIsoCmbMedium03,"tIsoCmbMedium03/F");
   tree->Branch("tIsoCmbTight",&tIsoCmbTight,"tIsoCmbTight/F");
   //tree->Branch("tIsoCmbTight03",&tIsoCmbTight03,"tIsoCmbTight03/F");
   tree->Branch("tauDM",&tDecayMode,"tauDM/F");
   tree->Branch("tauDMFinding",&tDMFinding,"tauDMFinding/F");
   tree->Branch("tTrigMatch",&tTrigMatch,"tTrigMatch/F");
   tree->Branch("hpsTauSize",&hpsTauSize,"hpsTauSize/F");
   tree->Branch("hpsTauPt",&hpsTauPt,"hpsTauPt/F");
   tree->Branch("hpsTauEta",&hpsTauEta,"hpsTauEta/F");
   tree->Branch("hpsTauPhi",&hpsTauPhi,"hpsTauPhi/F");
   tree->Branch("hpsTauDM",&hpsTauDM,"hpsTauDM/F");
   tree->Branch("hpsTauDMFinding",&hpsTauDMFinding,"hpsTauDMFinding/F");
   tree->Branch("hpsTauDR",&hpsTauDR,"hpsTauDR/F");
   tree->Branch("hpsTau2Pt",&hpsTau2Pt,"hpsTau2Pt/F");
   tree->Branch("hpsTau2Eta",&hpsTau2Eta,"hpsTau2Eta/F");
   tree->Branch("hpsTau2Phi",&hpsTau2Phi,"hpsTau2Phi/F");
   tree->Branch("hpsTau2DM",&hpsTau2DM,"hpsTau2DM/F");
   tree->Branch("defaultTauSize",&defaultTauSize,"defaultTauSize/F");
   tree->Branch("defaultTauPt",&defaultTauPt,"defaultTauPt/F");
   tree->Branch("defaultTauEta",&defaultTauEta,"defaultTauEta/F");
   tree->Branch("defaultTauPhi",&defaultTauPhi,"defaultTauPhi/F");
   tree->Branch("defaultTauDM",&defaultTauDM,"defaultTauDM/F");
   tree->Branch("defaultTauDMFinding",&defaultTauDMFinding,"defaultTauDMFinding/F");
   tree->Branch("defaultTauDR",&defaultTauDR,"defaultTauDR/F");
   tree->Branch("defaultTau2Pt",&defaultTau2Pt,"defaultTau2Pt/F");
   tree->Branch("defaultTau2Eta",&defaultTau2Eta,"defaultTau2Eta/F");
   tree->Branch("defaultTau2Phi",&defaultTau2Phi,"defaultTau2Phi/F");
   tree->Branch("defaultTau2DM",&defaultTau2DM,"defaultTau2DM/F");
   tree->Branch("t2Pt",&t2Pt,"t2Pt/F");
   tree->Branch("t2Eta",&t2Eta,"t2Eta/F");
   tree->Branch("t2Phi",&t2Phi,"t2Phi/F");
   tree->Branch("t2_gen_match",&t2_gen_match,"t2_gen_match/F");
   tree->Branch("t2genPt",&t2genPt,"t2genPt/F");
   tree->Branch("t2MVAIsoVLoose",&t2MVAIsoVLoose,"t2MVAIsoVLoose/F");
   tree->Branch("t2MVAIsoLoose",&t2MVAIsoLoose,"t2MVAIsoLoose/F");
   tree->Branch("t2MVAIsoMedium",&t2MVAIsoMedium,"t2MVAIsoMedium/F");
   tree->Branch("t2MVAIsoTight",&t2MVAIsoTight,"t2MVAIsoTight/F");
   tree->Branch("t2MVAIsoVTight",&t2MVAIsoVTight,"t2MVAIsoVTight/F");
   tree->Branch("t2MVAIsoVVTight",&t2MVAIsoVVTight,"t2MVAIsoVVTight/F");
   tree->Branch("t2IsoCmbLoose",&t2IsoCmbLoose,"t2IsoCmbLoose/F");
   //tree->Branch("t2IsoCmbLoose03",&t2IsoCmbLoose03,"t2IsoCmbLoose03/F");
   tree->Branch("t2IsoCmbMedium",&t2IsoCmbMedium,"t2IsoCmbMedium/F");
   //tree->Branch("t2IsoCmbMedium03",&t2IsoCmbMedium03,"t2IsoCmbMedium03/F");
   tree->Branch("t2IsoCmbTight",&t2IsoCmbTight,"t2IsoCmbTight/F");
   //tree->Branch("t2IsoCmbTight03",&t2IsoCmbTight03,"t2IsoCmbTight03/F");
   tree->Branch("t2DecayMode",&t2DecayMode,"t2DecayMode/F");
   tree->Branch("t2TrigMatch",&t2TrigMatch,"t2TrigMatch/F");
   tree->Branch("t2L1Match",&t2L1Match,"t2L1Match/F");
   tree->Branch("leptonDR_m_t1",&leptonDR_m_t1,"leptonDR_m_t1/F");
   tree->Branch("leptonDR_m_t2",&leptonDR_m_t2,"leptonDR_m_t2/F");
   tree->Branch("leptonDR_t1_t2",&leptonDR_t1_t2,"leptonDR_t1_t2/F");
   tree->Branch("m_vis",&m_vis,"m_vis/F");
   tree->Branch("transMass",&transMass,"transMass/F");
   tree->Branch("pfMet",&pfMet,"pfMet/F");
   tree->Branch("SS",&SS,"SS/F");
   tree->Branch("isOS",&isOS,"isOS/F");
   tree->Branch("nBTag",&nBTag,"nBTag/F");
   tree->Branch("nBTagAll",&nBTagAll,"nBTagAll/F");
   tree->Branch("emptyVertices",&emptyVertices,"emptyVertices/F");
   tree->Branch("failNdof",&failNdof,"failNdof/F");

   tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",                   &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1,                  "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1/I");
   tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM",                   &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM,                  "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_withNewDM/I");
   tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",                   &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1,                  "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1/I");
   //tree->Branch("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1",           &HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1,          "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   //tree->Branch("HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1",                  &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1,                 "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1/I");
   //tree->Branch("HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1",          &HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1,         "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   //tree->Branch("HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1",                   &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1,                  "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1/I");
   //tree->Branch("HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1",           &HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1,          "HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_TightID_CrossL1/I");
   tree->Branch("HLT_IsoMu20",                                                                &HLT_IsoMu20,                                                               "HLT_IsoMu20/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1",                 &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1,                "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",  &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1, "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",          &HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,         "HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1",                        &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1,                       "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1",                &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1,               "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1", &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1,"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",         &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,        "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1",         &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1,        "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1", &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1,"HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1",         &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1,        "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr",                &HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr,               "HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1",                 &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1,                "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1",  &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1, "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1",          &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1,         "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau35_Trk1_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1",  &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1, "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1",          &HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1,         "HLT_IsoMu24_eta2p1_TightChargedIsoPFTau40_Trk1_eta2p1_Reg_CrossL1/I");
   //tree->Branch("HLT_IsoMu24_eta2p1",                                                         &HLT_IsoMu24_eta2p1,                                                        "HLT_IsoMu24_eta2p1/I");
   tree->Branch("HLT_IsoMu24",                                                                &HLT_IsoMu24,                                                               "HLT_IsoMu24/I");
   //tree->Branch("HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu27_eta2p1_LooseChargedIsoPFTau20_SingleL1/I");
   //tree->Branch("HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1",                        &HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1,                       "HLT_IsoMu27_eta2p1_MediumChargedIsoPFTau20_SingleL1/I");
   //tree->Branch("HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1",                         &HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1,                        "HLT_IsoMu27_eta2p1_TightChargedIsoPFTau20_SingleL1/I");
   tree->Branch("HLT_IsoMu27",                                                                &HLT_IsoMu27,                                                               "HLT_IsoMu27/I");
   //tree->Branch("HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleLooseChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg",                           &HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg,                          "HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleLooseChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg",                           &HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg,                          "HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                  &HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                 "HLT_DoubleMediumChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg",                          &HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg,                         "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",                          &HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg,                         "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                  &HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                 "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg",                  &HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg,                 "HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg",                          &HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg,                         "HLT_DoubleMediumChargedIsoPFTau40_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg",                           &HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg,                          "HLT_DoubleTightChargedIsoPFTau35_Trk1_eta2p1_Reg/I");
   //tree->Branch("HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",                   &HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg,                  "HLT_DoubleTightChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",                           &HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg,                          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg/I");
   tree->Branch("HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg",                           &HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg,                          "HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg/I");

}


HPSTauHLTStudiesAnalyzer::~HPSTauHLTStudiesAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
HPSTauHLTStudiesAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  // First thing, fill the nEvents
  nEvents->Fill(0.);

  event = iEvent.eventAuxiliary().event();
  lumi = iEvent.eventAuxiliary().luminosityBlock();
  run = iEvent.eventAuxiliary().run();
  if (verbose) printf("Run: %.0f    Evt: %.0f   Lumi: %.0f\n", run, event, lumi);


  if (!isRAW) {
    emptyVertices = 0;
    failNdof = 0;
    cutFlow->Fill(0., 1.);

    edm::Handle<std::vector<reco::Vertex>> vertices;   
    iEvent.getByToken(vertexToken_, vertices);
    if (vertices->empty()) return; // skip the event if no PV found
    if (vertices->empty()) emptyVertices = 1; // skip the event if no PV found
    const reco::Vertex &PV = vertices->front();
    if (PV.ndof() < 4) return; // bad vertex
    //nvtx = vertices.product()->size();
    //nvtxCleaned = 0;
    //for (const reco::Vertex &vertex : *vertices)
    //    if (!vertex.isFake()) ++nvtxCleaned;

    //// Get the number of true events
    //// This is used later for pile up reweighting
    //edm::Handle<std::vector<PileupSummaryInfo>> puInfo;   
    //iEvent.getByToken(puToken_, puInfo);
    //nTruePU = -99;
    //if (puInfo.isValid()) {
    //    if (puInfo->size() > 0) {
    //        nTruePU = puInfo->at(1).getTrueNumInteractions();
    //    }
    //}

    if (!(vertices->empty())) {
        if (PV.ndof() < 4) failNdof = 1; // bad vertex
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
    else { // isData
        cutFlow->Fill(2., 1.); // no requirement 
        cutFlow->Fill(3., 1.); // no requirement 
    }




    edm::Handle<std::vector<pat::Muon>> muons; 
    iEvent.getByToken(muonToken_, muons);
    // Storage for the "best" muon
    pat::Muon bestMuon;
    passingMuons = 0;
    nSlimmedMuons = 0;
    nVetoMuons = 0;


    tmpPt = -9;
    tmpEta = -9;
    tmpPhi = -9;
    tmpIso = -9;
    for (const pat::Muon &mu : *muons) {
        ++nSlimmedMuons;
        tmpPt = mu.pt();
        tmpEta = mu.eta();
        tmpPhi = mu.phi();
        tmpIso = (mu.pfIsolationR04().sumChargedHadronPt
            + TMath::Max(0., mu.pfIsolationR04().sumNeutralHadronEt
            + mu.pfIsolationR04().sumPhotonEt
            - 0.5*mu.pfIsolationR04().sumPUPt))
            /mu.pt();
        if (mu.pt() > 10 && fabs(mu.eta()) < 2.4 && mu.isLooseMuon() && tmpIso < 0.3) ++nVetoMuons;
        if (mu.pt() < 20 || fabs(mu.eta()) > 2.1 || !mu.isMediumMuon()) continue;
        if (tmpIso > 0.1) continue;
        ++passingMuons;
        bestMuon = mu;
    }
    // Require strictly 1 muon
    //if (!doTauTau)
    //    if (passingMuons == 0) return;
    //if (doTauTau)
    //    if (passingMuons > 0) return;
    cutFlow->Fill(4., 1.);
    // Extra lepton veto (muons)
    //if (passingMuons > 1) return;
    cutFlow->Fill(5., 1.);


    // Veto events with loose electrons
    Handle<edm::View<reco::GsfElectron> > electrons;
    iEvent.getByToken(electronToken_, electrons);
    Handle<edm::ValueMap<bool> > loose_id_decisions;
    iEvent.getByToken(eleLooseIdMapTag_, loose_id_decisions);

    passingElectrons = 0;
    for(unsigned int i = 0; i< electrons->size(); ++i){
     
        const auto ele = electrons->ptrAt(i);
        int isLooseID = (*loose_id_decisions)[ele];
        if(isLooseID && ele->p4().Pt()>10 && fabs(ele->p4().Eta())<2.5)
            ++passingElectrons;
    }


    // Extra lepton veto (electrons)
    //if (passingElectrons > 0) return;
    cutFlow->Fill(6., 1.);


    edm::Handle<std::vector<pat::Tau>> taus;
    iEvent.getByToken(slimmedTauToken_, taus);
    // Storage for the good taus
    std::vector<pat::TauRef> passingTausV;
    std::vector<pat::TauRef> passingGenMatchedTausV;

    // Inverting the ordering will leave us with the highest pt tau selected
    for (size_t iTau = 0; iTau != taus->size(); ++iTau) {

        pat::TauRef tauCandidate(taus, iTau);

        if (tauCandidate->pt() < 20 || (fabs(tauCandidate->eta()) > 2.1) ||
            fabs(tauCandidate->charge()) != 1 ||
            tauCandidate->tauID("decayModeFindingNewDMs") < 0.5 ||
            //tauCandidate->tauID("againstElectronLooseMVA6") < 0.5 ||
            tauCandidate->tauID("againstElectronVLooseMVA6") < 0.5 ||
            tauCandidate->tauID("againstMuonLoose3") < 0.5) continue;

        if (!doTauTau) // For TauTau only require looser selection, but MuTau is tighter
            if (tauCandidate->tauID("againstMuonTight3") < 0.5) continue;
        
        // Require the loosest isolation WPs used by Tau POG
        // or require MVA Medium if requireMediumTauMVA selected
        if (requireMediumTauMVA) {
            if (tauCandidate->tauID("byMediumIsolationMVArun2v1DBoldDMwLT") < 0.5) continue;
        }
        else {
            if (tauCandidate->tauID("byVLooseIsolationMVArun2v1DBoldDMwLT") < 0.5 && 
                tauCandidate->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits") < 0.5) continue;
                //tauCandidate->tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03") < 0.5) continue;
        }
 
        // Make sure tau doesn't overlap muon
        if (!doTauTau &&  deltaR( bestMuon.p4(), tauCandidate->p4() ) < 0.5) continue;

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
    //if (doTauTau && passingTausV.size() < 2) return;
    passingTaus = passingTausV.size();
    cutFlow->Fill(7., 1.);
    if (verbose) std::cout << "Passing Muons: " << passingMuons << "   Passing Taus: " << passingTausV.size() << std::endl;
    if (verbose) std::cout << " --- From vector   Passing Taus: " << passingTausV.size() << " gen matched taus: " << passingGenMatchedTausV.size() << std::endl;

    // Pt order passing reco::taus
    std::sort(passingTausV.begin(), passingTausV.end(), [](pat::TauRef a, pat::TauRef b) {
        return a->pt() > b->pt();
    });


    edm::Handle<std::vector<reco::PFTau>> hpsTaus;
    try {iEvent.getByToken(hpsTauToken_, hpsTaus);} catch (...) {;}
    edm::Handle<reco::PFTauDiscriminator> hpsTauDMs;
    try {iEvent.getByToken(hpsTauDecayModeToken_, hpsTauDMs);} catch (...) {;}

    hpsTauSize = -9;
    hpsTauPt = -9;
    hpsTauEta = -9;
    hpsTauPhi = -9;
    hpsTauDM = -9;
    hpsTauDMFinding = -9;
    hpsTauDR = -9;
    if (hpsTaus.isValid()) {
        hpsTauSize = hpsTaus->size();
        for (size_t iTau = 0; iTau != hpsTaus->size(); ++iTau) {

            reco::PFTauRef hpsTauCandidate(hpsTaus, iTau);
            if (hpsTauCandidate->pt() < 18 || fabs(hpsTauCandidate->eta()) > 2.2) continue;

            if (deltaR(passingTausV.at(0)->p4(), hpsTauCandidate->p4()) < 0.5) {
                hpsTauPt = hpsTauCandidate->pt();
                hpsTauEta = hpsTauCandidate->eta();
                hpsTauPhi = hpsTauCandidate->phi();
                hpsTauDM = hpsTauCandidate->decayMode();
                hpsTauDR = deltaR(passingTausV.at(0)->p4(), hpsTauCandidate->p4());
                if (hpsTauDMs.isValid()) {
                    hpsTauDMFinding = (*hpsTauDMs)[hpsTauCandidate];
                }
                if (verbose) std::cout << "found hps tau matching slimmed tau:" << std::endl;
                if (verbose) std::cout << " slimmed pt: " << passingTausV.at(0)->pt() << "      DM: " << passingTausV.at(0)->decayMode() <<  std::endl;
                if (verbose) std::cout << " hps     pt: " << hpsTauPt << "      DM: " << hpsTauDM << std::endl;
                break; // only match to leading tau
            }
        }
    }
    //std::cout << "Finishd hps part" << std::endl;

    edm::Handle<std::vector<reco::PFTau>> defaultTaus;
    try {iEvent.getByToken(defaultTauToken_, defaultTaus);} catch (...) {;}
    edm::Handle<reco::PFTauDiscriminator> defaultTauDMs;
    try {iEvent.getByToken(defaultTauDecayModeToken_, defaultTauDMs);} catch (...) {;}

    defaultTauSize = -9;
    defaultTauPt = -9;
    defaultTauEta = -9;
    defaultTauPhi = -9;
    defaultTauDM = -9;
    defaultTauDMFinding = -9;
    defaultTauDR = -9;
    if (defaultTaus.isValid()) {
        defaultTauSize = defaultTaus->size();
        for (size_t iTau = 0; iTau != defaultTaus->size(); ++iTau) {

            reco::PFTauRef defaultTauCandidate(defaultTaus, iTau);
            if (defaultTauCandidate->pt() < 18 || fabs(defaultTauCandidate->eta()) > 2.2) continue;

            if (deltaR(passingTausV.at(0)->p4(), defaultTauCandidate->p4()) < 0.5) {
                defaultTauPt = defaultTauCandidate->pt();
                defaultTauEta = defaultTauCandidate->eta();
                defaultTauPhi = defaultTauCandidate->phi();
                defaultTauDM = defaultTauCandidate->decayMode();
                defaultTauDR = deltaR(passingTausV.at(0)->p4(), defaultTauCandidate->p4());
                if (defaultTauDMs.isValid()) {
                    defaultTauDMFinding = (*defaultTauDMs)[defaultTauCandidate];
                }
                if (verbose) std::cout << "found default tau matching slimmed tau:" << std::endl;
                if (verbose) std::cout << " slimmed pt: " << passingTausV.at(0)->pt() << "      DM: " << passingTausV.at(0)->decayMode() <<  std::endl;
                if (verbose) std::cout << " default     pt: " << defaultTauPt << "      DM: " << defaultTauDM << std::endl;
                break; // only match to leading tau
            }
        }
    }


    // Check for non-overlapping bjets
    // using Medium CISV value of 0.8
    edm::Handle<std::vector<pat::Jet>> jets;   
    iEvent.getByToken(jetToken_, jets);
    nBTag = 0;
    nBTagAll = 0;
    //bool btagged = false;
    for (const pat::Jet &j : *jets) {
        if (j.pt() < 20 || fabs(j.eta()) > 2.4 || j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags") < 0.8484) continue;
        ++nBTagAll;
        if (!doTauTau && deltaR(j, bestMuon) < 0.5) continue;
        if (deltaR(j.p4(), passingTausV.at(0)->p4()) < 0.5) continue;
        //btagged = true;
        ++nBTag;
    }
    //if (btagged) return;
    cutFlow->Fill(8., 1.);


    // Save our best tau and muon variables
    if (passingMuons > 0.5) {
        mPt = bestMuon.pt();
        mEta = bestMuon.eta();
        mPhi = bestMuon.phi();
        mIso = (bestMuon.pfIsolationR04().sumChargedHadronPt
            + TMath::Max(0., bestMuon.pfIsolationR04().sumNeutralHadronEt
            + bestMuon.pfIsolationR04().sumPhotonEt
            - 0.5*bestMuon.pfIsolationR04().sumPUPt))
            /bestMuon.pt();
    }
    else { // doTauTau
        mPt = -9;
        mEta = -9;
        mPhi = -9;
        mIso = -9;
    }
    
    tPt = passingTausV.at(0)->pt();
    tEta = passingTausV.at(0)->eta();
    tPhi = passingTausV.at(0)->phi();
    tMVAIsoVLoose = passingTausV.at(0)->tauID("byVLooseIsolationMVArun2v1DBoldDMwLT");
    tMVAIsoLoose  = passingTausV.at(0)->tauID("byLooseIsolationMVArun2v1DBoldDMwLT");
    tMVAIsoMedium = passingTausV.at(0)->tauID("byMediumIsolationMVArun2v1DBoldDMwLT");
    tMVAIsoTight  = passingTausV.at(0)->tauID("byTightIsolationMVArun2v1DBoldDMwLT");
    tMVAIsoVTight = passingTausV.at(0)->tauID("byVTightIsolationMVArun2v1DBoldDMwLT");
    tMVAIsoVVTight = passingTausV.at(0)->tauID("byVVTightIsolationMVArun2v1DBoldDMwLT");
    tIsoCmbLoose = passingTausV.at(0)->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits");
    //tIsoCmbLoose03 = passingTausV.at(0)->tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03");
    tIsoCmbMedium = passingTausV.at(0)->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits");
    //tIsoCmbMedium03 = passingTausV.at(0)->tauID("byMediumCombinedIsolationDeltaBetaCorr3HitsdR03");
    tIsoCmbTight = passingTausV.at(0)->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits");
    //tIsoCmbTight03 = passingTausV.at(0)->tauID("byTightCombinedIsolationDeltaBetaCorr3HitsdR03");
    tDecayMode = passingTausV.at(0)->decayMode();
    tDMFinding = passingTausV.at(0)->tauID("decayModeFindingNewDMs");
    if (!doTauTau )
        leptonDR_m_t1 = deltaR( bestMuon, *passingTausV.at(0) );

    if (passingTausV.size() > 1) {
        t2Pt = passingTausV.at(1)->pt();
        t2Eta = passingTausV.at(1)->eta();
        t2Phi = passingTausV.at(1)->phi();
        t2MVAIsoVLoose = passingTausV.at(1)->tauID("byVLooseIsolationMVArun2v1DBoldDMwLT");
        t2MVAIsoLoose  = passingTausV.at(1)->tauID("byLooseIsolationMVArun2v1DBoldDMwLT");
        t2MVAIsoMedium = passingTausV.at(1)->tauID("byMediumIsolationMVArun2v1DBoldDMwLT");
        t2MVAIsoTight  = passingTausV.at(1)->tauID("byTightIsolationMVArun2v1DBoldDMwLT");
        t2MVAIsoVTight = passingTausV.at(1)->tauID("byVTightIsolationMVArun2v1DBoldDMwLT");
        t2MVAIsoVVTight = passingTausV.at(1)->tauID("byVVTightIsolationMVArun2v1DBoldDMwLT");
        t2IsoCmbLoose = passingTausV.at(1)->tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits");
        //t2IsoCmbLoose03 = passingTausV.at(1)->tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03");
        t2IsoCmbMedium = passingTausV.at(1)->tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits");
        //t2IsoCmbMedium03 = passingTausV.at(1)->tauID("byMediumCombinedIsolationDeltaBetaCorr3HitsdR03");
        t2IsoCmbTight = passingTausV.at(1)->tauID("byTightCombinedIsolationDeltaBetaCorr3Hits");
        //t2IsoCmbTight03 = passingTausV.at(1)->tauID("byTightCombinedIsolationDeltaBetaCorr3HitsdR03");
        t2DecayMode = passingTausV.at(1)->decayMode();
        if (!doTauTau )
            leptonDR_m_t2 = deltaR( bestMuon, *passingTausV.at(1) );
        leptonDR_t1_t2 = deltaR( *passingTausV.at(0), *passingTausV.at(1) );

        // If tau2 is overlapped, fill with -9
        if (!doTauTau && leptonDR_m_t2 < 0.5) {
            t2Pt = -9;
            t2Eta = -9;
            t2Phi = -9;
            t2MVAIsoVLoose = -9;
            t2MVAIsoLoose  = -9;
            t2MVAIsoMedium = -9;
            t2MVAIsoTight  = -9;
            t2MVAIsoVTight = -9;
            t2MVAIsoVVTight = -9;
            t2IsoCmbLoose   = -9;
            //t2IsoCmbLoose03 = -9;
            t2IsoCmbMedium  = -9;
            //t2IsoCmbMedium03 = -9;
            t2IsoCmbTight   = -9;
            //t2IsoCmbTight03 = -9;
            t2DecayMode = -9;
            leptonDR_m_t2 = -9;
            leptonDR_t1_t2 = -9;
        }
    }
    else {
        t2Pt = -9;
        t2Eta = -9;
        t2Phi = -9;
        t2MVAIsoVLoose = -9;
        t2MVAIsoLoose  = -9;
        t2MVAIsoMedium = -9;
        t2MVAIsoTight  = -9;
        t2MVAIsoVTight = -9;
        t2MVAIsoVVTight = -9;
        t2IsoCmbLoose   = -9;
        //t2IsoCmbLoose03 = -9;
        t2IsoCmbMedium  = -9;
        //t2IsoCmbMedium03 = -9;
        t2IsoCmbTight   = -9;
        //t2IsoCmbTight03 = -9;
        t2DecayMode = -9;
        leptonDR_m_t2 = -9;
        leptonDR_t1_t2 = -9;
    }



    // Check for overlapping Gen Taus
    // with reconstructed gen taus of 3 types
    // and normal gen particles
    t1_gen_match = -9;
    genTauPt = -9;
    t2_gen_match = -9;
    t2genPt = -9;
    if (!isData) {

        getGenMatchNumber( 
            t1_gen_match, genTauPt, passingTausV.at(0),
            genHTaus, genETaus, genMTaus, genParticles);

        if (passingTausV.size() > 1) {
            getGenMatchNumber( 
                t2_gen_match, t2genPt, passingTausV.at(1),
                genHTaus, genETaus, genMTaus, genParticles);
        }
    }

    // Get MET for transverse mass calculation 
    edm::Handle<std::vector<pat::MET>> mets;   
    iEvent.getByToken(metToken_, mets);
    const pat::MET &met = mets->front();
    pfMet = met.pt();
    if (!doTauTau )
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
    else if (doTauTau && passingTausV.size() > 1) {
        TLorentzVector l2 = TLorentzVector( 0., 0., 0., 0. );
        l2.SetPtEtaPhiM( passingTausV.at(0)->pt(), passingTausV.at(0)->eta(),
            passingTausV.at(0)->phi(), passingTausV.at(0)->mass() );
        TLorentzVector l1 = TLorentzVector( 0., 0., 0., 0. );
        l1.SetPtEtaPhiM( passingTausV.at(1)->pt(), passingTausV.at(1)->eta(),
            passingTausV.at(1)->phi(), passingTausV.at(1)->mass() );
        m_vis = (l1 + l2).M();


        // Same sign comparison
        if (passingTausV.at(1)->charge() + passingTausV.at(0)->charge() == 0) SS = 0;
        else SS = 1;
    }
    else {
        m_vis = -9;
        SS = -9;
    }

    if (SS == -1) isOS = -1;
    if (SS == 0) isOS = 1;
    if (SS == 1) isOS = 0;


    edm::Handle<edm::TriggerResults> triggerResults;   
    iEvent.getByToken(triggerToken_, triggerResults);
    edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
    iEvent.getByToken(triggerObjectsToken_, triggerObjects);

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


    //// Do trigger object matching
    //// for the moment, just record the number
    //// of times our 'best' objects match
    //// this can be expanded later to indivual trigs if necessary
    //mTrigMatch = 0;
    //tTrigMatch = 0;
    //t2TrigMatch = 0;
    //for (pat::TriggerObjectStandAlone obj : *triggerObjects) { // note: not "const &" since we want to call unpackPathNames
    //    obj.unpackPathNames(names);
    //    std::vector<std::string> pathNamesLast = obj.pathNames(true);
    //    // pathNamesLast = vector of flags, if this object was used in the final 
    //    // filter of a succeeding HLT path resp. in a succeeding 
    //    // condition of a succeeding L1 algorithm
    //    for (unsigned h = 0, n = pathNamesLast.size(); h < n; ++h) {
    //        std::cout << "9a - xxx" << pathNamesLast[h] << std::endl;
    //        if (std::find( usedPaths.begin(), usedPaths.end(), pathNamesLast[h]) != usedPaths.end()) {
    //            std::cout << " ---  " << pathNamesLast[h] << std::endl;
    //            std::cout << "\tTrigger object:  pt " << obj.pt() << ", eta " << obj.eta() << ", phi " << obj.phi() << std::endl;
    //            if (!doTauTau) {
    //                float drMu = deltaR( bestMuon, obj );
    //                //std::cout << "\tbestMuon dR: " << drMu << std::endl;
    //                if (drMu < 0.5) ++mTrigMatch;
    //            }
    //            float drTau = deltaR( *passingTausV.at(0), obj );
    //            //std::cout << "\tpassingTausV.at(0) dR: " << drTau << std::endl;
    //            if (drTau < 0.5) ++tTrigMatch;
    //            if (doTauTau) {
    //                float drTau2 = deltaR( *passingTausV.at(1), obj );
    //                //std::cout << "\tpassingTausV.at(0) dR: " << drTau << std::endl;
    //                if (drTau2 < 0.5) ++t2TrigMatch;
    //            }
    //        }
    //    }
    //}


    //std::cout << "10 - xxx" << std::endl;
    //// Do l1extra object matching
    //// Make sure to only consider l1 objects from the
    //// intended BX.  That is the size(0) and
    //// at(0,i) notation
    //edm::Handle<BXVector<l1t::Tau>> l1Taus; 
    //iEvent.getByToken(stage2TauToken_, l1Taus);
    //
    //getL1TauMatch( passingTausV.at(0), l1Taus, tL1Match, l1TauPt, l1TauIso);
    ////if (passingTausV.size() > 1) {
    ////    t2L1Match = getL1TauMatch( passingTausV.at(1), l1Taus);
    ////}
    //std::cout << "11 - xxx" << std::endl;



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

    edm::Handle<std::vector<reco::PFTau>> hpsTaus;
    try {iEvent.getByToken(hpsTauToken_, hpsTaus);} catch (...) {;}
    edm::Handle<reco::PFTauDiscriminator> hpsTauDMs;
    try {iEvent.getByToken(hpsTauDecayModeToken_, hpsTauDMs);} catch (...) {;}

    hpsTauSize = -9;
    hpsTauPt = -9;
    hpsTauEta = -9;
    hpsTauPhi = -9;
    hpsTauDM = -9;
    hpsTauDMFinding = -9;
    hpsTauDR = -9;
    
    std::vector<reco::PFTauRef> passingHPSTaus;

    if (hpsTaus.isValid()) {
        hpsTauSize = hpsTaus->size();
        for (size_t iTau = 0; iTau != hpsTaus->size(); ++iTau) {

            reco::PFTauRef hpsTauCandidate(hpsTaus, iTau);
            if (hpsTauCandidate->pt() < 18 || fabs(hpsTauCandidate->eta()) > 2.2) continue;
            passingHPSTaus.push_back( hpsTauCandidate );

            if (verbose) std::cout << "found hps tau matching slimmed tau:" << std::endl;
            if (verbose) std::cout << " hps     pt: " << hpsTauPt << "      DM: " << hpsTauDM << std::endl;
        }
    }

    std::sort(passingHPSTaus.begin(), passingHPSTaus.end(), [](reco::PFTauRef a, reco::PFTauRef b) {
        return a->pt() > b->pt();
    });

    if ( passingHPSTaus.size() > 0 ) {
        hpsTauPt = passingHPSTaus.at(0)->pt();
        hpsTauEta = passingHPSTaus.at(0)->eta();
        hpsTauPhi = passingHPSTaus.at(0)->phi();
        hpsTauDM = passingHPSTaus.at(0)->decayMode();
        if (hpsTauDMs.isValid()) {
            hpsTauDMFinding = (*hpsTauDMs)[passingHPSTaus.at(0)];
        }
    }
    if ( passingHPSTaus.size() > 1 ) {
        hpsTau2Pt = passingHPSTaus.at(1)->pt();
        hpsTau2Eta = passingHPSTaus.at(1)->eta();
        hpsTau2Phi = passingHPSTaus.at(1)->phi();
        hpsTau2DM = passingHPSTaus.at(1)->decayMode();
    }


    //std::cout << "Finishd hps part" << std::endl;

    edm::Handle<std::vector<reco::PFTau>> defaultTaus;
    try {iEvent.getByToken(defaultTauToken_, defaultTaus);} catch (...) {;}
    edm::Handle<reco::PFTauDiscriminator> defaultTauDMs;
    try {iEvent.getByToken(defaultTauDecayModeToken_, defaultTauDMs);} catch (...) {;}

    defaultTauSize = -9;
    defaultTauPt = -9;
    defaultTauEta = -9;
    defaultTauPhi = -9;
    defaultTauDM = -9;
    defaultTauDMFinding = -9;
    defaultTauDR = -9;

    std::vector<reco::PFTauRef> passingDefaultTaus;

    if (defaultTaus.isValid()) {
        defaultTauSize = defaultTaus->size();
        for (size_t iTau = 0; iTau != defaultTaus->size(); ++iTau) {

            reco::PFTauRef defaultTauCandidate(defaultTaus, iTau);
            if (defaultTauCandidate->pt() < 18 || fabs(defaultTauCandidate->eta()) > 2.2) continue;

            passingDefaultTaus.push_back( defaultTauCandidate );

            if (verbose) std::cout << "found default tau matching slimmed tau:" << std::endl;
            if (verbose) std::cout << " default     pt: " << defaultTauPt << "      DM: " << defaultTauDM << std::endl;
        }
    }

    std::sort(passingDefaultTaus.begin(), passingDefaultTaus.end(), [](reco::PFTauRef a, reco::PFTauRef b) {
        return a->pt() > b->pt();
    });

    if ( passingDefaultTaus.size() > 0 ) {
        defaultTauPt = passingDefaultTaus.at(0)->pt();
        defaultTauEta = passingDefaultTaus.at(0)->eta();
        defaultTauPhi = passingDefaultTaus.at(0)->phi();
        defaultTauDM = passingDefaultTaus.at(0)->decayMode();
        if (defaultTauDMs.isValid()) {
            defaultTauDMFinding = (*defaultTauDMs)[passingDefaultTaus.at(0)];
        }
    }
    if ( passingDefaultTaus.size() > 1 ) {
        defaultTau2Pt = passingDefaultTaus.at(1)->pt();
        defaultTau2Eta = passingDefaultTaus.at(1)->eta();
        defaultTau2Phi = passingDefaultTaus.at(1)->phi();
        defaultTau2DM = passingDefaultTaus.at(1)->decayMode();
    }

    edm::Handle<edm::TriggerResults> triggerResults;   
    iEvent.getByToken(triggerToken_, triggerResults);
    //edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
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
HPSTauHLTStudiesAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HPSTauHLTStudiesAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HPSTauHLTStudiesAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// ------------ for retrieving the gen_match variable used in HTT ------------------
void
HPSTauHLTStudiesAnalyzer::getGenMatchNumber( 
        float &gen_match,
        float &gen_pt,
        pat::TauRef& tau,
        edm::Handle<std::vector<reco::GenJet>> genHTaus,
        edm::Handle<std::vector<reco::GenJet>> genETaus,
        edm::Handle<std::vector<reco::GenJet>> genMTaus,
        edm::Handle<std::vector<reco::GenParticle>> genParticles) {

  // Find the closest gen particle to our candidate
  gen_match = -9;
  gen_pt = -9;
  if ( genParticles->size() > 0 ) {
      reco::GenParticle closest = genParticles->at(0);
      float closestDR = 999;
      float closestPt = 0.;
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
      float HTauPt = 0.;
      float ETauPt = 0.;
      float MTauPt = 0.;
      if ( genHTaus->size() > 0 ) {
          for (size_t j = 0; j != genHTaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genHTaus->at(j).p4() );
              if (tmpDR < closestDR_HTau) {
                  closestDR_HTau = tmpDR;
                  HTauPt = genHTaus->at(j).pt();
              }
          }
      }
      if ( genETaus->size() > 0 ) {
          for (size_t j = 0; j != genETaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genETaus->at(j).p4() );
              if (tmpDR < closestDR_ETau) {
                  closestDR_ETau = tmpDR;
                  ETauPt = genETaus->at(j).pt();
              }
          }
      }
      if ( genMTaus->size() > 0 ) {
          for (size_t j = 0; j != genMTaus->size(); ++j) {
              float tmpDR = deltaR( tau->p4(), genMTaus->at(j).p4() );
              if (tmpDR < closestDR_MTau) {
                  closestDR_MTau = tmpDR;
                  MTauPt = genMTaus->at(j).pt();
              }
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
            {
                  gen_match = 1.0;
                  gen_pt = closestPt;
            }
      else if (closestDR < closestGetTau && genID == 13 && closest.pt() > 8
              && closest.statusFlags().isPrompt() && closestDR < 0.2 )
            {
                  gen_match = 2.0;
                  gen_pt = closestPt;
            }
      // Other codes based off of not matching previous 2 options
      // as closest gen particle, retruns based on closest rebuilt gen tau
      else if (closestDR_ETau < 0.2 && closestDR_ETau < TMath::Min(closestDR_MTau, 
              closestDR_HTau))
            {
                gen_match = 3.0;
                gen_pt = ETauPt;
            }
      else if (closestDR_MTau < 0.2 && closestDR_MTau < TMath::Min(closestDR_ETau, 
              closestDR_HTau))
            {
                gen_match = 4.0;
                gen_pt = MTauPt;
            }
      else if (closestDR_HTau < 0.2 && closestDR_HTau < TMath::Min(closestDR_ETau, 
              closestDR_MTau))
            {
                gen_match = 5.0;
                gen_pt = HTauPt;
            }
      else gen_match = 6.0; // No match, return 6 for "fake tau"
  }
  return;
}

void
HPSTauHLTStudiesAnalyzer::getL1TauMatch( pat::TauRef& tau,
        edm::Handle<BXVector<l1t::Tau>> l1Taus, float& l1TauMatch, float& l1TauPt, float& l1TauIso ) {
    l1TauMatch = -9;
    l1TauPt = -9;
    l1TauIso = -9;
    if (l1Taus.isValid()) {
        l1TauMatch = 0;
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
            if (drTau < 0.5) {
                ++l1TauMatch;
                l1TauPt = l1Tau.pt();
                l1TauIso = l1Tau.hwIso();
            }
        }    
    } // end l1Taus

}

//define this as a plug-in
DEFINE_FWK_MODULE(HPSTauHLTStudiesAnalyzer);
