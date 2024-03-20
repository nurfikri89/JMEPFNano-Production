#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Utilities/interface/transform.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

class PFCandidateExtTableProducerV2 : public edm::stream::EDProducer<> {
public:
  explicit PFCandidateExtTableProducerV2(const edm::ParameterSet &);
  ~PFCandidateExtTableProducerV2() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  edm::EDGetTokenT<reco::CandidateView>  pfcands_token_;
  const std::string name_;
  const bool saveFromPVvertexRef_;
  const int weightPrecision_;

  std::vector<edm::EDGetTokenT<edm::ValueMap<float>>> v_pfcands_weights_tokens_;
  std::vector<std::string> v_weightNames_;
  std::vector<std::string> v_weightDocs_;
};

//
// constructors and destructor
//
PFCandidateExtTableProducerV2::PFCandidateExtTableProducerV2(const edm::ParameterSet &iConfig):
  pfcands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcPFCandidates"))),
  name_(iConfig.getParameter<std::string>("name")),
  saveFromPVvertexRef_(iConfig.getParameter<bool>("saveFromPVvertexRef")),
  weightPrecision_(iConfig.getParameter<int>("weightPrecision"))
{
  v_pfcands_weights_tokens_ = edm::vector_transform(
    iConfig.getParameter<std::vector<edm::InputTag>>("srcWeightsV"),
    [this](edm::InputTag const& tag) {return consumes<edm::ValueMap<float>>(tag);}
  );
  v_weightNames_ = iConfig.getParameter<std::vector<std::string>>("weightNamesV");
  v_weightDocs_ = iConfig.getParameter<std::vector<std::string>>("weightDocsV");

  produces<nanoaod::FlatTable>(name_);
}

PFCandidateExtTableProducerV2::~PFCandidateExtTableProducerV2() {}

void PFCandidateExtTableProducerV2::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {

  //
  // Retrieve pf candidates
  //
  edm::Handle<reco::CandidateView> pfCands;
  iEvent.getByToken(pfcands_token_, pfCands);

  //
  //
  //
  std::vector<edm::ValueMap<float>> v_pfcands_weights;
  for (size_t i = 0; i < v_pfcands_weights_tokens_.size(); ++i) {
    v_pfcands_weights.push_back(iEvent.get(v_pfcands_weights_tokens_[i]));
  }

  //
  //
  //
  std::vector<edm::Ptr<reco::Candidate>> candPtrs;
  candPtrs.reserve(pfCands->size());
  for (size_t iCand = 0; iCand < pfCands->size(); ++iCand) {
    candPtrs.push_back(pfCands->ptrAt(iCand));
  }

  //
  //
  //
  std::vector<std::vector<float>> v_v_weightsOut;
  v_v_weightsOut.reserve(v_pfcands_weights.size());
  for (size_t iW = 0; iW < v_pfcands_weights.size(); ++iW) {
    std::vector<float> weightsOut;
    weightsOut.reserve(pfCands->size());
    v_v_weightsOut.push_back(weightsOut);
  }

  std::vector<int> fromPV_vertexRefOutVec;
  fromPV_vertexRefOutVec.reserve(pfCands->size());

  //
  // Loop over ptr-candidate collection
  //
  for (size_t iPtr = 0; iPtr < candPtrs.size(); ++iPtr) {
    auto candPtr = candPtrs[iPtr];


    //
    // For each ptr-candidate collection, save all
    //
    for (size_t iW = 0; iW < v_pfcands_weights.size(); ++iW) {
      v_v_weightsOut[iW].push_back(v_pfcands_weights[iW][candPtr]);
    }
    //
    //
    //
    const reco::Candidate* cand = candPtr.get();
    const pat::PackedCandidate* packedCand = dynamic_cast<const pat::PackedCandidate*>(cand);

    if(saveFromPVvertexRef_){
      int fromPV_vertexRef = -1;
      if (packedCand->vertexRef().isNonnull())
        fromPV_vertexRef = packedCand->fromPV(packedCand->vertexRef().key());
      fromPV_vertexRefOutVec.push_back(fromPV_vertexRef);
    }
  }

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(pfCands->size(), name_, false, true);
  for (size_t iW = 0; iW < v_pfcands_weights.size(); ++iW) {
    candTable->addColumn<float>(v_weightNames_[iW], v_v_weightsOut[iW], v_weightDocs_[iW], weightPrecision_);
  }
  if (saveFromPVvertexRef_){
    candTable->addColumn<int>("fromPVvertexRef", fromPV_vertexRefOutVec, "PV(vertexRef) (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)");
  }
  iEvent.put(std::move(candTable), name_);
}

void PFCandidateExtTableProducerV2::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("srcPFCandidates", edm::InputTag("finalJetsConstituents"));
  desc.add<std::string>("name", "PFCands");
  desc.add<bool>("saveFromPVvertexRef", false);
  desc.add<int>("weightPrecision", -1);

  std::vector<edm::InputTag> emptyVInputTags;
  desc.add<std::vector<edm::InputTag>>("srcWeightsV",emptyVInputTags);

  std::vector<std::string> emptyVStrings;
  desc.add<std::vector<std::string>>("weightNamesV",emptyVStrings);
  desc.add<std::vector<std::string>>("weightDocsV",emptyVStrings);

  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(PFCandidateExtTableProducerV2);