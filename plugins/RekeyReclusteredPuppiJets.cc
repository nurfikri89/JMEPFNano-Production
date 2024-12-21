#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

class RekeyReclusteredPuppiJets : public edm::stream::EDProducer<> {
public:
  explicit RekeyReclusteredPuppiJets(const edm::ParameterSet &);
  ~RekeyReclusteredPuppiJets() override;

  static pat::Jet rekeyJet(const pat::Jet & jet, edm::Handle<edm::View<reco::Candidate>> & candHandle);
  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  //const std::string name_;
  const std::string name_;
  const std::string nameSV_;
  const std::string idx_name_;

  edm::EDGetTokenT<edm::View<pat::Jet>> jet_token_;
  edm::EDGetTokenT<reco::CandidateView> cand_token_;
};

//
// constructors and destructor
//
RekeyReclusteredPuppiJets::RekeyReclusteredPuppiJets(const edm::ParameterSet &iConfig):
  jet_token_(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jets"))),
  cand_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("candidates")))
{
  produces<pat::JetCollection>();
}

RekeyReclusteredPuppiJets::~RekeyReclusteredPuppiJets() {}

void RekeyReclusteredPuppiJets::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  edm::Handle<edm::View<pat::Jet> > src;
  iEvent.getByToken(jet_token_, src);

  edm::Handle<reco::CandidateView> cands_;
  iEvent.getByToken(cand_token_, cands_);

  auto out = std::make_unique<std::vector<pat::Jet>>();
  out->reserve(src->size());

  for (edm::View<pat::Jet>::const_iterator it = src->begin(), ed = src->end(); it != ed; ++it) {
    // out->push_back(*it);
    // pat::Jet & jet = out->back();
    pat::Jet thisPatJet = rekeyJet(*it, cands_);
    out->push_back(thisPatJet);
  }

  iEvent.put(std::move(out));
}

pat::Jet RekeyReclusteredPuppiJets::rekeyJet(const pat::Jet & jet, edm::Handle<edm::View<reco::Candidate>> & candHandle) {
  pat::Jet newJet(jet);
  newJet.clearDaughters();
  for (const auto & dauItr : jet.daughterPtrVector()) {
    const unsigned long key = dauItr.key();
    edm::Ptr<reco::Candidate> newDau = candHandle->ptrAt(key);
    newJet.addDaughter(newDau);
  }
  return newJet;
}

void RekeyReclusteredPuppiJets::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("jets", edm::InputTag("slimmedJets"));
  desc.add<edm::InputTag>("candidates", edm::InputTag("packedPFCandidates"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(RekeyReclusteredPuppiJets);