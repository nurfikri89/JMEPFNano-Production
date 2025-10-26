#
# Compatible with NanoV15 and JMENanoV15. Tested with MiniAODv6 using CMSSW_15_0_14_patch4
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

from PhysicsTools.PatAlgos.tools.jetTools import setupPuppiForPackedPF

from JMEPFNano.Production.setupPFNanoV15 import PrepJetConstituents, PrepJetConstituentTables
from JMEPFNano.Production.setupPFNanoV15 import PrepGenJetConstituents, PrepGenJetConstituentTables
from JMEPFNano.Production.setupPFNanoV15 import ExtendGenVisTauTable

from PhysicsTools.NanoAOD.jetConstituents_cff import SaveAK4JetConstituents

def PrepPFNanoAOD(process, runOnMC,
  saveAK8=False, saveAK4=False, saveAK8Subjets=False,
  saveTau=False,saveElectron=False,savePhoton=False,saveMuon=False,
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
    doTau=saveTau,
    doElectron=saveElectron,
    doPhoton=savePhoton,
    doMuon=saveMuon
  )

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=saveOnlyPFCandsInJets,
    doAK8Puppi=saveAK8,
    doAK4Puppi=jetAK4Switch.doAK4Puppi and saveAK4,
    doAK4CHS=jetAK4Switch.doAK4CHS and saveAK4,
    doAK8PuppiSubjets=saveAK8Subjets,
    doTau=saveTau,
    doElectron=saveElectron, doPhoton=savePhoton, doMuon=saveMuon
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

def AddAllGenPartInNano(process):
  process.genParticleTable.src = "prunedGenParticles"
  return process

def AddCaloJets(process,runOnMC=False):
  from PhysicsTools.NanoAOD.common_cff import Var, P4Vars

  # process.jetCorrFactorsNanoAK4Calo = process.jetCorrFactorsNano.clone(
  #   src = "slimmedCaloJets",
  #   payload = "AK4Calo",
  # )
  # process.updatedJetsCalo = process.updatedJets.clone(
  #   jetSource = "slimmedCaloJets",
  #   jetCorrFactorsSource = ["jetCorrFactorsNanoAK4Calo"],
  # )
  # process.updatedJetsCaloWithUserData = cms.EDProducer("PATJetUserDataEmbedder",
  #   src = cms.InputTag("updatedJetsCalo"),
  #   userFloats = cms.PSet(),
  #   userInts = cms.PSet(),
  # )
  # process.finalJetsCalo = process.finalJets.clone(
  #   src = "updatedJetsCaloWithUserData",
  #   cut = ""
  # )

  CALOJETVARS = cms.PSet(P4Vars,
    area      = process.jetPuppiTable.variables.area,
    # rawFactor = process.jetPuppiTable.variables.rawFactor,
    hadEf       = Var("energyFractionHadronic()", float, doc = "energyFractionHadronic()", precision=12),
    # hadEInHO    = Var("hadEnergyInHO()", float, doc = "hadEnergyInHO()", precision=12),
    # hadEInHE    = Var("hadEnergyInHE()", float, doc = "hadEnergyInHE()", precision=12),
    # hadEInHF    = Var("hadEnergyInHF()", float, doc = "hadEnergyInHF()", precision=12),
    emEf        = Var("emEnergyFraction()", float, doc = "emEnergyFraction()", precision=12),
    # emEInEB     = Var("emEnergyInEB()", float, doc = "emEnergyInEB()", precision=12),
    # emEInEE     = Var("emEnergyInEE()", float, doc = "emEnergyInEE()", precision=12),
    # emEInHF     = Var("emEnergyInHF()", float, doc = "emEnergyInHF()", precision=12),
  )

  from PhysicsTools.NanoAOD.simpleCandidateFlatTableProducer_cfi import simpleCandidateFlatTableProducer
  process.jetCaloTable = simpleCandidateFlatTableProducer.clone(
    src = cms.InputTag("slimmedCaloJets"),
    cut = cms.string(""),
    name = cms.string("JetCalo"),
    doc  = cms.string("slimmedCaloJets"),
    variables = CALOJETVARS
  )
  process.jetCaloTable.variables.pt.precision=10
  process.jetCaloTable.variables.mass.precision=10
  # process.jetCaloTable.variables.rawFactor.precision=10

  # process.jetCaloMCTable = simpleCandidateFlatTableProducer.clone(
  #   src = process.jetCaloTable.src,
  #   name = process.jetCaloTable.name,
  #   extension = cms.bool(True), # this is an extension  table for the jets
  #   variables = cms.PSet(
  #     partonFlavour = Var("partonFlavour()", "int16", doc="flavour from parton matching"),
  #     hadronFlavour = Var("hadronFlavour()", "uint8", doc="flavour from hadron ghost clustering"),
  #   )
  # )

  process.jetCaloTask = cms.Task(
    # process.jetCorrFactorsNanoAK4Calo,process.updatedJetsCalo,
    # process.updatedJetsCaloWithUserData,process.finalJetsCalo,
    process.jetCaloTable
  )
  process.nanoTableTaskCommon.add(process.jetCaloTask)

  # process.jetCaloMCTask = cms.Task(
  #   process.jetCaloMCTable
  # )
  # if runOnMC:
  #   process.nanoTableTaskCommon.add(process.jetCaloMCTask)

  return process

