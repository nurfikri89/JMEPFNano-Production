#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/transform.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

template<typename T>
class CandidateJetIdxExtTableProducer : public edm::stream::EDProducer<> {
public:
  explicit CandidateJetIdxExtTableProducer(const edm::ParameterSet &);
  ~CandidateJetIdxExtTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  edm::EDGetTokenT<reco::CandidateView> cands_token_;
  const std::string name_;

  std::vector<edm::EDGetTokenT<edm::View<T>>> v_jets_tokens_;
  std::vector<std::string> v_jetIdxNames_;
  std::vector<std::string> v_jetIdxDocs_;
  std::vector<std::string> v_jetCutStr_;

  std::vector<StringCutObjectSelector<T>> v_jetCut_;
};

//
// constructors and destructor
//
template< typename T>
CandidateJetIdxExtTableProducer<T>::CandidateJetIdxExtTableProducer(const edm::ParameterSet &iConfig):
  cands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("candidates"))),
  name_(iConfig.getParameter<std::string>("name"))
{
  v_jets_tokens_ = edm::vector_transform(
    iConfig.getParameter<std::vector<edm::InputTag>>("jetsV"),
    [this](edm::InputTag const& tag) {return consumes<edm::View<T>>(tag);}
  );
  v_jetIdxNames_ = iConfig.getParameter<std::vector<std::string>>("jetIdxNamesV");
  v_jetIdxDocs_ = iConfig.getParameter<std::vector<std::string>>("jetIdxDocsV");
  v_jetCutStr_ = iConfig.getParameter<std::vector<std::string>>("jetCutV");
  for (size_t iC = 0; iC < v_jetCutStr_.size(); ++iC) {
    v_jetCut_.push_back(StringCutObjectSelector<T>(v_jetCutStr_[iC]));
  }

  produces<nanoaod::FlatTable>(name_);
}

template< typename T>
CandidateJetIdxExtTableProducer<T>::~CandidateJetIdxExtTableProducer() {}

template< typename T>
void CandidateJetIdxExtTableProducer<T>::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  //
  // Retrieve candidates
  //
  edm::Handle<reco::CandidateView> cands;
  iEvent.getByToken(cands_token_, cands);
  auto candPtrs = cands->ptrs();

  //
  // Retrieve jet collections
  //
  std::vector<edm::Handle<edm::View<T>>> v_jetsHandle;
  for (size_t i = 0; i < v_jets_tokens_.size(); ++i) {
    v_jetsHandle.push_back(iEvent.getHandle(v_jets_tokens_[i]));
  }

  //
  // Prepare vector of vector of indices
  //
  std::vector<std::vector<int>> v_v_jetIdxs(
    v_jets_tokens_.size(),
    std::vector<int>(cands->size(), -1)
  );

  //
  // Loop over each jet collection and select the jets
  //
  std::vector<std::vector<T>> v_v_jetsPassCut;
  v_v_jetsPassCut.reserve(v_jetsHandle.size());
  for (size_t iJC = 0; iJC < v_jetsHandle.size(); ++iJC) {
    std::vector<T> v_jetsPassCut;
    for (unsigned iJet = 0; iJet < v_jetsHandle[iJC]->size(); ++iJet) {
      const auto &jet = v_jetsHandle[iJC]->at(iJet);
      if(!v_jetCut_[iJC](jet)) continue;
      v_jetsPassCut.push_back(v_jetsHandle[iJC]->at(iJet));
    }
    v_v_jetsPassCut.push_back(v_jetsPassCut);
  }

  //
  // Loop over (ptr-)candidate collection
  //
  for (size_t iPtr = 0; iPtr < candPtrs.size(); ++iPtr) {
    auto candPtr = candPtrs[iPtr];
    //
    // Loop over each jet collection
    //
    for (size_t iJC = 0; iJC < v_v_jetsPassCut.size(); ++iJC) {;
      //
      // Loop over each jet in the collection
      //
      for (size_t jetIdx = 0; jetIdx < v_v_jetsPassCut[iJC].size(); ++jetIdx) {
        const auto &jet = v_v_jetsPassCut[iJC].at(jetIdx);
        //
        // Find candPtr in the jet constituents vector
        //
        std::vector<reco::CandidatePtr> const & daughters = jet.daughterPtrVector();
        auto candInJetConstVec = std::find( daughters.begin(), daughters.end(), candPtr );
        if ( candInJetConstVec != daughters.end() ) {
          v_v_jetIdxs[iJC][iPtr] = jetIdx;
        }
      }
    }
  }

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(cands->size(), name_, false, true);
  for (size_t iJC = 0; iJC < v_jetIdxNames_.size(); ++iJC) {
    candTable->addColumn<int>(v_jetIdxNames_[iJC]+"Idx", v_v_jetIdxs[iJC], v_jetIdxDocs_[iJC]);
  }
  iEvent.put(std::move(candTable), name_);
}

template< typename T>
void CandidateJetIdxExtTableProducer<T>::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("candidates", edm::InputTag("packedPFCandidates"));
  desc.add<std::string>("name", "PFCands");

  std::vector<edm::InputTag> emptyVInputTags;
  desc.add<std::vector<edm::InputTag>>("jetsV",emptyVInputTags);

  std::vector<std::string> emptyVStrings;
  desc.add<std::vector<std::string>>("jetIdxNamesV",emptyVStrings);
  desc.add<std::vector<std::string>>("jetIdxDocsV",emptyVStrings);
  desc.add<std::vector<std::string>>("jetCutV", emptyVStrings);

  descriptions.addWithDefaultLabel(desc);
}

typedef CandidateJetIdxExtTableProducer<pat::Jet> CandidatePatJetIdxExtTableProducer;
typedef CandidateJetIdxExtTableProducer<reco::GenJet> CandidateGenJetIdxExtTableProducer;

DEFINE_FWK_MODULE(CandidatePatJetIdxExtTableProducer);
DEFINE_FWK_MODULE(CandidateGenJetIdxExtTableProducer);
