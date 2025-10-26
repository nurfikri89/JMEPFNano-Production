import FWCore.ParameterSet.Config as cms

def SetupSkimForMC_AlwaysRunWeightsTable(process):
  process.genWeightsTableSequence = cms.Sequence(process.genWeightsTable)
  process.genWeightsTablePath = cms.Path(process.genWeightsTableSequence)
  process.schedule.insert(0, process.genWeightsTablePath)

  return process
