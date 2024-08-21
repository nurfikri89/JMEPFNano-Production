#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
typedef SimpleFlatTableProducer<pat::PackedCandidate> SimplePATPackedCandidateFlatTableProducer;

#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
typedef SimpleFlatTableProducer<pat::PackedGenParticle> SimplePATPackedGenParticleFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimplePATPackedCandidateFlatTableProducer);
DEFINE_FWK_MODULE(SimplePATPackedGenParticleFlatTableProducer);
