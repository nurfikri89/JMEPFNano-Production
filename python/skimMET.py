import FWCore.ParameterSet.Config as cms

def SetupSkimHLTMET(process):
  #Trigger bit requirement
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTMETFilter = hlt.hltHighLevel.clone()
  process.HLTMETFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTMETFilter.HLTPaths = cms.vstring(
    'HLT_PFMETNoMu*_PFMHTNoMu*_IDTight_FilterHF_v*',
    'HLT_PFMETNoMu*_PFMHTNoMu*_IDTight_v*',
  )
  process.skimHLTMETSequence = cms.Sequence(process.HLTMETFilter)
  process.SKIM_HLTMET = cms.Path(process.skimHLTMETSequence)

  return process