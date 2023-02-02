#
# Compatible with NanoV11 (CMSSW_12_6_0_patch1). Tested on Run3Summer22MiniAODv3 (CMSSSW_12_4_11_patch3) samples 
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepPuppiProducer
from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJetConstituents
from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJetConstituentTables

def PrepPFNanoAOD(process, runOnMC, saveAK4=True, saveOnlyPFCandsInJets=True):
  process.customizedPFCandsTask = cms.Task()
  process.schedule.associate(process.customizedPFCandsTask)

  process = PrepPuppiProducer(process)

  #
  # Switch from Run-3 to Run-2 default jet collection
  #
  jetAK4Switch = cms.PSet(
    doAK4Puppi = cms.untracked.bool(True),
    doAK4CHS = cms.untracked.bool(False),
  )

  run2_nanoAOD_ANY.toModify(jetAK4Switch, 
    doAK4Puppi = cms.untracked.bool(False),
    doAK4CHS = cms.untracked.bool(True)
  )

  if saveOnlyPFCandsInJets:
    process, candList = PrepJetConstituents(
      process,
      doAK8Puppi=True, 
      doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4, 
      doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4
    )
    process.finalJetsConstituents = cms.EDProducer("PackedCandidatePtrMerger", 
      src = candList, 
      skipNulls = cms.bool(True), 
      warnOnSkip = cms.bool(True)
    )
    process.customizedPFCandsTask.add(process.finalJetsConstituents)
    candInputForTable = cms.InputTag("finalJetsConstituents")
  else:
    # NOTE: Store all packedPFCandidates
    candInputForTable = cms.InputTag("packedPFCandidates")
  
  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=True,
    doAK8Puppi=True, 
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4, 
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4
  )

  if not(saveOnlyPFCandsInJets):
    process.customPFConstituentsTable.doc = "PF Candidates"

  return process

def PrepPFNanoAOD_MC(process):
  PrepPFNanoAOD(process,runOnMC=True)
  return process

def PrepPFNanoAOD_Data(process):
  PrepPFNanoAOD(process,runOnMC=False)
  return process

def PrepPFNanoAOD_SavePFAK8Only_MC(process):
  PrepPFNanoAOD(process,runOnMC=True,saveAK4=False)
  return process

def PrepPFNanoAOD_SavePFAK8Only_Data(process):
  PrepPFNanoAOD(process,runOnMC=False,saveAK4=False)
  return process

def PrepPFNanoAOD_SavePFAll_MC(process):
  PrepPFNanoAOD(process,runOnMC=True,saveAK4=True,saveOnlyPFCandsInJets=False)
  return process

def PrepPFNanoAOD_SavePFAll_Data(process):
  PrepPFNanoAOD(process,runOnMC=False,saveAK4=True,saveOnlyPFCandsInJets=False)
  return process
