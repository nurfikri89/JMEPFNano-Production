#
# Compatible with NanoV12 and JMENanoV12p5. Tested with MiniAODv4 using CMSSW_13_2_6_patch2
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

# from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data
# Use this and comment out above if use >= CMSSW_14_0_6_patch1
from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD

from JMEPFNano.Production.setupPFNano import PrepJetConstituents, PrepJetConstituentTables
from JMEPFNano.Production.setupPFNano import PrepGenJetConstituents, PrepGenJetConstituentTables

def PrepJMEPFCustomNanoAOD(process, runOnMC,
  saveAK8Puppi=True,saveAK4Puppi=True,saveAK4CHS=True,saveAK8Subjets=False,
  saveTau=False,saveElectron=False,savePhoton=False,saveMuon=False,
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
    doAK8PuppiSubjets=saveAK8Subjets,
    doTau=saveTau,
    doElectron=saveElectron, doPhoton=savePhoton, doMuon=saveMuon
  )

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8Puppi,
    doAK4Puppi=saveAK4Puppi,
    doAK4CHS=saveAK4CHS,
    doAK8PuppiSubjets=saveAK8Subjets,
    doTau=saveTau,
    doElectron=saveElectron, doPhoton=savePhoton, doMuon=saveMuon
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


def PrepJMECustomNanoAOD_Common_Extra(process):
  from PhysicsTools.NanoAOD.custom_jme_cff import QGLVARS
  process.updatedJetsWithUserData.userFloats.qgl_axis2 = cms.InputTag("qgtagger:axis2")
  process.updatedJetsWithUserData.userFloats.qgl_ptD   = cms.InputTag("qgtagger:ptD")
  process.updatedJetsWithUserData.userInts.qgl_mult    = cms.InputTag("qgtagger:mult")
  # Save quark gluon likelihood input variables variables
  process.jetTable.variables.qgl_axis2 =  QGLVARS.qgl_axis2
  process.jetTable.variables.qgl_ptD   =  QGLVARS.qgl_ptD
  process.jetTable.variables.qgl_mult  =  QGLVARS.qgl_mult
  #
  process.jetTable.variables.chHEF.precision=-1
  process.jetTable.variables.neHEF.precision=-1
  process.jetTable.variables.chEmEF.precision=-1
  process.jetTable.variables.neEmEF.precision=-1
  process.jetTable.variables.hfHEF.precision=-1
  process.jetTable.variables.hfEmEF.precision=-1
  process.jetTable.variables.muEF.precision=-1
  #
  if hasattr(process,"jetTableCHS"):
    process.jetTableCHS.variables.chHEF.precision=-1
    process.jetTableCHS.variables.neHEF.precision=-1
    process.jetTableCHS.variables.chEmEF.precision=-1
    process.jetTableCHS.variables.neEmEF.precision=-1
    process.jetTableCHS.variables.hfHEF.precision=-1
    process.jetTableCHS.variables.hfEmEF.precision=-1
    process.jetTableCHS.variables.muEF.precision=-1

  return process

def PrepJMECustomNanoAOD_Data_Fixes(process):
  process = PrepJMECustomNanoAOD_Data(process)
  # Use this and comment out above if use >= CMSSW_14_0_6_patch1
  # process = PrepJMECustomNanoAOD(process)

  return process

def PrepJMECustomNanoAOD_MC_Fixes(process):
  process = PrepJMECustomNanoAOD_MC(process)
  # Use this and comment out above if use >= CMSSW_14_0_6_patch1
  # process = PrepJMECustomNanoAOD(process)

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
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=True
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
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
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAndGenPartInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
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
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAll_MC(process):
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=False
  )
  return process

######################################################################
#
#
#
######################################################################
def PrepJMEPFCustomNanoAOD_SavePFAllAndGenPartInJets_Data(process):
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=True,
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAllAndGenPartInJets_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
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
def PrepJMEPFCustomNanoAOD_SavePFAndGenPartAll_Data(process):
  process = PrepJMECustomNanoAOD_Data_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=False,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=False,
  )
  return process

def PrepJMEPFCustomNanoAOD_SavePFAndGenPartAll_MC(process):
  process = PrepJMECustomNanoAOD_MC_Fixes(process)
  process = PrepJMECustomNanoAOD_Common_Extra(process)
  process = PrepJMEPFCustomNanoAOD(process,runOnMC=True,
    saveOnlyPFCandsInJets=False,
    saveGenPartCands=True,
    saveOnlyGenCandsInJets=False,
  )
  return process
