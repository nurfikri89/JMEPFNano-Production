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

  edm::EDGetTokenT<reco::CandidateView>  pfcands_token_;
  const std::string name_;

  edm::EDGetTokenT<edm::ValueMap<float>> pfcands_weights_token_;
  const std::string weightName_;
  const std::string weightDoc_;
  const int weightPrecision_;
};

//
// constructors and destructor
//
PFCandidateExtTableProducer::PFCandidateExtTableProducer(const edm::ParameterSet &iConfig): 
  pfcands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcPFCandidates"))),
  name_(iConfig.getParameter<std::string>("name")),
  pfcands_weights_token_(consumes<edm::ValueMap<float>>(iConfig.getParameter<edm::InputTag>("srcWeights"))),
  weightName_(iConfig.getParameter<std::string>("weightName")),
  weightDoc_(iConfig.getParameter<std::string>("weightDoc")),
  weightPrecision_(iConfig.getParameter<int>("weightPrecision"))
{ 
  produces<nanoaod::FlatTable>(name_);
}

PFCandidateExtTableProducer::~PFCandidateExtTableProducer() {}

void PFCandidateExtTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {  
  
  //
  // Get packedPFCandidates
  //
  edm::Handle<reco::CandidateView> pfCands;
  iEvent.getByToken(pfcands_token_, pfCands);

  //
  // Get Weights Collection
  //
  edm::ValueMap<float> pfCands_weights;
  if (!pfcands_weights_token_.isUninitialized())
    pfCands_weights = iEvent.get(pfcands_weights_token_);

  //
  // Define output vectors to store in Table 
  //

  // consituent weights
  std::vector<float> weightsOutVec;
  weightsOutVec.reserve(pfCands->size());

  // fromPV(vertexRef)
  std::vector<int> fromPV_vertexRefOutVec;
  fromPV_vertexRefOutVec.reserve(pfCands->size());
  
  //
  // Loop over PF candidate collection
  //
  for (size_t i = 0; i < pfCands->size(); ++i) {
    reco::CandidatePtr candPtr = pfCands->ptrAt(i);
    const reco::Candidate* cand = candPtr.get();
    const pat::PackedCandidate* packedCand = dynamic_cast<const pat::PackedCandidate*>(cand);
    //
    // Store 
    //
    weightsOutVec.push_back(pfCands_weights[candPtr]);

    int fromPV_vertexRef = -1;
    if (packedCand->vertexRef().isNonnull())
      fromPV_vertexRef = packedCand->fromPV(packedCand->vertexRef().key());
    
    fromPV_vertexRefOutVec.push_back(fromPV_vertexRef);
  }    

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(pfCands->size(), name_, false, true);
  candTable->addColumn<float>(weightName_, weightsOutVec, weightDoc_, weightPrecision_);
  candTable->addColumn<int>("fromPVvertexRef", fromPV_vertexRefOutVec, "PV(vertexRef) (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)");
  iEvent.put(std::move(candTable), name_);
}

void PFCandidateExtTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("srcPFCandidates", edm::InputTag("finalJetsConstituents"));
  desc.add<std::string>("name", "PFCands");
  desc.add<edm::InputTag>("srcWeights", edm::InputTag("puppi"));
  desc.add<std::string>("weightName", "puppiWeightRecomputed");
  desc.add<std::string>("weightDoc", "Recomputed Puppi Weights");
  desc.add<int>("weightPrecision", -1);
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(PFCandidateExtTableProducer);