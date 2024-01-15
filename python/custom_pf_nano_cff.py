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
  saveAK8=False,saveAK4=False,saveAK8Subjets=False,
  saveOnlyPFCandsInJets=True,
  saveGenPartCands=False,
  saveAK8Gen=False,saveAK4Gen=False,saveAK8GenSubjets=False,
  saveOnlyGenCandsInJets=True):
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

  process, candInputForTable = PrepJetConstituents(
    process,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8,
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4,
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4,
    doAK8PuppiSubjets=saveAK8Subjets
  )

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=True,
    doAK8Puppi=True,
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4,
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4,
    doAK8PuppiSubjets=saveAK8Subjets
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

######################################################################
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


def PrepPFNanoAOD_SavePFInJets_ChgHadIso_Data(process):
  process = PrepPFNanoAOD_SavePFInJetsAK8AK4_Data(process)
  process = SaveIsoChargedHadronPFCandidates(process)
  return process

def PrepPFNanoAOD_SavePFInJets_ChgHadIso_MC(process):
  process = PrepPFNanoAOD_SavePFInJetsAK8AK4_MC(process)
  process = SaveIsoChargedHadronPFCandidates(process)
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
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
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
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=True,
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
def PrepPFNanoAOD_SavePFAndGenPartAll_Data(process):
  process = PrepPFNanoAOD(process,runOnMC=False,
    saveAK4=True,
    saveAK8=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveOnlyGenCandsInJets=False,
  )
  return process

def PrepPFNanoAOD_SavePFAndGenPartAll_MC(process):
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
