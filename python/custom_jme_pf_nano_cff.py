#
# Compatible with NanoV12 and JMENanoV12p5. Tested with MiniAODv4 using CMSSW_13_2_6_patch2
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data

from JMEPFNano.Production.setupPFNano import PrepJetConstituents, PrepJetConstituentTables
from JMEPFNano.Production.setupPFNano import PrepGenJetConstituents, PrepGenJetConstituentTables

def PrepJMEPFCustomNanoAOD(process, runOnMC,
  saveAK8Puppi=True,saveAK4Puppi=True,saveAK4CHS=True,saveAK8Subjets=False,
  saveOnlyPFCandsInJets=True,
  saveGenPartCands=False,
  saveAK8GEN=True, saveAK4Gen=True,saveAK8GenSubjets=False,
  saveOnlyGenCandsInJets=True):
  process.customizedJetCandsTask = cms.Task()
  process.schedule.associate(process.customizedJetCandsTask)

  ###################################
  #
  # Reco-jets and PF candidates
  #
  ###################################
  process, candInputForTable = PrepJetConstituents(
    process,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8Puppi,
    doAK4Puppi=saveAK4Puppi,
    doAK4CHS=saveAK4CHS,
    doAK8PuppiSubjets=saveAK8Subjets
  )

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8Puppi,
    doAK4Puppi=saveAK4Puppi,
    doAK4CHS=saveAK4CHS,
    doAK8PuppiSubjets=saveAK8Subjets
  )
  process.customPFConstituentsTable.variables.passCHS.expr = process.packedPFCandidateschs.cut.value()
  process.customPFConstituentsTable.variables.passCHS.doc = process.packedPFCandidateschs.cut.value()

  ###################################
  #
  # GenJets and Gen candidates
  #
  ###################################
  if runOnMC and saveGenPartCands:
    process, candInputForTable = PrepGenJetConstituents(
      process,
      saveOnlyGenCandsInJets=saveOnlyGenCandsInJets,
      doAK8=saveAK8GEN,
      doAK4=saveAK4Gen,
      doAK8Subjets=saveAK8Subjets,
    )

    process = PrepGenJetConstituentTables(
      process,
      candInputForTable,
      saveOnlyGenCandsInJets=saveOnlyGenCandsInJets,
      doAK8=saveAK8GEN,
      doAK4=saveAK4Gen,
      doAK8Subjets=saveAK8Subjets
    )
  return process

def PrepJMECustomNanoAOD_MC_Fixes(process):
  process = PrepJMECustomNanoAOD_MC(process)
  # Fix for NanAODv12_JMENano12p5. To be fixed in future JMENano
  process.jetMCTable.variables.genJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", "int16", doc="index of matched gen jet")
  # Undo this cut removal in future JMENano.
  process.genJetAK8Table.cut = "pt > 100." # Revert back to 100.
  process.genJetAK8FlavourTable.cut = process.genJetAK8Table.cut
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFInJets_Data(process):
  process = PrepJMECustomNanoAOD_Data(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=True
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=True
  )
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFAndGenPartInJets_Data(process):
  process = PrepJMECustomNanoAOD_Data(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAndGenPartInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True
  )
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFAll_Data(process):
  process = PrepJMECustomNanoAOD_Data(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAll_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=False
  )
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFAllAndGenPartInJets_MC(process):
  process = PrepJMECustomNanoAOD_Data(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True,
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAllAndGenPartInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True,
  )
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFAndGenPartAll_MC(process):
  process = PrepJMECustomNanoAOD_Data(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=False,
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAndGenPartAll_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=False,
  )
  return process
