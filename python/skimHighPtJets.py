import FWCore.ParameterSet.Config as cms

def ApplySkimHighPtJets(process):
  ######################################################################
  #
  #
  #
  ######################################################################
  process.highPtJetsSlimmedJetsPuppi = cms.EDFilter("CandViewRefSelector",
    src = cms.InputTag("slimmedJetsPuppi"),
    cut = cms.string("pt > 200 && abs(eta) < 5.0")
  )

  process.highPtSlimmedJetsPuppiCountFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("highPtJetsSlimmedJetsPuppi"),
    minNumber = cms.uint32(1)
  )

  process.highPtSlimmedJetsPuppiSequence = cms.Sequence(process.highPtJetsSlimmedJetsPuppi * process.highPtSlimmedJetsPuppiCountFilter)
  process.highPtSlimmedJetsPuppiPath = cms.Path( process.highPtSlimmedJetsPuppiSequence )
  ######################################################################
  #
  #
  #
  ######################################################################
  process.highPtJetsUpdatedJetsPuppi = cms.EDFilter("CandViewRefSelector",
    src = cms.InputTag("updatedJetsPuppi"), # Defined in jetsAK4_Puppi_cff.py
    cut = cms.string("pt > 800 && abs(eta) < 5.0")
  )

  process.highPtUpdatedJetsPuppiCountFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("highPtJetsUpdatedJetsPuppi"),
    minNumber = cms.uint32(1)
  )

  process.highPtUpdatedJetsPuppiSequence = cms.Sequence(process.highPtJetsUpdatedJetsPuppi * process.highPtUpdatedJetsPuppiCountFilter)
  process.highPtUpdatedJetsPuppiPath = cms.Path( process.highPtUpdatedJetsPuppiSequence )

  return process