def AugmentAK4PuppiJetsInNano(process):
  # process.finalJetsPuppi.cut = "pt > 10"
  # process.jetPuppiTable.doc = "slimmedJetsPuppi, i.e. ak4 PFJets Puppi with JECs applied, after basic selection (" + process.finalJetsPuppi.cut.value()+")"
  process.jetPuppiTable.variables.chMultiplicity    = Var("chargedMultiplicity()","uint8",doc="(Puppi-weighted) Number of charged particles in the jet")
  process.jetPuppiTable.variables.neMultiplicity    = Var("neutralMultiplicity()","uint8",doc="(Puppi-weighted) Number of neutral particles in the jet")
  process.jetPuppiTable.variables.chHadMultiplicity = Var("chargedHadronMultiplicity()","int16", doc="(Puppi-weighted) number of charged hadrons in the jet")
  process.jetPuppiTable.variables.neHadMultiplicity = Var("neutralHadronMultiplicity()","int16", doc="(Puppi-weighted) number of neutral hadrons in the jet")
  process.jetPuppiTable.variables.elMultiplicity    = Var("electronMultiplicity()", "int16", doc="(Puppi-weighted) number of electrons in the jet")
  process.jetPuppiTable.variables.phoMultiplicity   = Var("photonMultiplicity()", "int16", doc="(Puppi-weighted) number of photons in the jet")
  process.jetPuppiTable.variables.hfHadMultiplicity = Var("HFHadronMultiplicity()", "int16", doc="(Puppi-weighted) number of HF Hadrons in the jet")
  process.jetPuppiTable.variables.hfEMMultiplicity  = Var("HFEMMultiplicity()", "int16", doc="(Puppi-weighted) number of HF EMs in the jet")
  process.jetPuppiTable.variables.muMultiplicity    = Var("muonMultiplicity()", "int16", doc="(Puppi-weighted) number of muons in the jet")
  process.jetPuppiTable.variables.chHEF             = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision=15)
  process.jetPuppiTable.variables.neHEF             = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision=15)
  process.jetPuppiTable.variables.chEmEF            = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision=15)
  process.jetPuppiTable.variables.neEmEF            = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision=15)
  process.jetPuppiTable.variables.hfHEF             = Var("HFHadronEnergyFraction()",float, doc="hadronic Energy Fraction in HF",precision=15)
  process.jetPuppiTable.variables.hfEmEF            = Var("HFEMEnergyFraction()",float, doc="electromagnetic Energy Fraction in HF",precision=15)
  process.jetPuppiTable.variables.muEF              = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision=15)
  return process

