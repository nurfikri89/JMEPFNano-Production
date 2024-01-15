#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"

typedef edm::Ptr<pat::PackedCandidate> PackedCandidatePtr;
typedef edm::View<reco::Candidate> CandView;

class PackedCandidatePtrSelector : public edm::stream::EDProducer<> {
public:
  explicit PackedCandidatePtrSelector(const edm::ParameterSet &);
  ~PackedCandidatePtrSelector() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  edm::EDGetTokenT<CandView> const srcToken_;
  StringCutObjectSelector<reco::Candidate, true> const selector_;
  // StringCutObjectSelector<pat::PackedCandidate> const selector_;
};

//
// constructors and destructor
//
PackedCandidatePtrSelector::PackedCandidatePtrSelector(edm::ParameterSet const& iConfig):
  srcToken_(consumes<CandView>(iConfig.getParameter<edm::InputTag>("src"))),
  selector_(iConfig.getParameter<std::string>("cut"))
{
  produces<std::vector<PackedCandidatePtr>>();
}

PackedCandidatePtrSelector::~PackedCandidatePtrSelector() {}


void PackedCandidatePtrSelector::produce(edm::Event& iEvent, edm::EventSetup const& iSetup) {
  auto outCands = std::make_unique<std::vector<PackedCandidatePtr>>();

  edm::Handle<CandView> h_cands;
  iEvent.getByToken(srcToken_, h_cands);

  // Now set the Ptrs with the orphan handles.
  for (size_t ic = 0; ic < h_cands->size(); ++ic) {
    auto cand = h_cands->ptrAt(ic);
    // Check the selection
    if (selector_(*cand)) {
      PackedCandidatePtr retval(cand);
      outCands->emplace_back(retval);
    }
  }
  iEvent.put(std::move(outCands));
}


void PackedCandidatePtrSelector::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("packedPFCandidates"));
  desc.add<std::string>("cut", "");
  descriptions.addWithDefaultLabel(desc);
}


DEFINE_FWK_MODULE(PackedCandidatePtrSelector);