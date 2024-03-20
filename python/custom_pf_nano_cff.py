#
# Compatible with NanoV12 and JMENanoV12p5. Tested with MiniAODv4 using CMSSW_13_2_6_patch2
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

from PhysicsTools.PatAlgos.tools.jetTools import setupPuppiForPackedPF

from JMEPFNano.Production.setupPFNano import PrepJetConstituents, PrepJetConstituentTables
from JMEPFNano.Production.setupPFNano import SaveIsoChargedHadronPFCandidates
from JMEPFNano.Production.setupPFNano import PrepGenJetConstituents, PrepGenJetConstituentTables

def PrepPFNanoAOD(process, runOnMC,
  saveAK8=False,saveAK4=False,saveAK8Subjets=False, saveTau=False,
  saveOnlyPFCandsInJets=True,
  saveGenPartCands=False,
  saveAK8Gen=False,saveAK4Gen=False,saveAK8GenSubjets=False,
  saveOnlyGenCandsInJets=True, saveAK4BothPuppiAndCHS=False):
  process.customizedJetCandsTask = cms.Task()
  process.schedule.associate(process.customizedJetCandsTask)

  ###################################
  #
  # Reco-jets and PF candidates
  #
  ###################################
  packedPuppi, packedPuppiNoLep = setupPuppiForPackedPF(process)

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

  if saveAK4BothPuppiAndCHS:
    jetAK4Switch.doAK4Puppi=True
    jetAK4Switch.doAK4CHS=True

  process, candInputForTable = PrepJetConstituents(
    process,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8,
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4,
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4,
    doAK8PuppiSubjets=saveAK8Subjets,
    doTau=saveTau
  )

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8,
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4,
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4,
    doAK8PuppiSubjets=saveAK8Subjets,
    doTau=saveTau
  )

  ###################################
  #
  # GenJets and Gen candidates
  #
  ###################################
  if runOnMC and saveGenPartCands:
    process, candInputForTable = PrepGenJetConstituents(
      process,
      saveOnlyGenCandsInJets=saveOnlyGenCandsInJets,
      doAK8=saveAK8Gen,
      doAK4=saveAK4Gen,
      doAK8Subjets=saveAK8Subjets,
    )
    process = PrepGenJetConstituentTables(
      process,
      candInputForTable,
      saveOnlyGenCandsInJets=saveOnlyGenCandsInJets,
      doAK8=saveAK8Gen,
      doAK4=saveAK4Gen,
      doAK8Subjets=saveAK8Subjets
    )
  return process


def AddAK4CHSJetsInNano(process):
  process.nanoTableTaskCommon.add(process.jetTask)
  process.nanoTableTaskCommon.add(process.jetForMETTask)
  process.nanoTableTaskCommon.add(process.jetTablesTask)
  process.corrT1METJetTable.name = "CorrT1METJetCHS"
  process.jetTable.name = "JetCHS"
  process.jetTable.src = "finalJets"
  process.jetTable.externalVariables = cms.PSet()
  del process.updatedJetsWithUserData.userFloats.leadTrackPt
  del process.updatedJetsWithUserData.userFloats.leptonPtRelv0
  del process.updatedJetsWithUserData.userFloats.leptonPtRelInvv0
  del process.updatedJetsWithUserData.userFloats.leptonDeltaR
  del process.updatedJetsWithUserData.userFloats.vtxPt
  del process.updatedJetsWithUserData.userFloats.vtxMass
  del process.updatedJetsWithUserData.userFloats.vtx3dL
  del process.updatedJetsWithUserData.userFloats.vtx3deL
  del process.updatedJetsWithUserData.userInts.vtxNtrk
  del process.updatedJetsWithUserData.userInts.leptonPdgId
  del process.bjetNN
  del process.cjetNN
  del process.jetTable.variables.nElectrons
  del process.jetTable.variables.nMuons
  del process.jetTable.variables.nSVs
  del process.jetTable.variables.electronIdx1
  del process.jetTable.variables.electronIdx2
  del process.jetTable.variables.muonIdx1
  del process.jetTable.variables.muonIdx2
  del process.jetTable.variables.svIdx1
  del process.jetTable.variables.svIdx2
  process.jetCHSMCTable = process.jetMCTable.clone(
      name=process.jetTable.name,
      src=process.jetTable.src,
  )
  process.jeCHSMCTask = cms.Task(process.jetCHSMCTable)
  process.jetMCTask = process.jetMCTask.copyAndAdd(process.jeCHSMCTask)

  return process

def PrepNanoAOD_MC_Fixes(process):
  # Only for NanoAODv12
  process.jetMCTable.variables.genJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", "int16", doc="index of matched gen jet")
  return process

#####################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFInJetsAK8_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
  )
  return process

def PrepPFNanoAOD_SavePFInJetsAK8_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFInJetsAK8AK4_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK8=True,
    saveAK4=True,
    saveOnlyPFCandsInJets=True,
  )
  return process

def PrepPFNanoAOD_SavePFInJetsAK8AK4_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK8=True,
    saveAK4=True,
    saveOnlyPFCandsInJets=True,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFAndGenPartInJetsAK8_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
  )
  return process

def PrepPFNanoAOD_SavePFAndGenPartInJetsAK8_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFAndGenPartInJetsAK8AK4_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
  )
  return process

def PrepPFNanoAOD_SavePFAndGenPartInJetsAK8AK4_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFAll_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
  )
  return process

def PrepPFNanoAOD_SavePFAll_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFAllAndGenPartInJets_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
  )
  return process

def PrepPFNanoAOD_SavePFAllAndGenPartInJets_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
  )
  return process


######################################################################
#
#
#
######################################################################
def PrepPFNanoAOD_SavePFAllAndGenPartAll_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
  )
  return process

def PrepPFNanoAOD_SavePFAllAndGenPartAll_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=False,
  )
  return process
