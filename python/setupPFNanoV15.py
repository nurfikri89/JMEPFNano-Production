#
# Compatible with NanoV15 and JMENanoV12p5. Tested with MiniAODv6 using CMSSW_15_0_15_patch4
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars

from CommonTools.PileupAlgos.Puppi_cff import puppi
from CommonTools.ParticleFlow.pfCHS_cff import pfCHS

from PhysicsTools.PatAlgos.tools.jetTools import setupPuppiForPackedPF
from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask, addToProcessAndTask

def addProcessAndTask(proc, label, module):
  task = getPatAlgosToolsTask(proc)
  addToProcessAndTask(label, module, proc, task)

#####################################################################
#
#
#
######################################################################
def PrepJetConstituents(process, saveOnlyPFCandsInJets,
  doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=False,
  doTau=False, doElectron=False, doPhoton=False, doMuon=False):

  if saveOnlyPFCandsInJets:
    #################################################################
    # Collect pointers to candidates from different jet collections
    # and merge them into one list
    #################################################################
    candList = cms.VInputTag()

    if doAK8Puppi:
      # Collect AK8 Puppi Constituents pointers
      process.finalJetsAK8ConstituentsPFNano = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJetsAK8"),
        cut = cms.string("abs(eta) <= 2.5") # Store PF candidates for central jets in finalJetsAK8
      )
      process.customizedJetCandsTask.add(process.finalJetsAK8ConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK8ConstituentsPFNano", "constituents"))

    if doAK4Puppi:
      # Collect AK4 Puppi Constituents pointers
      process.finalJetsAK4PuppiConstituentsPFNano = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJetsPuppi"),
        cut = cms.string("") # Store all PF candidates for all jets in finalJetsPuppi
      )
      process.customizedJetCandsTask.add(process.finalJetsAK4PuppiConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK4PuppiConstituentsPFNano", "constituents"))

    if doAK4CHS:
      # Collect AK4 CHS Constituents pointers
      process.finalJetsAK4CHSConstituentsPFNano = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJets"),
        cut = cms.string("") # Store all PF candidates for all jets in finalJets
      )
      process.customizedJetCandsTask.add(process.finalJetsAK4CHSConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK4CHSConstituentsPFNano", "constituents"))

    if doAK8PuppiSubjets:
      # Collect AK8 Puppi Subjets Constituents pointers
      process.finalJetsAK8SubjetConstituentsPFNano = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
        cut = cms.string("") # Store all PF candidates for all subjets
      )
      process.customizedJetCandsTask.add(process.finalJetsAK8SubjetConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK8SubjetConstituentsPFNano", "constituents"))

    if doTau:
      # Collect Tau signalCands and isolationCands
      process.finalTausConstituentsPFNano = cms.EDProducer("PatTauConstituentSelector",
        src = cms.InputTag("finalTaus"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalTausConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalTausConstituentsPFNano", "constituents"))

    if doElectron:
      process.finalElectronsPFCandConstituentsPFNano = cms.EDProducer("PatElectronPFCandSelector",
        src = cms.InputTag("finalElectrons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalElectronsPFCandConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalElectronsPFCandConstituentsPFNano", "constituents"))

    if doPhoton:
      process.finalPhotonsPFCandConstituentsPFNano = cms.EDProducer("PatPhotonPFCandSelector",
        src = cms.InputTag("finalPhotons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalPhotonsPFCandConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalPhotonsPFCandConstituentsPFNano", "constituents"))

    if doMuon:
      process.finalMuonsPFCandConstituentsPFNano = cms.EDProducer("PatMuonPFCandSelector",
        src = cms.InputTag("finalMuons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalMuonsPFCandConstituentsPFNano)
      candList += cms.VInputTag(cms.InputTag("finalMuonsPFCandConstituentsPFNano", "constituents"))

    #
    # Merge all candidate pointers
    #
    process.finalJetsConstituentsPFNano = cms.EDProducer("PackedCandidatePtrMerger",
      src = candList,
      skipNulls = cms.bool(True),
      warnOnSkip = cms.bool(True)
    )
    process.customizedJetCandsTask.add(process.finalJetsConstituentsPFNano)
    #
    # Collection to give to candidate table
    #
    candInputForTable = cms.InputTag("finalJetsConstituentsPFNano")
  else:
    ###################################
    # Store all packedPFCandidates
    ###################################
    #
    # Collection to give to candidate table
    #
    candInputForTable = cms.InputTag("packedPFCandidates")

  return process, candInputForTable

#########################################################################################################################################################
def SaveChargedHadronPFCandidates(process, ptcut="5", applyCHS=False, applyIso=False, runOnMC=False):

  pfChargedHadName = "pfChargedHadronSelected"
  pfChargedHadTableName = "customPFChargedHadronCandidateTable"
  pfChargedHadExtTableName = "customPFChargedHadronCandidateExtTable"
  cutStr    = f"(abs(pdgId()) == 211 && (pt >= {ptcut}))"
  tableName = "SelectedChHadPFCandV2"
  tableDoc  = f"Charged Hadron PF candidates. Selection: pt >= {ptcut}"
  if applyCHS:
    cutStr    += f" && ({pfCHS.cut.value()})"
    tableDoc  = tableDoc + ", pass CHS"
  if applyIso:
    cutStr    += f" && (isIsolatedChargedHadron())"
    tableDoc  = tableDoc + ", isIsolatedChargedHadron()"

  setattr(process, pfChargedHadName, cms.EDProducer("PackedCandidatePtrSelector",
      src = cms.InputTag("packedPFCandidates"),
      cut = cms.string(cutStr),
    )
  )
  if hasattr(process,"finalJetsConstituentsPFNano"):
    process.finalJetsConstituentsPFNano.src += cms.VInputTag(cms.InputTag(pfChargedHadName))
  process.customizedJetCandsTask.add(getattr(process, pfChargedHadName))

  setattr(process, pfChargedHadTableName, cms.EDProducer("SimplePATCandidateFlatTableProducer",
      src = cms.InputTag(pfChargedHadName),
      cut = cms.string(""), #we should not filter
      name = cms.string(tableName),
      doc = cms.string(tableDoc),
      singleton = cms.bool(False), # the number of entries is variable
      extension = cms.bool(False), # this is the extension table for the AK8 constituents
      variables = cms.PSet(
        # rawCaloFraction = Var("rawCaloFraction()", float, doc="(rawEcalE+rawHcalE)/candE. Only for isolated charged hadron", precision=15),
        # rawHcalFraction = Var("rawHcalFraction()", float, doc="rawHcalE/(rawEcalE+rawHcalE). Only for isolated charged hadrons", precision=15),
      )
    )
  )
  process.customizedJetCandsTask.add(getattr(process, pfChargedHadTableName))

  setattr(process, pfChargedHadExtTableName, cms.EDProducer("SimpleSelectedCandidateTableProducer",
      name = cms.string(tableName),
      candIdxName = cms.string("PFCandV2Idx"),
      candIdxDoc = cms.string("Index in PFCandV2 table"),
      candidatesMain = process.customPFConstituentsPFNanoTable.src,
      candidatesSelected = getattr(process,pfChargedHadTableName).src,
      # pc2gp = cms.InputTag("packedPFCandidateToGenAssociation" if runOnMC else "")
    )
  )
  process.customizedJetCandsTask.add(getattr(process ,pfChargedHadExtTableName))

  process.pfChargedHadronSelectedIsoCands = cms.EDProducer("PackedPFCandIsoProducer",
    packedPFCandidatesSelected = cms.InputTag(pfChargedHadName),
    packedPFCandidates = cms.InputTag("packedPFCandidates"),
    maxDeltaR = cms.double(0.4)
  )
  process.customizedJetCandsTask.add(process.pfChargedHadronSelectedIsoCands)
  if hasattr(process,"finalJetsConstituentsPFNano"):
    process.finalJetsConstituentsPFNano.src += cms.VInputTag(cms.InputTag("pfChargedHadronSelectedIsoCands"))

  return process

def SaveChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process,applyCHS=False,applyIso=False,runOnMC=True)
  return process

def SaveChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process,applyCHS=False,applyIso=False,runOnMC=False)
  return process

def SaveCHSIsoChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process, applyCHS=True,applyIso=True,runOnMC=True)
  return process

def SaveCHSIsoChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process, applyCHS=True,applyIso=True,runOnMC=False)
  return process

def SaveCHSChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process, applyCHS=True,runOnMC=True)
  return process

def SaveCHSChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process, applyCHS=True,runOnMC=False)
  return process

def SaveIsoChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=True,runOnMC=True)
  return process

def SaveIsoChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=True,runOnMC=False)
  return process

#########################################################################################################################################################
def SavePFInfoForElecPhoton(process):
  process.electronTable.variables.pf0pt    =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].pt():-1.",   float, doc="pf0 pt",precision=15)
  process.electronTable.variables.pf0eta   =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].eta():-9.",  float, doc="pf0 pt",precision=15)
  process.electronTable.variables.pf0phi   =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].phi():-9.",  float, doc="pf0 pt",precision=15)
  process.electronTable.variables.pf0mass  =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].mass():-1.", float, doc="pf0 pt",precision=15)
  process.electronTable.variables.pf0pdgId =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].pdgId():0",    int, doc="pf0 pdgid")
  process.electronTable.variables.pf1pt    =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].pt():-1.",   float, doc="pf1 pt",precision=15)
  process.electronTable.variables.pf1eta   =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].eta():-9.",  float, doc="pf1 pt",precision=15)
  process.electronTable.variables.pf1phi   =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].phi():-9.",  float, doc="pf1 pt",precision=15)
  process.electronTable.variables.pf1mass  =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].mass():-1.", float, doc="pf1 pt",precision=15)
  process.electronTable.variables.pf1pdgId =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].pdgId():0",   int,  doc="pf1 pdgid")

  process.photonTable.variables.pf0pt     =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].pt():-1.",   float, doc="pf0 pt",precision=15)
  process.photonTable.variables.pf0eta    =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].eta():-9.",  float, doc="pf0 pt",precision=15)
  process.photonTable.variables.pf0phi    =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].phi():-9.",  float, doc="pf0 pt",precision=15)
  process.photonTable.variables.pf0mass   =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].mass():-1.", float, doc="pf0 pt",precision=15)
  process.photonTable.variables.pf0pdgId  =  Var("?associatedPackedPFCandidates().size()>=1?associatedPackedPFCandidates()[0].pdgId():0",    int, doc="pf0 pdgid")
  process.photonTable.variables.pf1pt     =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].pt():-1.",   float, doc="pf1 pt",precision=15)
  process.photonTable.variables.pf1eta    =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].eta():-9.",  float, doc="pf1 pt",precision=15)
  process.photonTable.variables.pf1phi    =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].phi():-9.",  float, doc="pf1 pt",precision=15)
  process.photonTable.variables.pf1mass   =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].mass():-1.", float, doc="pf1 pt",precision=15)
  process.photonTable.variables.pf1pdgId  =  Var("?associatedPackedPFCandidates().size()>=2?associatedPackedPFCandidates()[1].pdgId():0",    int, doc="pf1 pdgid")
  return process

