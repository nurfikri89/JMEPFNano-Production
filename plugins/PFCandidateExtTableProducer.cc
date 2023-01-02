#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

class PFCandidateExtTableProducer : public edm::stream::EDProducer<> {
public:
  explicit PFCandidateExtTableProducer(const edm::ParameterSet &);
  ~PFCandidateExtTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  void produce(edm::Event &, const edm::EventSetup &) override;

  const std::string name_;
  const std::string weightName_;
  const std::string weightDoc_;

  // edm::EDGetTokenT<reco::CandidateView> packedPFCands_token_;
  edm::EDGetTokenT<reco::CandidateView> finalPFCands_token_;
  edm::EDGetTokenT<edm::ValueMap<float>> input_weights_token_;
  
  edm::ValueMap<float> weights_;
};

//
// constructors and destructor
//
PFCandidateExtTableProducer::PFCandidateExtTableProducer(const edm::ParameterSet &iConfig): 
  name_(iConfig.getParameter<std::string>("name")),
  weightName_(iConfig.getParameter<std::string>("weightName")),
  weightDoc_(iConfig.getParameter<std::string>("weightDoc")),
  finalPFCands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("finalPFCandidates"))),
  input_weights_token_(consumes<edm::ValueMap<float>>(iConfig.getParameter<edm::InputTag>("srcWeights")))
{ 
  produces<nanoaod::FlatTable>(name_);
}

PFCandidateExtTableProducer::~PFCandidateExtTableProducer() {}

void PFCandidateExtTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {  
  //
  //
  //
  edm::Handle<reco::CandidateView> finalPFcands;
  iEvent.getByToken(finalPFCands_token_, finalPFcands);
  //
  // Get Weights Collection
  //
  if (!input_weights_token_.isUninitialized())
    weights_ = iEvent.get(input_weights_token_);
  //
  //
  //
  std::vector<edm::Ptr<reco::Candidate>> candPtrs;   
  candPtrs.reserve(finalPFcands->size());  
  for (size_t i = 0; i < finalPFcands->size(); ++i) {
    candPtrs.push_back(finalPFcands->ptrAt(i));
  }    
  //
  // 
  //
  std::vector<float> weightsOut;
  weightsOut.reserve(finalPFcands->size());
  //
  //
  //
  auto inBegin = candPtrs.begin(); 
  auto inEnd = candPtrs.end(); 
  auto i = inBegin;
  for (; i != inEnd; ++i) {
    float w = weights_[*i];
    weightsOut.push_back(w);
  }

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(finalPFcands->size(), name_, false, true);
  candTable->addColumn<float>(weightName_, weightsOut, weightDoc_, nanoaod::FlatTable::FloatColumn);
  iEvent.put(std::move(candTable), name_);
}

void PFCandidateExtTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "PFCands");
  desc.add<std::string>("weightName", "puppiWeightRecomputed");
  desc.add<std::string>("weightDoc", "Recomputed Puppi Weights");
  desc.add<edm::InputTag>("finalPFCandidates", edm::InputTag("finalJetsConstituents"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(PFCandidateExtTableProducer);