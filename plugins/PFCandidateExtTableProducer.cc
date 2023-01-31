#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/Vertex.h"

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
  float computedZ0ForPuIdVarBeta(const pat::PackedCandidate*, const reco::Vertex*, const reco::VertexCollection&);
  
  const edm::EDGetTokenT<reco::CandidateView> pfcands_token_;
  const edm::EDGetTokenT<reco::VertexCollection> primaryvertices_token_;
  const std::string name_;

  const edm::EDGetTokenT<edm::ValueMap<float>> pfcands_weights_token_;
  const std::string weightName_;
  const std::string weightDoc_;
  const int weightPrecision_;
};

//
// constructors and destructor
//
PFCandidateExtTableProducer::PFCandidateExtTableProducer(const edm::ParameterSet &iConfig): 
  pfcands_token_(consumes<reco::CandidateView>(iConfig.getParameter<edm::InputTag>("srcPFCandidates"))),
  primaryvertices_token_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("srcPrimaryVertices"))),
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
  // Get offlineSlimmedPrimaryVertices
  //
  edm::Handle<reco::VertexCollection> primaryVertices;
  const reco::VertexCollection* vertexes = nullptr;
  reco::VertexCollection::const_iterator vtx;


  bool calcPuIdVarBeta=true;
  if (calcPuIdVarBeta){
    //
    // https://github.com/cms-sw/cmssw/blob/CMSSW_12_6_0_patch1/RecoJets/JetProducers/plugins/PileupJetIdProducer.cc#L100-L113
    //
    iEvent.getByToken(primaryvertices_token_, primaryVertices);
    vertexes = primaryVertices.product();
    vtx = vertexes->begin();
    while (vtx != vertexes->end() && (vtx->isFake() || vtx->ndof() < 4)) {
      ++vtx;
    }
    if (vtx == vertexes->end()) {
      vtx = vertexes->begin();
    }
  }

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

  // dZ0ForPuIdVarBetaVec
  std::vector<float> dZ0ForPuIdVarBetaVec;
  dZ0ForPuIdVarBetaVec.reserve(pfCands->size());
  
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
    //
    //
    //
    int fromPV_vertexRef = -1;
    if (packedCand->vertexRef().isNonnull())
      fromPV_vertexRef = packedCand->fromPV(packedCand->vertexRef().key());
    fromPV_vertexRefOutVec.push_back(fromPV_vertexRef);
    //
    //
    //
    float dZ0ForPuIdVarBeta = -99.;
    if (calcPuIdVarBeta and cand->charge() != 0) {
      dZ0ForPuIdVarBeta = computedZ0ForPuIdVarBeta(packedCand, &(*vtx), *vertexes);
    }
    dZ0ForPuIdVarBetaVec.push_back(dZ0ForPuIdVarBeta);
  }    

  //
  //
  //
  auto candTable = std::make_unique<nanoaod::FlatTable>(pfCands->size(), name_, false, true);
  candTable->addColumn<float>(weightName_, weightsOutVec, weightDoc_, weightPrecision_);
  candTable->addColumn<int>("fromPVvertexRef", fromPV_vertexRefOutVec, "PV(vertexRef) (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)");
  if (calcPuIdVarBeta){
    candTable->addColumn<float>("dZ0ForPuIdVarBeta", dZ0ForPuIdVarBetaVec, "dZ0 (For PuId Variable Beta)", 15);
  }
  iEvent.put(std::move(candTable), name_);
}
//
// https://github.com/cms-sw/cmssw/blob/CMSSW_12_6_0_patch1/RecoJets/JetProducers/src/PileupJetIdAlgo.cc#L487-L524
//
float PFCandidateExtTableProducer::computedZ0ForPuIdVarBeta(
  const pat::PackedCandidate* lPack, const reco::Vertex* vtx, const reco::VertexCollection& allvtx
){
  // bool inVtx0 = false;
  // bool inVtxOther = false;
  float dZ0 = 9999.f;

  for (unsigned vtx_i = 0; vtx_i < allvtx.size(); vtx_i++) {
    auto iv = allvtx[vtx_i];
    if (iv.isFake())
      continue;

    // Match to vertex in case of copy as above
    bool isVtx0 = (iv.position() - vtx->position()).r() < 0.02;

    if (isVtx0) {
      // if (lPack->fromPV(vtx_i) == pat::PackedCandidate::PVUsedInFit)
      //   inVtx0 = true;
      // if (lPack->fromPV(vtx_i) == 0)
      //   inVtxOther = true;
      dZ0 = lPack->dz(iv.position());
    }
  }
  return dZ0;
}

void PFCandidateExtTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("srcPFCandidates", edm::InputTag("finalJetsConstituents"));
  desc.add<edm::InputTag>("srcPrimaryVertices", edm::InputTag("offlineSlimmedPrimaryVertices"));
  desc.add<std::string>("name", "PFCands");
  desc.add<edm::InputTag>("srcWeights", edm::InputTag("puppi"));
  desc.add<std::string>("weightName", "puppiWeightRecomputed");
  desc.add<std::string>("weightDoc", "Recomputed Puppi Weights");
  desc.add<int>("weightPrecision", -1);
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(PFCandidateExtTableProducer);