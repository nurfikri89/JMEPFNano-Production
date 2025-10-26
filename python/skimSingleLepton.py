import FWCore.ParameterSet.Config as cms
from JMEPFNano.Production.skimForMC import SetupSkimForMC_AlwaysRunWeightsTable

#
# These should be unprescaled throughout Run-3
#
trigPathsSingleMuon = [
  'HLT_IsoMu24_v*',
  'HLT_Mu50_v*',
  'HLT_HighPtTkMu100_v*',
  'HLT_CascadeMu100_v*'
]
trigPathsSingleElectron = [
  'HLT_Ele30_WPTight_Gsf_v*',
  'HLT_Ele115_CaloIdVT_GsfTrkIdT_v*',
  'HLT_Photon200_v*',
  'HLT_Photon300_NoHE_v*',
]

def SetupSkim_HLTSingleMuon(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTSingleMuonFilter = hlt.hltHighLevel.clone()
  process.HLTSingleMuonFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTSingleMuonFilter.HLTPaths = cms.vstring(trigPathsSingleMuon)
  process.HLTSingleMuonFilter.throw = cms.bool( False )
  process.skimHLTSingleMuonSequence = cms.Sequence(process.HLTSingleMuonFilter)
  process.SKIMHLTSingleMuon = cms.Path(process.skimHLTSingleMuonSequence)
  process.schedule.insert(0, process.SKIMHLTSingleMuon)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleMuon'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleMuon'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process

def SetupSkim_HLTSingleElectron(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTSingleElectronFilter = hlt.hltHighLevel.clone()
  process.HLTSingleElectronFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTSingleElectronFilter.HLTPaths = cms.vstring(trigPathsSingleElectron)
  process.HLTSingleElectronFilter.throw = cms.bool( False )
  process.skimHLTSingleElectronSequence = cms.Sequence(process.HLTSingleElectronFilter)
  process.SKIMHLTSingleElectron = cms.Path(process.skimHLTSingleElectronSequence)
  process.schedule.insert(0, process.SKIMHLTSingleElectron)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleElectron'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleElectron'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process

def SetupSkim_HLTSingleLepton(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTSingleLeptonFilter = hlt.hltHighLevel.clone()
  process.HLTSingleLeptonFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTSingleLeptonFilter.HLTPaths = cms.vstring(trigPathsSingleMuon+trigPathsSingleElectron)
  process.HLTSingleLeptonFilter.throw = cms.bool( False )
  process.skimHLTSingleLeptonSequence = cms.Sequence(process.HLTSingleLeptonFilter)
  process.SKIMHLTSingleLepton = cms.Path(process.skimHLTSingleLeptonSequence)
  process.schedule.insert(0, process.SKIMHLTSingleLepton)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleLepton'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTSingleLepton'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process