#########################################################################################################################################################
def SavePFInfoForTau(process):
  return process

#########################################################################################################################################################

def PrepJetConstituentTables(process, candInputForTable, saveOnlyPFCandsInJets,
  doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=False,
  doTau=False, doElectron=False, doPhoton=False, doMuon=False):

  ############################################################
  #
  # Setup table to store the PF candidates
  #
  ############################################################
  docStr = "PF Candidates"
  if saveOnlyPFCandsInJets:
    docStrList = []
    if doAK8Puppi: docStrList += ["AK8Puppi(|eta|<=2.5)"]
    if doAK4Puppi: docStrList += ["AK4Puppi"]
    if doAK4CHS:   docStrList += ["AK4CHS"]
    if doAK8PuppiSubjets:   docStrList += ["AK8PuppiSubjets"]
    docStr += " from following jets: "+", ".join(docStrList)
    docStr += "."
    if doTau or doElectron or doPhoton or doMuon:
      docStr += "Also from "
      if doTau:     docStr += " taus "
      if doElectron:docStr += " electrons "
      if doPhoton:docStr += " photons "
      if doMuon:docStr += " muons "

  # NOTE:
  # Need to change "SimplePATCandidateFlatTableProducer" if using >= CMSSW_14_0_6_patch1 (NanoV14 release)
  #
  process.customPFConstituentsPFNanoTable = cms.EDProducer("SimplePATCandidateFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("PFCandV2"),
    doc = cms.string(docStr),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      energy = Var("energy()", float, doc="energy",precision=-1),
      puppiWeight = Var("puppiWeight()", float, doc="Puppi weight",precision=-1),
      puppiWeightNoLep = Var("puppiWeightNoLep()", float, doc="Puppi weight removing leptons",precision=-1),
      passCHS = Var(pfCHS.cut.value(), bool, doc=pfCHS.cut.value()),
      isIsolatedChargedHadron = Var("isIsolatedChargedHadron()", bool, doc="isIsolatedChargedHadron()"),
      isStandAloneMuon = Var("isStandAloneMuon()", bool, doc="isStandAloneMuon()"),
      isGlobalMuon = Var("isGlobalMuon()", bool, doc="isGlobalMuon()"),
      isGoodEgamma = Var("isGoodEgamma()", bool, doc="isGoodEgamma()"),
      trkQuality = Var("?hasTrackDetails()?bestTrack().qualityMask():0", int, doc="track quality mask"),
      trkHighPurity = Var("trackHighPurity()", bool, doc="is trackHighPurity"),
      trkAlgo = Var("?hasTrackDetails()?bestTrack().algo():-1", int, doc="track algorithm"),
      trkP = Var("?hasTrackDetails()?bestTrack().p():-1", float, doc="track momemtum", precision=15),
      trkPt = Var("?hasTrackDetails()?bestTrack().pt():-1", float, doc="track pt", precision=15),
      trkEta = Var("?hasTrackDetails()?bestTrack().eta():-1", float, doc="track eta", precision=15),
      trkPhi = Var("?hasTrackDetails()?bestTrack().phi():-1", float, doc="track phi", precision=15),
      dz = Var("?hasTrackDetails()?dz():-1", float, doc="dz", precision=15),
      dzErr = Var("?hasTrackDetails()?dzError():-1", float, doc="dz err", precision=15),
      d0 = Var("?hasTrackDetails()?dxy():-1", float, doc="dxy", precision=15),
      d0Err = Var("?hasTrackDetails()?dxyError():-1", float, doc="dxy err", precision=15),
      nHits = Var("numberOfHits()", int, doc="numberOfHits()"),
      nPixelHits = Var("numberOfPixelHits()", int, doc="numberOfPixelHits()"),
      lostInnerHits = Var("lostInnerHits()", int, doc="lost inner hits. -1: validHitInFirstPixelBarrelLayer, 0: noLostInnerHits, 1: oneLostInnerHit, 2: moreLostInnerHits"),
      lostOuterHits = Var("?hasTrackDetails()?bestTrack().hitPattern().numberOfLostHits('MISSING_OUTER_HITS'):0", int, doc="lost outer hits"),
      trkChi2 = Var("?hasTrackDetails()?bestTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=15),
      pvAssocQuality = Var("pvAssociationQuality()", int, doc="primary vertex association quality (NotReconstructedPrimary = 0, OtherDeltaZ = 1, CompatibilityBTag = 4, CompatibilityDz = 5, UsedInFitLoose = 6, UsedInFitTight = 7)"),
      vertexRef = Var("?vertexRef().isNonnull()?vertexRef().key():-1", int, doc="vertexRef().key()"),
      fromPV0 = Var("fromPV()", int, doc="PV0 association (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)"),
      vtxChi2 = Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2",precision=15),
      caloFraction = Var("caloFraction()", float, doc="(EcalE+HcalE)/candE", precision=-1),
      hcalFraction = Var("hcalFraction()", float, doc="HcalE/(EcalE+HcalE)", precision=-1),
      rawCaloFraction = Var("rawCaloFraction()", float, doc="(rawEcalE+rawHcalE)/candE. Only for isolated charged hadron", precision=-1),
      rawHcalFraction = Var("rawHcalFraction()", float, doc="rawHcalE/(rawEcalE+rawHcalE). Only for isolated charged hadrons", precision=-1),
    )
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsPFNanoTable)
  #keep maximum precision for 4-vector
  process.customPFConstituentsPFNanoTable.variables.pt.precision = -1
  process.customPFConstituentsPFNanoTable.variables.eta.precision = -1
  process.customPFConstituentsPFNanoTable.variables.phi.precision = -1
  process.customPFConstituentsPFNanoTable.variables.mass.precision = -1

  ############################################################
  #
  # Extension to the PF candidate table for variables that cannot
  # be simply called in SimpleCandidateFlatTableProducer
  #
  ############################################################
  # process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
  #   srcPFCandidates = process.customPFConstituentsPFNanoTable.src,
  #   srcPrimaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
  #   name = process.customPFConstituentsPFNanoTable.name,
  #   srcWeights = cms.InputTag("packedpuppi"),
  #   weightName = cms.string("puppiWeightValueMap"),
  #   weightDoc = cms.string("Puppi Weight (ValueMap from PuppiProducer)"),
  #   weightPrecision = process.customPFConstituentsPFNanoTable.variables.puppiWeight.precision,
  # )
  # process.customizedJetCandsTask.add(process.customPFConstituentsExtTable)

  #
  # NOTE: Use this one if you want to store multiple constituent weights
  #
  # packedpuppi, packedpuppiNoLep = setupPuppiForPackedPF(process, useExistingWeights=True)
  process.customPFConstituentsPFNanoExtTable = cms.EDProducer("PFCandidateExtTableProducerV2",
    srcPFCandidates = process.customPFConstituentsPFNanoTable.src,
    name = process.customPFConstituentsPFNanoTable.name,
    srcWeightsV = cms.VInputTag(
      # cms.InputTag("packedpuppi"),
      # cms.InputTag("packedpuppiNoLep")
    ),
    weightNamesV = cms.vstring(
      # "puppiWeightValueMap",
      # "puppiWeightNoLepValueMap",
    ),
    weightDocsV = cms.vstring(
      # "Puppi Weight (ValueMap from PuppiProducer)",
      # "Puppi Weight No Lep (ValueMap from PuppiProducer)",
    ),
    weightPrecision = process.customPFConstituentsPFNanoTable.variables.puppiWeight.precision,
    saveFromPVvertexRef = cms.bool(True)
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsPFNanoExtTable)

  ############################################################
  #
  # Setup modules to store information to associate candidates
  # with jets.
  #
  ############################################################
  makeConstJetTable=True

  candIdxName=f"{process.customPFConstituentsPFNanoTable.name.value()}Idx"
  candIdxDoc=f"Index in the {process.customPFConstituentsPFNanoTable.name.value()} table"
  if doAK8Puppi:
    process.customAK8ConstituentsPFNanoTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.fatJetTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.fatJetTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK8ConstituentsPFNanoTable)

  if doAK4Puppi:
    process.customAK4PuppiConstituentsPFNanoTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.jetPuppiTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.jetPuppiTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK4PuppiConstituentsPFNanoTable)

  if doAK4CHS:
    process.customAK4CHSConstituentsPFNanoTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.jetTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.jetTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK4CHSConstituentsPFNanoTable)

  if doAK8PuppiSubjets:
    process.customAK8SubjetConstituentsPFNanoTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.subJetTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.subJetTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK8SubjetConstituentsPFNanoTable)

  if doTau:
    process.customTauConstituentsPFNanoTable = cms.EDProducer("SimplePatTauConstituentTableProducer",
      name = cms.string(f"{process.tauTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      taus = process.tauTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      tauCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customTauConstituentsPFNanoTable)

  if doElectron:
    process.customElectronPFCandsPFNanoTable = cms.EDProducer("SimplePatElectronPFCandTableProducer",
      name = cms.string(f"{process.electronTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.electronTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customElectronPFCandsPFNanoTable)

  if doPhoton:
    process.customPhotonPFCandsPFNanoTable = cms.EDProducer("SimplePatPhotonPFCandTableProducer",
      name = cms.string(f"{process.photonTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.photonTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customPhotonPFCandsPFNanoTable)

  if doMuon:
    process.customMuonPFCandsPFNanoTable = cms.EDProducer("SimplePatMuonPFCandTableProducer",
      name = cms.string(f"{process.muonTable.name.value()}{process.customPFConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.muonTable.src,
      candidates = process.customPFConstituentsPFNanoTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customMuonPFCandsPFNanoTable)

  return process

def ReducedPFCandInfo(process):

  process.customPFConstituentsPFNanoTable.variables.pt.precision   = 12
  process.customPFConstituentsPFNanoTable.variables.eta.precision  = 12
  process.customPFConstituentsPFNanoTable.variables.phi.precision  = 12
  process.customPFConstituentsPFNanoTable.variables.mass.precision = 12

  process.customPFConstituentsPFNanoTable.variables.dz.precision = 12
  process.customPFConstituentsPFNanoTable.variables.dzErr.precision = 12
  process.customPFConstituentsPFNanoTable.variables.d0.precision = 12
  process.customPFConstituentsPFNanoTable.variables.d0Err.precision = 12

  del process.customPFConstituentsPFNanoTable.variables.trkQuality
  del process.customPFConstituentsPFNanoTable.variables.trkHighPurity
  del process.customPFConstituentsPFNanoTable.variables.trkAlgo

  del process.customPFConstituentsPFNanoTable.variables.energy
  del process.customPFConstituentsPFNanoTable.variables.isIsolatedChargedHadron
  del process.customPFConstituentsPFNanoTable.variables.nHits
  del process.customPFConstituentsPFNanoTable.variables.nPixelHits
  del process.customPFConstituentsPFNanoTable.variables.lostInnerHits
  del process.customPFConstituentsPFNanoTable.variables.lostOuterHits
  del process.customPFConstituentsPFNanoTable.variables.caloFraction
  del process.customPFConstituentsPFNanoTable.variables.hcalFraction
  del process.customPFConstituentsPFNanoTable.variables.rawCaloFraction
  del process.customPFConstituentsPFNanoTable.variables.rawHcalFraction

  return process

def SavePuppiWeightsFromValueMap(process,puppiLabel="packedpuppi"):

  if not hasattr(process, puppiLabel):
    excpStr = f"{puppiLabel} not setup but asked to save weight from ValueMap in Nano."
    excpStr += f"Please check!"
    raise Exception(excpStr)
  else:
    print(f"SavePuppiWeightsFromValueMap()::Saving weights from {puppiLabel} ValueMap")

  process.customPFConstituentsExtTable.srcWeightsV += [
    cms.InputTag(puppiLabel),
    cms.InputTag(puppiLabel+"NoLep"),
  ]
  process.customPFConstituentsExtTable.weightNamesV += [
    "puppiWeightValueMap",
    "puppiWeightNoLepValueMap",
  ]
  process.customPFConstituentsExtTable.weightDocsV += [
    f"Puppi Weight (ValueMap from {puppiLabel} PuppiProducer)",
    f"Puppi Weight No Lep (ValueMap from {puppiLabel}NoLep PuppiProducer)",
  ]

  return process

def PrepGenJetConstituents(process, saveOnlyGenCandsInJets,
  doAK8=True, doAK4=True, doAK8Subjets=False, doTau=False):
  genCandList = cms.VInputTag()

  if saveOnlyGenCandsInJets:
    #################################################################
    # Collect pointers to candidates from different jet collections
    # and merge them into one list
    #################################################################
    if doAK8:
      # Collect AK8 Gen Constituents pointers
      process.genJetsAK8ConstituentsPFNano = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genJetAK8Table.src,
        cut = process.genJetAK8Table.cut
      )
      process.customizedJetCandsTask.add(process.genJetsAK8ConstituentsPFNano)
      genCandList += cms.VInputTag(cms.InputTag("genJetsAK8ConstituentsPFNano", "constituents"))

    if doAK8Subjets:
      # Collect AK8 Gen Subjet Constituents pointers
      process.genSubJetsAK8ConstituentsPFNano = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genSubJetAK8Table.src,
        cut = process.genSubJetAK8Table.cut
      )
      process.customizedJetCandsTask.add(process.genSubJetsAK8ConstituentsPFNano)
      genCandList += cms.VInputTag(cms.InputTag("genSubJetsAK8ConstituentsPFNano", "constituents"))

    if doAK4:
      # Collect AK4 Gen Constituents pointers
      process.genJetsAK4ConstituentsPFNano = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genJetTable.src,
        cut = process.genJetTable.cut
      )
      process.customizedJetCandsTask.add(process.genJetsAK4ConstituentsPFNano)
      genCandList += cms.VInputTag(cms.InputTag("genJetsAK4ConstituentsPFNano", "constituents"))

    if doTau:
      # Collect AK4 Gen Constituents pointers
      process.genJetsTauConstituentsPFNano = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genJetTable.src,
        cut = process.genJetTable.cut
      )
      process.customizedJetCandsTask.add(process.genJetsAK4ConstituentsPFNano)
      genCandList += cms.VInputTag(cms.InputTag("genJetsAK4ConstituentsPFNano", "constituents"))

    process.finalGenJetsConstituentsPFNano = cms.EDProducer("PackedGenParticlePtrMerger",
      src = genCandList,
      skipNulls = cms.bool(True),
      warnOnSkip = cms.bool(True)
    )
    process.customizedJetCandsTask.add(process.finalGenJetsConstituentsPFNano)
    candInputForTable = cms.InputTag("finalGenJetsConstituentsPFNano")
  else:
    ###################################
    # Store all packedGenParticles
    ###################################
    #
    # Collection to give to candidate table
    #
    candInputForTable = cms.InputTag("packedGenParticles")

  return process, candInputForTable

def PrepGenJetConstituentTables(process, candInputForTable, saveOnlyGenCandsInJets,
  doAK8=True, doAK4=True, doAK8Subjets=False):

  ############################################################
  #
  # Setup table to store the GenPart candidates
  #
  ############################################################
  docStr = "Particle-level (i.e status==1) Gen Candidates"
  if saveOnlyGenCandsInJets:
    docStrList = []
    if doAK8: docStrList += ["AK8Gen"]
    if doAK4: docStrList += ["AK4Gen"]
    if doAK8Subjets: docStrList += ["AK8GenSubjets"]
    docStr += " from following jets: "+",".join(docStrList)

  motherGenPartIdxDoc  = "Index of mother genpart in GenPart table."
  motherGenPartIdxDoc += "WARNING: Should only use this index to retrieve gen-particle in GenPart if *ALL* prunedGenParticles from Mini are stored in GenPart."
  motherGenPartIdxDoc += "This branch is useful to check if a GenPartCand has the same mother with another GenPartCand."
  motherGenPartIdxDoc += "Example would be to check for photons from pi0 decays."

  # NOTE:
  # - simplePATPackedGenParticleFlatTableProducer is defined in:
  #   src/JMEPFNano/Production/plugins/SimplePATFlatTableProducerPlugins.cc
  #
  process.customGenPartConstituentsPFNanoTable = cms.EDProducer("SimplePATPackedGenParticleFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("GenPartCand"),
    doc = cms.string(docStr),
    lazyEval = cms.untracked.bool(True),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      motherGenPartIdx    = Var("?motherRef().isNonnull()?motherRef().key():-1",    int, doc=motherGenPartIdxDoc),
      motherGenPartPdgId  = Var("?motherRef().isNonnull()?motherRef().pdgId():0",   int, doc="pdgId of mother genpart"),
      motherGenPartStatus = Var("?motherRef().isNonnull()?motherRef().status():-1", int, doc="status of mother genpart"),
      statusFlags = Var(
        "statusFlags().isLastCopyBeforeFSR()                  * 16384 +"
        "statusFlags().isLastCopy()                           * 8192  +"
        "statusFlags().isFirstCopy()                          * 4096  +"
        "statusFlags().fromHardProcessBeforeFSR()             * 2048  +"
        "statusFlags().isDirectHardProcessTauDecayProduct()   * 1024  +"
        "statusFlags().isHardProcessTauDecayProduct()         * 512   +"
        "statusFlags().fromHardProcess()                      * 256   +"
        "statusFlags().isHardProcess()                        * 128   +"
        "statusFlags().isDirectHadronDecayProduct()           * 64    +"
        "statusFlags().isDirectPromptTauDecayProduct()        * 32    +"
        "statusFlags().isDirectTauDecayProduct()              * 16    +"
        "statusFlags().isPromptTauDecayProduct()              * 8     +"
        "statusFlags().isTauDecayProduct()                    * 4     +"
        "statusFlags().isDecayedLeptonHadron()                * 2     +"
        "statusFlags().isPrompt()                             * 1      ",
        "uint16", doc=("gen status flags stored bitwise, bits are: "
           "0 : isPrompt, "
           "1 : isDecayedLeptonHadron, "
           "2 : isTauDecayProduct, "
           "3 : isPromptTauDecayProduct, "
           "4 : isDirectTauDecayProduct, "
           "5 : isDirectPromptTauDecayProduct, "
           "6 : isDirectHadronDecayProduct, "
           "7 : isHardProcess, "
           "8 : fromHardProcess, "
           "9 : isHardProcessTauDecayProduct, "
           "10 : isDirectHardProcessTauDecayProduct, "
           "11 : fromHardProcessBeforeFSR, "
           "12 : isFirstCopy, "
           "13 : isLastCopy, "
           "14 : isLastCopyBeforeFSR, ")
      ),
    )
  )
  process.customGenPartConstituentsPFNanoTable.variables.pdgId = Var("pdgId()", int, doc="pdgId from MC truth")
  process.customizedJetCandsTask.add(process.customGenPartConstituentsPFNanoTable)

  ###############################################################################################################
  # Uncomment this if you want to have meaningful mapping of the GenPartCand_genPartIdx to GenPart collection.
  ###############################################################################################################
  process.genParticleTable.src = "prunedGenParticles"
  process.genParticleTable.doc = "All gen particles from prunedGenParticles collection"
  process.genIso.genPart = "prunedGenParticles"

  # process.customGenPartConstituentsPFNanoExtTable = cms.EDProducer("GenParticleCandidateExtTableProducer",
  #   srcGenPartCandidates = process.customGenPartConstituentsPFNanoTable.src,
  #   name = process.customGenPartConstituentsPFNanoTable.name,
  # )
  # process.customizedJetCandsTask.add(process.customGenPartConstituentsPFNanoExtTable)

  #keep maximum precision for 4-vector
  process.customGenPartConstituentsPFNanoTable.variables.pt.precision = -1
  process.customGenPartConstituentsPFNanoTable.variables.eta.precision = -1
  process.customGenPartConstituentsPFNanoTable.variables.phi.precision = -1
  process.customGenPartConstituentsPFNanoTable.variables.mass.precision = -1

  # Add more branch for genParticleTable
  process.genParticleTable.variables.vx = Var("vx", float , doc="x coordinate of vertex position", precision=12)
  process.genParticleTable.variables.vy = Var("vy", float , doc="y coordinate of vertex position", precision=12)
  process.genParticleTable.variables.vz = Var("vz", float , doc="z coordinate of vertex position", precision=12)
  process.genParticleTable.variables.genPartIdxMother2 = Var("?numberOfMothers>1?motherRef(1).key():-1", "int", doc="index of the second mother particle, if valid")

  # Modify p4 branches
  process.genParticleTable.variables.pt.precision  = 12
  process.genParticleTable.variables.eta.precision = 12
  process.genParticleTable.variables.phi.precision = 12
  process.genParticleTable.variables.mass = Var("mass", float, precision=12)

  ############################################################
  #
  # Setup modules to store information to associate candidates
  # with jets.
  #
  ############################################################
  candIdxName=f"{process.customGenPartConstituentsPFNanoTable.name.value()}Idx"
  candIdxDoc=f"Index in the {process.customGenPartConstituentsPFNanoTable.name.value()} table"
  if doAK8:
    process.customAK8GenConstituentsPFNanoTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genJetAK8Table.name.value()}{process.customGenPartConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genJetAK8Table.src,
      candidates = process.customGenPartConstituentsPFNanoTable.src,
      jetCut = process.genJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.customAK8GenConstituentsPFNanoTable)

  if doAK8Subjets:
    process.customAK8SubJetGenConstituentsPFNanoTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genSubJetAK8Table.name.value()}{process.customGenPartConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genSubJetAK8Table.src,
      candidates = process.customGenPartConstituentsPFNanoTable.src,
      jetCut = process.genSubJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.customAK8SubJetGenConstituentsPFNanoTable)

  if doAK4:
    process.customAK4GenConstituentsPFNanoTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genJetTable.name.value()}{process.customGenPartConstituentsPFNanoTable.name.value()}"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genJetTable.src,
      candidates = process.customGenPartConstituentsPFNanoTable.src,
      jetCut = process.genJetTable.cut
    )
    process.customizedJetCandsTask.add(process.customAK4GenConstituentsPFNanoTable)
  return process

