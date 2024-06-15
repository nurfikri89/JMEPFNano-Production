#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/JetReco/interface/CaloJet.h"
typedef SimpleFlatTableProducer<reco::CaloJet> SimpleRecoCaloJetFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleRecoCaloJetFlatTableProducer);
