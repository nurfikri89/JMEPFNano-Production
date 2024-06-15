#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
typedef SimpleFlatTableProducer<pat::PackedCandidate> SimplePATPackedCandidateFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimplePATPackedCandidateFlatTableProducer);
