#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/TauReco/interface/PFTau.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CompositePtrCandidate.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/NanoAOD/interface/FlatTable.h"

class GenVisTauExtTableProducer : public edm::stream::EDProducer<> {
public:
  explicit GenVisTauExtTableProducer(const edm::ParameterSet &);
  ~GenVisTauExtTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  const edm::EDGetTokenT<reco::GenParticleCollection> genVisTaus_token_;
  const edm::EDGetTokenT<reco::GenJetCollection>      genJetTaus_token_;

  const std::string name_;

  const StringCutObjectSelector<reco::GenParticle> cut_;
};

//
// constructors and destructor
//
GenVisTauExtTableProducer::GenVisTauExtTableProducer(const edm::ParameterSet &iConfig):
  genVisTaus_token_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("srcGenVisTaus"))),
  genJetTaus_token_(consumes<reco::GenJetCollection>(iConfig.getParameter<edm::InputTag>("srcGenJetTaus"))),
  name_(iConfig.getParameter<std::string>("name")),
  cut_(iConfig.getParameter<std::string>("cut")){
  produces<nanoaod::FlatTable>(name_);
}

GenVisTauExtTableProducer::~GenVisTauExtTableProducer() {}

void GenVisTauExtTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  edm::Handle<reco::GenParticleCollection> genVisTaus;
  iEvent.getByToken(genVisTaus_token_, genVisTaus);

  edm::Handle<reco::GenJetCollection> genJetTaus;
  iEvent.getByToken(genJetTaus_token_, genJetTaus);

  std::vector<reco::GenParticle> genVisTausPassCut;
  for (size_t genVisTauIdx=0; genVisTauIdx <genVisTaus->size(); genVisTauIdx++) {
    const auto& genVisTau = (*genVisTaus)[genVisTauIdx];
    if (!cut_(genVisTau)) continue;
    genVisTausPassCut.push_back(genVisTau);
  }

  std::vector<float> ChgHad0_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> ChgHad0_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad0_phi(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad0_mass(genVisTausPassCut.size(), -1.f);
  std::vector<int>   ChgHad0_pdgId(genVisTausPassCut.size(),   0);

  std::vector<float> ChgHad1_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> ChgHad1_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad1_phi(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad1_mass(genVisTausPassCut.size(), -1.f);
  std::vector<int>   ChgHad1_pdgId(genVisTausPassCut.size(),   0);

  std::vector<float> ChgHad2_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> ChgHad2_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad2_phi(genVisTausPassCut.size(),  -9.f);
  std::vector<float> ChgHad2_mass(genVisTausPassCut.size(), -1.f);
  std::vector<int>   ChgHad2_pdgId(genVisTausPassCut.size(),   0);

  std::vector<float> Photon0_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> Photon0_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> Photon0_phi(genVisTausPassCut.size(),  -9.f);

  std::vector<float> Photon1_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> Photon1_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> Photon1_phi(genVisTausPassCut.size(),  -9.f);

  std::vector<float> Photon2_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> Photon2_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> Photon2_phi(genVisTausPassCut.size(),  -9.f);

  std::vector<float> Photon3_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> Photon3_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> Photon3_phi(genVisTausPassCut.size(),  -9.f);

  std::vector<float> NeuHad0_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> NeuHad0_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> NeuHad0_phi(genVisTausPassCut.size(),  -9.f);
  std::vector<float> NeuHad0_mass(genVisTausPassCut.size(), -1.f);
  std::vector<int>   NeuHad0_pdgId(genVisTausPassCut.size(),   0);

  std::vector<float> NeuHad1_pt(genVisTausPassCut.size(),   -1.f);
  std::vector<float> NeuHad1_eta(genVisTausPassCut.size(),  -9.f);
  std::vector<float> NeuHad1_phi(genVisTausPassCut.size(),  -9.f);
  std::vector<float> NeuHad1_mass(genVisTausPassCut.size(), -1.f);
  std::vector<int>   NeuHad1_pdgId(genVisTausPassCut.size(),   0);

  for (size_t genVisTauIdx=0; genVisTauIdx < genVisTausPassCut.size(); genVisTauIdx++) {
    const auto& genVisTau = genVisTausPassCut[genVisTauIdx];

    std::vector<reco::CandidatePtr> chgHads;
    std::vector<reco::CandidatePtr> photons;
    std::vector<reco::CandidatePtr> neuHads;

    for (const auto& genJetTau : *genJetTaus) {
      double dR2 = deltaR2(genJetTau, genVisTau);

      if (dR2 < 0.05*0.05) {
        //
        // Stolen from PhysicsTools/JetMCUtils/src/JetMCTag.cc
        // genTauDecayMode() function
        //
        const reco::CompositePtrCandidate::daughters &daughters = genJetTau.daughterPtrVector();
        for (const reco::CandidatePtr& daughter : daughters) {
          int pdg_id = abs(daughter->pdgId());
          switch (pdg_id) {
            case 22:
              photons.push_back(daughter);
              break;
            case 11:
              break;
            case 13:
              break;
            case 15:
              break;
            default: {
              if (daughter->charge() != 0){
                chgHads.push_back(daughter);
              }
              else{
                neuHads.push_back(daughter);
              }
            }
          }
        }
        break;// Found match. Break
      }
    }

    auto pTComparator_ = [](auto const& t1, auto const& t2) { return t1->pt() > t2->pt();};
    std::sort(chgHads.begin(), chgHads.end(), pTComparator_);
    std::sort(photons.begin(), photons.end(), pTComparator_);
    std::sort(neuHads.begin(), neuHads.end(), pTComparator_);

    if (chgHads.size() >= 1){
      ChgHad0_pt[genVisTauIdx]    = chgHads[0]->pt();
      ChgHad0_eta[genVisTauIdx]   = chgHads[0]->eta();
      ChgHad0_phi[genVisTauIdx]   = chgHads[0]->phi();
      ChgHad0_mass[genVisTauIdx]  = chgHads[0]->mass();
      ChgHad0_pdgId[genVisTauIdx] = chgHads[0]->pdgId();
    }
    if (chgHads.size() >= 2){
      ChgHad1_pt[genVisTauIdx]    = chgHads[1]->pt();
      ChgHad1_eta[genVisTauIdx]   = chgHads[1]->eta();
      ChgHad1_phi[genVisTauIdx]   = chgHads[1]->phi();
      ChgHad1_mass[genVisTauIdx]  = chgHads[1]->mass();
      ChgHad1_pdgId[genVisTauIdx] = chgHads[1]->pdgId();
    }
    if (chgHads.size() >= 3){
      ChgHad2_pt[genVisTauIdx]    = chgHads[2]->pt();
      ChgHad2_eta[genVisTauIdx]   = chgHads[2]->eta();
      ChgHad2_phi[genVisTauIdx]   = chgHads[2]->phi();
      ChgHad2_mass[genVisTauIdx]  = chgHads[2]->mass();
      ChgHad2_pdgId[genVisTauIdx] = chgHads[2]->pdgId();
    }
    if (photons.size() >= 1){
      Photon0_pt[genVisTauIdx]    = photons[0]->pt();
      Photon0_eta[genVisTauIdx]   = photons[0]->eta();
      Photon0_phi[genVisTauIdx]   = photons[0]->phi();
    }
    if (photons.size() >= 2){
      Photon1_pt[genVisTauIdx]    = photons[1]->pt();
      Photon1_eta[genVisTauIdx]   = photons[1]->eta();
      Photon1_phi[genVisTauIdx]   = photons[1]->phi();
    }
    if (photons.size() >= 3){
      Photon2_pt[genVisTauIdx]    = photons[2]->pt();
      Photon2_eta[genVisTauIdx]   = photons[2]->eta();
      Photon2_phi[genVisTauIdx]   = photons[2]->phi();
    }
    if (photons.size() >= 4){
      Photon3_pt[genVisTauIdx]    = photons[3]->pt();
      Photon3_eta[genVisTauIdx]   = photons[3]->eta();
      Photon3_phi[genVisTauIdx]   = photons[3]->phi();
    }
    if (neuHads.size() >= 1){
      NeuHad0_pt[genVisTauIdx]    = neuHads[0]->pt();
      NeuHad0_eta[genVisTauIdx]   = neuHads[0]->eta();
      NeuHad0_phi[genVisTauIdx]   = neuHads[0]->phi();
      NeuHad0_mass[genVisTauIdx]  = neuHads[0]->mass();
      NeuHad0_pdgId[genVisTauIdx] = neuHads[0]->pdgId();
    }
    if (neuHads.size() >= 2){
      NeuHad1_pt[genVisTauIdx]    = neuHads[1]->pt();
      NeuHad1_eta[genVisTauIdx]   = neuHads[1]->eta();
      NeuHad1_phi[genVisTauIdx]   = neuHads[1]->phi();
      NeuHad1_mass[genVisTauIdx]  = neuHads[1]->mass();
      NeuHad1_pdgId[genVisTauIdx] = neuHads[1]->pdgId();
    }
  }

  auto candTable = std::make_unique<nanoaod::FlatTable>(genVisTausPassCut.size(), name_, false, true);
  candTable->addColumn<float> ("ChgHad0_pt",   ChgHad0_pt,    "Leading ChgHad pt",   15);
  candTable->addColumn<float> ("ChgHad0_eta",  ChgHad0_eta,   "Leading ChgHad eta",  15);
  candTable->addColumn<float> ("ChgHad0_phi",  ChgHad0_phi,   "Leading ChgHad phi",  15);
  candTable->addColumn<float> ("ChgHad0_mass", ChgHad0_mass,  "Leading ChgHad mass", 15);
  candTable->addColumn<int>   ("ChgHad0_pdgId",ChgHad0_pdgId, "Leading ChgHad pdgId"   );
  candTable->addColumn<float> ("ChgHad1_pt",   ChgHad1_pt,    "2nd-Leading ChgHad pt",   15);
  candTable->addColumn<float> ("ChgHad1_eta",  ChgHad1_eta,   "2nd-Leading ChgHad eta",  15);
  candTable->addColumn<float> ("ChgHad1_phi",  ChgHad1_phi,   "2nd-Leading ChgHad phi",  15);
  candTable->addColumn<float> ("ChgHad1_mass", ChgHad1_mass,  "2nd-Leading ChgHad mass", 15);
  candTable->addColumn<int>   ("ChgHad1_pdgId",ChgHad1_pdgId, "2nd-Leading ChgHad pdgId"   );
  candTable->addColumn<float> ("ChgHad2_pt",   ChgHad2_pt,    "3rd-Leading ChgHad pt",   15);
  candTable->addColumn<float> ("ChgHad2_eta",  ChgHad2_eta,   "3rd-Leading ChgHad eta",  15);
  candTable->addColumn<float> ("ChgHad2_phi",  ChgHad2_phi,   "3rd-Leading ChgHad phi",  15);
  candTable->addColumn<float> ("ChgHad2_mass", ChgHad2_mass,  "3rd-Leading ChgHad mass", 15);
  candTable->addColumn<int>   ("ChgHad2_pdgId",ChgHad2_pdgId, "3rd-Leading ChgHad pdgId"   );
  candTable->addColumn<float> ("Photon0_pt",   Photon0_pt,    "Leading Photon pt",   15);
  candTable->addColumn<float> ("Photon0_eta",  Photon0_eta,   "Leading Photon eta",  15);
  candTable->addColumn<float> ("Photon0_phi",  Photon0_phi,   "Leading Photon phi",  15);
  candTable->addColumn<float> ("Photon1_pt",   Photon1_pt,    "2nd-Leading Photon pt",   15);
  candTable->addColumn<float> ("Photon1_eta",  Photon1_eta,   "2nd-Leading Photon eta",  15);
  candTable->addColumn<float> ("Photon1_phi",  Photon1_phi,   "2nd-Leading Photon phi",  15);
  candTable->addColumn<float> ("Photon2_pt",   Photon2_pt,    "3rd-Leading Photon pt",   15);
  candTable->addColumn<float> ("Photon2_eta",  Photon2_eta,   "3rd-Leading Photon eta",  15);
  candTable->addColumn<float> ("Photon2_phi",  Photon2_phi,   "3rd-Leading Photon phi",  15);
  candTable->addColumn<float> ("Photon3_pt",   Photon3_pt,    "4th-Leading Photon pt",   15);
  candTable->addColumn<float> ("Photon3_eta",  Photon3_eta,   "4th-Leading Photon eta",  15);
  candTable->addColumn<float> ("Photon3_phi",  Photon3_phi,   "4th-Leading Photon phi",  15);
  candTable->addColumn<float> ("NeuHad0_pt",   NeuHad0_pt,    "Leading NeuHad pt",   15);
  candTable->addColumn<float> ("NeuHad0_eta",  NeuHad0_eta,   "Leading NeuHad eta",  15);
  candTable->addColumn<float> ("NeuHad0_phi",  NeuHad0_phi,   "Leading NeuHad phi",  15);
  candTable->addColumn<float> ("NeuHad0_mass", NeuHad0_mass,  "Leading NeuHad mass", 15);
  candTable->addColumn<int>   ("NeuHad0_pdgId",NeuHad0_pdgId, "Leading NeuHad pdgId"   );
  candTable->addColumn<float> ("NeuHad1_pt",   NeuHad1_pt,    "2nd-Leading NeuHad pt",   15);
  candTable->addColumn<float> ("NeuHad1_eta",  NeuHad1_eta,   "2nd-Leading NeuHad eta",  15);
  candTable->addColumn<float> ("NeuHad1_phi",  NeuHad1_phi,   "2nd-Leading NeuHad phi",  15);
  candTable->addColumn<float> ("NeuHad1_mass", NeuHad1_mass,  "2nd-Leading NeuHad mass", 15);
  candTable->addColumn<int>   ("NeuHad1_pdgId",NeuHad1_pdgId, "2nd-Leading NeuHad pdgId"   );

  iEvent.put(std::move(candTable), name_);
}

void GenVisTauExtTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "genVisTaus");
  desc.add<std::string>("cut",   "");
  desc.add<edm::InputTag>("srcGenVisTaus", edm::InputTag("genVisTaus"));
  desc.add<edm::InputTag>("srcGenJetTaus", edm::InputTag("tauGenJetsSelectorAllHadronsForNano"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(GenVisTauExtTableProducer);