#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"

#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

template<typename T>
class SimpleJetConstituentTableProducer : public edm::stream::EDProducer<> {
public:
  explicit SimpleJetConstituentTableProducer(const edm::ParameterSet &);
  ~SimpleJetConstituentTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  //const std::string name_;
  const std::string name_;
  const std::string nameSV_;
  const std::string idx_name_;

  edm::EDGetTokenT<edm::View<T>> jet_token_;
  edm::EDGetTokenT<reco::CandidateView> cand_token_;

  edm::Handle<reco::CandidateView> cands_;
};

//
// constructors and destructor
//
template< typename T>
SimpleJetConstituentTableProducer<T>::SimpleJetConstituentTableProducer(const edm::ParameterSet &iConfig): 
  name_(iConfig.getParameter<std::string>("name")),
  idx_name_(iConfig.getParameter<std::string>("idx_name")),
  jet_token_(consumes<edm::View<T>>(iConfig.getParameter<edm::InputTag>("jets"))),
  cand_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("candidates")))
{
  produces<nanoaod::FlatTable>(name_);
  produces<std::vector<reco::CandidatePtr>>();
}

template< typename T>
SimpleJetConstituentTableProducer<T>::~SimpleJetConstituentTableProducer() {}

template< typename T>
void SimpleJetConstituentTableProducer<T>::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  // elements in all these collections must have the same order!
  auto outCands = std::make_unique<std::vector<reco::CandidatePtr>>();
  std::vector<int> jetIdx_pf, pfcandIdx;

  auto jets = iEvent.getHandle(jet_token_);
  iEvent.getByToken(cand_token_, cands_);

  for (unsigned i_jet = 0; i_jet < jets->size(); ++i_jet) {
    const auto &jet = jets->at(i_jet);

    // PF Cands
    std::vector<reco::CandidatePtr> const & daughters = jet.daughterPtrVector();

    for (const auto &cand : daughters) {
      auto candPtrs = cands_->ptrs();
      auto candInNewList = std::find( candPtrs.begin(), candPtrs.end(), cand );
      if ( candInNewList == candPtrs.end() ) {
        //std::cout << "Cannot find candidate : " << cand.id() << ", " << cand.key() << ", pt = " << cand->pt() << std::endl;
        continue;
      }
      outCands->push_back(cand);
      jetIdx_pf.push_back(i_jet);
      pfcandIdx.push_back(candInNewList - candPtrs.begin());
    }
  }// end jet loop

  auto candTable = std::make_unique<nanoaod::FlatTable>(outCands->size(), name_, false);
  // We fill from here only stuff that cannot be created with the SimpleFlatTableProducer
  candTable->addColumn<int>(idx_name_, pfcandIdx, "Index in the candidate list");
  candTable->addColumn<int>("jetIdx", jetIdx_pf, "Index of the parent jet");
  iEvent.put(std::move(candTable), name_);
  iEvent.put(std::move(outCands));
}

template< typename T>
void SimpleJetConstituentTableProducer<T>::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "JetPFCands");
  desc.add<std::string>("idx_name", "candIdx");
  desc.add<edm::InputTag>("jets", edm::InputTag("slimmedJets"));
  desc.add<edm::InputTag>("candidates", edm::InputTag("packedPFCandidates"));
  descriptions.addWithDefaultLabel(desc);
}

typedef SimpleJetConstituentTableProducer<pat::Jet> SimplePatJetConstituentTableProducer;
typedef SimpleJetConstituentTableProducer<reco::GenJet> SimpleGenJetConstituentTableProducer;

DEFINE_FWK_MODULE(SimplePatJetConstituentTableProducer);
DEFINE_FWK_MODULE(SimpleGenJetConstituentTableProducer);
