#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

#include "PhysicsTools/JetMCUtils/interface/CandMCTag.h"

class GenParticleCandidateExtTableProducer : public edm::stream::EDProducer<> {
public:
  explicit GenParticleCandidateExtTableProducer(const edm::ParameterSet &);
  ~GenParticleCandidateExtTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;
  std::vector<int> decayFromBHadronAndCHadron(const reco::Candidate &);

  const edm::EDGetTokenT<reco::CandidateView> genpartcands_token_;
  const std::string name_;
};

//
// constructors and destructor
//
GenParticleCandidateExtTableProducer::GenParticleCandidateExtTableProducer(const edm::ParameterSet &iConfig):
  genpartcands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcGenPartCandidates"))),
  name_(iConfig.getParameter<std::string>("name"))
{
  produces<nanoaod::FlatTable>(name_);
}

GenParticleCandidateExtTableProducer::~GenParticleCandidateExtTableProducer() {}

void GenParticleCandidateExtTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  edm::Handle<reco::CandidateView> genPartCands;
  iEvent.getByToken(genpartcands_token_, genPartCands);

  std::vector<int> bHadronAncestorPDGIdVec;
  std::vector<int> cHadronAncestorPDGIdVec;
  bHadronAncestorPDGIdVec.reserve(genPartCands->size());
  cHadronAncestorPDGIdVec.reserve(genPartCands->size());

  for (size_t i = 0; i < genPartCands->size(); ++i) {
    reco::CandidatePtr candPtr = genPartCands->ptrAt(i);
    const reco::Candidate* cand = candPtr.get();
    std::vector<int> pdgIdBHadCHad = decayFromBHadronAndCHadron(*cand);
    bHadronAncestorPDGIdVec.push_back(pdgIdBHadCHad[0]);
    cHadronAncestorPDGIdVec.push_back(pdgIdBHadCHad[1]);
  }

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(genPartCands->size(), name_, false, true);
  candTable->addColumn<int>("bHadronAncestorPDGId", bHadronAncestorPDGIdVec, "pdgId of b-Hadron ancestor. 0 if there is none");
  candTable->addColumn<int>("cHadronAncestorPDGId", cHadronAncestorPDGIdVec, "pdgId of c-Hadron ancestor. 0 if there is none");
  iEvent.put(std::move(candTable), name_);
}

//
// Shamelessly stolen and modified from PhysicsTools/JetMCUtils/src/JetMCTag.cc
// For each genparticle, check if it has *any* ancestor that is a b-hadron or a c-hadron.
// Save the pdgId of the ancestor.
//
std::vector<int> GenParticleCandidateExtTableProducer::decayFromBHadronAndCHadron(const reco::Candidate &c){
  int bHadronPDGId = 0;
  int cHadronPDGId = 0;
  std::vector<const reco::Candidate *> allParents = CandMCTagUtils::getAncestors(c); // From PhysicsTools/JetMCUtils/interface/CandMCTag.h
  for (std::vector<const reco::Candidate *>::const_iterator aParent = allParents.begin(); aParent != allParents.end(); aParent++) {
    if (CandMCTagUtils::hasBottom(**aParent)){// From PhysicsTools/JetMCUtils/interface/CandMCTag.h
      bHadronPDGId = (*aParent)->pdgId();
    }
    if (CandMCTagUtils::hasCharm(**aParent)){// From PhysicsTools/JetMCUtils/interface/CandMCTag.h
      cHadronPDGId = (*aParent)->pdgId();
    }
  }
  return {bHadronPDGId,cHadronPDGId};
}

void GenParticleCandidateExtTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "GenPartCand");
  desc.add<edm::InputTag>("srcGenPartCandidates", edm::InputTag("finalGenJetsConstituents"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(GenParticleCandidateExtTableProducer);