def AddAK4CHSJetsInNano(process):
  process.nanoTableTaskCommon.add(process.jetTask)
  process.nanoTableTaskCommon.add(process.jetForMETTask)
  process.nanoTableTaskCommon.add(process.jetTablesTask)
  process.corrT1METJetTable.name = "CorrT1METJetCHS"
  # process.finalJets.cut = "pt > 10"
  # process.jetTable.doc = "slimmedJets, i.e. ak4 PFJets CHS with JECs applied, after basic selection (" + process.finalJets.cut.value()+")"
  process.jetTable.name = "JetCHS"
  process.jetTable.src = "finalJets"
  process.jetTable.externalVariables = cms.PSet()
  process.jetTable.variables.chMultiplicity    = Var("chargedMultiplicity()","uint8",doc="Number of charged particles in the jet")
  process.jetTable.variables.neMultiplicity    = Var("neutralMultiplicity()","uint8",doc="Number of neutral particles in the jet")
  process.jetTable.variables.chHadMultiplicity = Var("chargedHadronMultiplicity()","int16", doc="number of charged hadrons in the jet")
  process.jetTable.variables.neHadMultiplicity = Var("neutralHadronMultiplicity()","int16", doc="number of neutral hadrons in the jet")
  process.jetTable.variables.elMultiplicity    = Var("electronMultiplicity()", "int16", doc="number of electrons in the jet")
  process.jetTable.variables.phoMultiplicity   = Var("photonMultiplicity()", "int16", doc="number of photons in the jet")
  process.jetTable.variables.hfHadMultiplicity = Var("HFHadronMultiplicity()", "int16", doc="number of HF Hadrons in the jet")
  process.jetTable.variables.hfEMMultiplicity  = Var("HFEMMultiplicity()", "int16", doc="number of HF EMs in the jet")
  process.jetTable.variables.muMultiplicity    = Var("muonMultiplicity()", "int16", doc="number of muons in the jet")
  process.jetTable.variables.chHEF             = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision=15)
  process.jetTable.variables.neHEF             = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision=15)
  process.jetTable.variables.chEmEF            = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision=15)
  process.jetTable.variables.neEmEF            = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision=15)
  process.jetTable.variables.hfHEF             = Var("HFHadronEnergyFraction()",float, doc="hadronic Energy Fraction in HF",precision=15)
  process.jetTable.variables.hfEmEF            = Var("HFEMEnergyFraction()",float, doc="electromagnetic Energy Fraction in HF",precision=15)
  process.jetTable.variables.muEF              = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision=15)

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
  del process.jetTable.variables.btagDeepFlavB
  del process.jetTable.variables.btagDeepFlavCvB
  del process.jetTable.variables.btagDeepFlavCvL
  del process.jetTable.variables.btagDeepFlavQG
  process.jetCHSMCTable = process.jetMCTable.clone(
    name=process.jetTable.name,
    src=process.jetTable.src,
  )
  process.jetCHSMCTable.variables.genJetIdx = Var("?genJetFwdRef().backRef().isNonnull()?genJetFwdRef().backRef().key():-1", "int16", doc="index of matched gen jet")
  process.jeCHSMCTask = cms.Task(process.jetCHSMCTable)
  process.jetMCTask = process.jetMCTask.copyAndAdd(process.jeCHSMCTask)

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
    saveAK8Subjets=True,
    saveOnlyPFCandsInJets=True,
  )
  return process

def PrepPFNanoAOD_SavePFAndGenPartInJetsAK8AK4_MC(process):
  process = PrepPFNanoAOD(process,runOnMC=True,
    saveAK4=True,
    saveAK8=True,
    saveAK8Subjets=True,
    saveOnlyPFCandsInJets=True,
    saveGenPartCands=True,
    saveAK4Gen=True,
    saveAK8Gen=True,
    saveAK8GenSubjets=True,
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
