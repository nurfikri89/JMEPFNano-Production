import FWCore.ParameterSet.Config as cms
from JMEPFNano.Production.skimForMC import SetupSkimForMC_AlwaysRunWeightsTable

#
# These should be unprescaled throughout Run-3
#
trigPathsDiMuon = [
  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*',
  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*'
]
trigPathsDiElectron = [
  'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*',
  'HLT_DoubleEle33_CaloIdL_MW_v*'
]

def SetupSkim_HLTDiMuon(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTDiMuonFilter = hlt.hltHighLevel.clone()
  process.HLTDiMuonFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTDiMuonFilter.HLTPaths = cms.vstring(trigPathsDiMuon)
  process.HLTDiMuonFilter.throw = cms.bool( False )
  process.skimHLTDiMuonSequence = cms.Sequence(process.HLTDiMuonFilter)
  process.SKIMHLTDiMuon = cms.Path(process.skimHLTDiMuonSequence)
  process.schedule.insert(0, process.SKIMHLTDiMuon)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiMuon'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiMuon'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process

def SetupSkim_HLTDiElectron(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTDiElectronFilter = hlt.hltHighLevel.clone()
  process.HLTDiElectronFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTDiElectronFilter.HLTPaths = cms.vstring(trigPathsDiElectron)
  process.HLTDiElectronFilter.throw = cms.bool( False )
  process.skimHLTDiElectronSequence = cms.Sequence(process.HLTDiElectronFilter)
  process.SKIMHLTDiElectron = cms.Path(process.skimHLTDiElectronSequence)
  process.schedule.insert(0, process.SKIMHLTDiElectron)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiElectron'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiElectron'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process

def SetupSkim_HLTDiLepton(process):
  import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
  process.HLTDiLeptonFilter = hlt.hltHighLevel.clone()
  process.HLTDiLeptonFilter.TriggerResultsTag = cms.InputTag( "TriggerResults", "", "HLT" )
  process.HLTDiLeptonFilter.HLTPaths = cms.vstring(trigPathsDiMuon+trigPathsDiElectron)
  process.HLTDiLeptonFilter.throw = cms.bool( False )
  process.skimHLTDiLeptonSequence = cms.Sequence(process.HLTDiLeptonFilter)
  process.SKIMHLTDiLepton = cms.Path(process.skimHLTDiLeptonSequence)
  process.schedule.insert(0, process.SKIMHLTDiLepton)
  if hasattr(process,"NANOEDMAODoutput") or hasattr(process,"NANOAODoutput"):
    process.NANOAODoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiLepton'))
  elif hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput"):
    process.NANOAODSIMoutput.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('SKIMHLTDiLepton'))
    process = SetupSkimForMC_AlwaysRunWeightsTable(process)

  return process
