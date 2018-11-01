// -*- C++ -*-
//
// Package:    Acceptance/GenMassAnalyzer
// Class:      GenMassAnalyzer
// 
/**\class GenMassAnalyzer GenMassAnalyzer.cc Acceptance/GenMassAnalyzer/plugins/GenMassAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Tyler Henry Ruggles
//         Created:  Mon, 29 Feb 2016 10:32:40 GMT
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
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"



//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class GenMassAnalyzer : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit GenMassAnalyzer(const edm::ParameterSet&);
      ~GenMassAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      // ----------member data ---------------------------
      edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;
      edm::EDGetTokenT<LHEEventProduct> lheToken_;
      TTree *tree;
      float genMass, nTruePU, run, lumi, genPt, genEta, genPhi;
      double eventD;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
GenMassAnalyzer::GenMassAnalyzer(const edm::ParameterSet& iConfig) :
    puToken_(consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("puSrc"))),
    lheToken_(consumes<LHEEventProduct>(iConfig.getParameter<edm::InputTag>("lheSrc")))
{
   //now do what ever initialization is needed
   //usesResource("TFileService");
   edm::Service<TFileService> fs;
   TFileDirectory subDir = fs->mkdir( "events" );
   tree = subDir.make<TTree>("Ntuple","My Analyzer Ntuple");
   tree->Branch("run",&run,"run/F");
   tree->Branch("lumi",&lumi,"lumi/F");
   tree->Branch("eventD",&eventD,"eventD/D");
   tree->Branch("genMass",&genMass,"genMass/F");
   tree->Branch("genPt",&genPt,"genPt/F");
   tree->Branch("genEta",&genEta,"genEta/F");
   tree->Branch("genPhi",&genPhi,"genPhi/F");

}


GenMassAnalyzer::~GenMassAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
GenMassAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
    using namespace edm;
    edm::Handle<std::vector<PileupSummaryInfo>> puInfo;   
    iEvent.getByToken(puToken_, puInfo);
    edm::Handle<LHEEventProduct> lheProd;   
    iEvent.getByToken(lheToken_, lheProd);

    run = -1.0;
    lumi = -1.0;
    eventD = -1.0;
    genMass = -1.0;
    genPt = -1.0;
    genEta = -1.0;
    genPhi = -1.0;

    //std::cout << iEvent.eventAuxiliary().event() << std::endl;
    run = iEvent.eventAuxiliary().run();
    lumi = iEvent.eventAuxiliary().luminosityBlock();
    eventD = iEvent.eventAuxiliary().event();

    // Get the number of true events
    // This is used later for pile up reweighting
    if (puInfo->size() > 0) {
        //std::cout<<"pu size = "<<puInfo->size()<<std::endl;
        //std::cout<<puInfo->at(1).getTrueNumInteractions()<<std::endl;
        nTruePU = puInfo->at(1).getTrueNumInteractions();
    }



    //std::cout << lheProd << std::endl;
    //lhe
    //std::cout << lheProd.isValid() << std::endl;
    //lhef::HEPEUP lhe;
    //if (lheProd.isValid()) {
    //  lhe = lheProd->hepeup();
    //}
    //const lhef::HEPEUP lhe = lheProd.product()->hepeup();
    ////std::cout << lhe.ISTUP[0] << std::endl;
    //std::vector<int> outgoing;
    //std::vector<TLorentzVector> invmass;
    //for (uint32_t i = 0; i < lhe.ISTUP.size(); ++i) {
    //    if (lhe.ISTUP[i]) {
    //        int Id = TMath::Abs( lhe.IDUP[i] );
    //        if (Id==21||Id==1||Id==2||Id==3||Id==4||Id==5)
    //            outgoing.push_back( TMath::Abs( Id ));
    //        int Id2 = TMath::Abs( lhe.IDUP[i] );
    //        if (Id2==11||Id2==13||Id2==15) {
    //            TLorentzVector l = TLorentzVector( lhe.PUP[i][0],
    //                                               lhe.PUP[i][1],
    //                                               lhe.PUP[i][2],
    //                                               lhe.PUP[i][3]);
    //            invmass.push_back( l );
    //        }
    //    }
    //}
    //if (invmass.size() == 2) {
    //    //std::cout << "Len InvMass: "<<invmass.size()<<std::endl;
    //    TLorentzVector diLep = invmass[0];
    //    diLep += invmass[1];
    //    //std::cout << "m(ll) " << diLep.M() << std::endl;
    //    genMass = diLep.M();

    //}

    const lhef::HEPEUP lhe = lheProd.product()->hepeup();
    reco::Candidate::LorentzVector lorentz;
    for (size_t i = 0; i < lhe.ISTUP.size() ; ++i) {
        if (lhe.ISTUP[i] == 1 ) {
            int pdgId = abs(lhe.IDUP[i]);
            if (pdgId == 11 || pdgId == 13 || pdgId == 15) {
                reco::Candidate::LorentzVector tmpVec = reco::Candidate::LorentzVector(lhe.PUP[i].x[0],
                          lhe.PUP[i].x[1],
                          lhe.PUP[i].x[2],
                          lhe.PUP[i].x[3]);
                lorentz += tmpVec;
            }
        }
    }
    //std::cout << " - Gen Mass: " << lorentz.M() << std::endl;
    genMass = lorentz.M();
    genPt = lorentz.pt();
    genEta = lorentz.eta();
    genPhi = lorentz.phi();
  
    
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
GenMassAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
GenMassAnalyzer::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
GenMassAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenMassAnalyzer);