def ReducedGenPartCandInfo(process):
  process.customGenPartConstituentsPFNanoTable.variables.pt.precision = 12
  process.customGenPartConstituentsPFNanoTable.variables.eta.precision = 12
  process.customGenPartConstituentsPFNanoTable.variables.phi.precision = 12
  process.customGenPartConstituentsPFNanoTable.variables.mass.precision = 12

  process.genParticleTable.variables.pt.precision = 12
  process.genParticleTable.variables.eta.precision = 12
  process.genParticleTable.variables.phi.precision = 12
  process.genParticleTable.variables.mass.precision = 12

  del process.genParticleTable.variables.genPartIdxMother2

  return process
#
# https://cmssdt.cern.ch/lxr/source/PhysicsTools/NanoAOD/python/btvMC_cff.py
#
def AddBTVInfoForMC(process):
  process.btvMCTable = cms.EDProducer("BTVMCFlavourTableProducer",
    name=process.jetPuppiTable.name,
    src=process.jetPuppiTable.src,
    genparticles=cms.InputTag("prunedGenParticles")
  )
  process.jetMCTask.add(process.btvMCTable)
  return process

def ExtendGenVisTauTable(process):

  # https://github.com/cms-sw/cmssw/blob/CMSSW_15_0_15_patch4/PhysicsTools/NanoAOD/python/taus_cff.py#L168
  # Lower the gen visible tau pt cut from 10 GeV to 5 GeV
  process.genVisTauTable.cut = "pt > 5."

  process.genVisTauExtTable = cms.EDProducer("GenVisTauExtTableProducer",
    srcGenVisTaus = cms.InputTag("genVisTaus"),
    srcGenJetTaus = cms.InputTag("tauGenJetsSelectorAllHadronsForNano"),
    name = process.genVisTauTable.name,
    cut = process.genVisTauTable.cut,
  )
  process.genTauTask.add(process.genVisTauExtTable)

  return process
