#
# Compatible with NanoV12 and JMENanoV12p5. Tested with MiniAODv4 using CMSSW_13_2_6_patch2
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
      process.finalJetsAK8Constituents = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJetsAK8"),
        cut = cms.string("abs(eta) <= 2.5") # Store PF candidates for central jets in finalJetsAK8
      )
      process.customizedJetCandsTask.add(process.finalJetsAK8Constituents)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK8Constituents", "constituents"))

    if doAK4Puppi:
      # Collect AK4 Puppi Constituents pointers
      process.finalJetsAK4PuppiConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJetsPuppi"),
        cut = cms.string("") # Store all PF candidates for all jets in finalJetsPuppi
      )
      process.customizedJetCandsTask.add(process.finalJetsAK4PuppiConstituents)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK4PuppiConstituents", "constituents"))

    if doAK4CHS:
      # Collect AK4 CHS Constituents pointers
      process.finalJetsAK4CHSConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("finalJets"),
        cut = cms.string("") # Store all PF candidates for all jets in finalJets
      )
      process.customizedJetCandsTask.add(process.finalJetsAK4CHSConstituents)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK4CHSConstituents", "constituents"))

    if doAK8PuppiSubjets:
      # Collect AK8 Puppi Subjets Constituents pointers
      process.finalJetsAK8SubjetConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
        src = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
        cut = cms.string("") # Store all PF candidates for all subjets
      )
      process.customizedJetCandsTask.add(process.finalJetsAK8SubjetConstituents)
      candList += cms.VInputTag(cms.InputTag("finalJetsAK8SubjetConstituents", "constituents"))

    if doTau:
      # Collect Tau signalCands and isolationCands
      process.finalTausConstituents = cms.EDProducer("PatTauConstituentSelector",
        src = cms.InputTag("finalTaus"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalTausConstituents)
      candList += cms.VInputTag(cms.InputTag("finalTausConstituents", "constituents"))

    if doElectron:
      process.finalElectronsPFCandsConstituents = cms.EDProducer("PatElectronPFCandSelector",
        src = cms.InputTag("finalElectrons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalElectronsPFCandsConstituents)
      candList += cms.VInputTag(cms.InputTag("finalElectronsPFCandsConstituents", "constituents"))

    if doPhoton:
      process.finalPhotonsPFCandsConstituents = cms.EDProducer("PatPhotonPFCandSelector",
        src = cms.InputTag("finalPhotons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalPhotonsPFCandsConstituents)
      candList += cms.VInputTag(cms.InputTag("finalPhotonsPFCandsConstituents", "constituents"))

    if doMuon:
      process.finalMuonsPFCandsConstituents = cms.EDProducer("PatMuonPFCandSelector",
        src = cms.InputTag("finalMuons"),
        cut = cms.string("") # Store all PF candidates for all taus
      )
      process.customizedJetCandsTask.add(process.finalMuonsPFCandsConstituents)
      candList += cms.VInputTag(cms.InputTag("finalMuonsPFCandsConstituents", "constituents"))

    #
    # Merge all candidate pointers
    #
    process.finalJetsConstituents = cms.EDProducer("PackedCandidatePtrMerger",
      src = candList,
      skipNulls = cms.bool(True),
      warnOnSkip = cms.bool(True)
    )
    process.customizedJetCandsTask.add(process.finalJetsConstituents)
    #
    # Collection to give to candidate table
    #
    candInputForTable = cms.InputTag("finalJetsConstituents")
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
def SaveChargedHadronPFCandidates(process, applyIso=False, runOnMC=False):

  pfChargedHadName = "pfChargedHadronSelected"
  pfChargedHadTableName = "customPFChargedHadronCandidateTable"
  pfChargedHadExtTableName = "customPFChargedHadronCandidateExtTable"
  cutStr = f"abs(pdgId()) == 211 && ({pfCHS.cut.value()})"
  tableName = "CHSChHadPFCand"
  tableDoc  = "Charged Hadron PF candidates with CHS applied"
  if applyIso:
    pfChargedHadName = "pfIsoChargedHadronSelected"
    pfChargedHadTableName = "customPFIsoChargedHadronCandidateTable"
    pfChargedHadExtTableName = "customPFIsoChargedHadronCandidateExtTable"
    cutStr = "isIsolatedChargedHadron()"
    tableName = "IsoChHadPFCand"
    tableDoc  = "Isolated " + tableDoc

  setattr(process, pfChargedHadName, cms.EDProducer("PackedCandidatePtrSelector",
      src = cms.InputTag("packedPFCandidates"),
      cut = cms.string(cutStr),
    )
  )
  if hasattr(process,"finalJetsConstituents"):
    process.finalJetsConstituents.src += cms.VInputTag(cms.InputTag(pfChargedHadName))
  process.customizedJetCandsTask.add(getattr(process, pfChargedHadName))

  # NOTE:
  # Need to change "SimplePATCandidateFlatTableProducer" if using >= CMSSW_14_0_6_patch1 (NanoV14 release)
  #
  setattr(process, pfChargedHadTableName, cms.EDProducer("SimpleCandidateFlatTableProducer",
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
      candIdxName = cms.string("PFCandIdx"),
      candIdxDoc = cms.string("Index in PFCand table"),
      candidatesMain = process.customPFConstituentsTable.src,
      candidatesSelected = getattr(process,pfChargedHadTableName).src,
      # pc2gp = cms.InputTag("packedPFCandidateToGenAssociation" if runOnMC else "")
    )
  )
  process.customizedJetCandsTask.add(getattr(process ,pfChargedHadExtTableName))

  return process

def SaveIsoChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=True,runOnMC=True)
  return process

def SaveIsoChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=True,runOnMC=False)
  return process

def SaveChargedHadronPFCandidates_MC(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=False,runOnMC=True)
  return process

def SaveChargedHadronPFCandidates_Data(process):
  process = SaveChargedHadronPFCandidates(process, applyIso=False,runOnMC=False)
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
  # process.customPFConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
  process.customPFConstituentsTable = cms.EDProducer("SimplePATCandidateFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("PFCand"),
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
      trkP = Var("?hasTrackDetails()?bestTrack().p():-1", float, doc="track momemtum", precision=-1),
      trkPt = Var("?hasTrackDetails()?bestTrack().pt():-1", float, doc="track pt", precision=-1),
      trkEta = Var("?hasTrackDetails()?bestTrack().eta():-1", float, doc="track eta", precision=-1),
      trkPhi = Var("?hasTrackDetails()?bestTrack().phi():-1", float, doc="track phi", precision=-1),
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
      caloFraction = Var("caloFraction()", float, doc="(EcalE+HcalE)/candE", precision=15),
      hcalFraction = Var("hcalFraction()", float, doc="HcalE/(EcalE+HcalE)", precision=15),
      rawCaloFraction = Var("rawCaloFraction()", float, doc="(rawEcalE+rawHcalE)/candE. Only for isolated charged hadron", precision=15),
      rawHcalFraction = Var("rawHcalFraction()", float, doc="rawHcalE/(rawEcalE+rawHcalE). Only for isolated charged hadrons", precision=15),
    )
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsTable)
  #keep maximum precision for 4-vector
  process.customPFConstituentsTable.variables.pt.precision = -1
  process.customPFConstituentsTable.variables.eta.precision = -1
  process.customPFConstituentsTable.variables.phi.precision = -1
  process.customPFConstituentsTable.variables.mass.precision = -1

  ############################################################
  #
  # Extension to the PF candidate table for variables that cannot
  # be simply called in SimpleCandidateFlatTableProducer
  #
  ############################################################
  # process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
  #   srcPFCandidates = process.customPFConstituentsTable.src,
  #   srcPrimaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
  #   name = process.customPFConstituentsTable.name,
  #   srcWeights = cms.InputTag("packedpuppi"),
  #   weightName = cms.string("puppiWeightValueMap"),
  #   weightDoc = cms.string("Puppi Weight (ValueMap from PuppiProducer)"),
  #   weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  # )
  # process.customizedJetCandsTask.add(process.customPFConstituentsExtTable)

  #
  # NOTE: Use this one if you want to store multiple constituent weights
  #
  # packedpuppi, packedpuppiNoLep = setupPuppiForPackedPF(process, useExistingWeights=True)
  process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducerV2",
    srcPFCandidates = process.customPFConstituentsTable.src,
    name = process.customPFConstituentsTable.name,
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
    weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
    saveFromPVvertexRef = cms.bool(True)
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsExtTable)

  ############################################################
  #
  # Setup modules to store information to associate candidates
  # with jets.
  #
  #
  ############################################################
  makeConstJetTable=True

  candIdxName="PFCandIdx"
  candIdxDoc="Index in the PFCand table"
  if doAK8Puppi:
    process.customAK8ConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.fatJetTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.fatJetTable.src,
      candidates = process.customPFConstituentsTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK8ConstituentsTable)

  if doAK4Puppi:
    process.customAK4PuppiConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.jetPuppiTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.jetPuppiTable.src,
      candidates = process.customPFConstituentsTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK4PuppiConstituentsTable)

  if doAK4CHS:
    process.customAK4CHSConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.jetTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.jetTable.src,
      candidates = process.customPFConstituentsTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK4CHSConstituentsTable)

  if doAK8PuppiSubjets:
    process.customAK8SubjetConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      name = cms.string(f"{process.subJetTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.subJetTable.src,
      candidates = process.customPFConstituentsTable.src,
      jetCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customAK8SubjetConstituentsTable)

  if doTau:
    process.customTauConstituentsTable = cms.EDProducer("SimplePatTauConstituentTableProducer",
      name = cms.string(f"{process.tauTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      taus = process.tauTable.src,
      candidates = process.customPFConstituentsTable.src,
      tauCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customTauConstituentsTable)

  if doElectron:
    process.customElectronPFCandsTable = cms.EDProducer("SimplePatElectronPFCandTableProducer",
      name = cms.string(f"{process.electronTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.electronTable.src,
      candidates = process.customPFConstituentsTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customElectronPFCandsTable)

  if doPhoton:
    process.customPhotonPFCandsTable = cms.EDProducer("SimplePatPhotonPFCandTableProducer",
      name = cms.string(f"{process.photonTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.photonTable.src,
      candidates = process.customPFConstituentsTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customPhotonPFCandsTable)

  if doMuon:
    process.customMuonPFCandsTable = cms.EDProducer("SimplePatMuonPFCandTableProducer",
      name = cms.string(f"{process.muonTable.name.value()}PFCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      objects = process.muonTable.src,
      candidates = process.customPFConstituentsTable.src,
      objectCut = cms.string("") # No need to apply cut here.
    )
    process.customizedJetCandsTask.add(process.customMuonPFCandsTable)

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
  doAK8=True, doAK4=True, doAK8Subjets=False):
  genCandList = cms.VInputTag()

  if saveOnlyGenCandsInJets:
    #################################################################
    # Collect pointers to candidates from different jet collections
    # and merge them into one list
    #################################################################
    if doAK8:
      # Collect AK8 Gen Constituents pointers
      process.genJetsAK8Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genJetAK8Table.src,
        cut = process.genJetAK8Table.cut
      )
      process.customizedJetCandsTask.add(process.genJetsAK8Constituents)
      genCandList += cms.VInputTag(cms.InputTag("genJetsAK8Constituents", "constituents"))

    if doAK8Subjets:
      # Collect AK8 Gen Subjet Constituents pointers
      process.genSubJetsAK8Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genSubJetAK8Table.src,
        cut = process.genSubJetAK8Table.cut
      )
      process.customizedJetCandsTask.add(process.genSubJetsAK8Constituents)
      genCandList += cms.VInputTag(cms.InputTag("genSubJetsAK8Constituents", "constituents"))

    if doAK4:
      # Collect AK4 Gen Constituents pointers
      process.genJetsAK4Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
        src = process.genJetTable.src,
        cut = process.genJetTable.cut
      )
      process.customizedJetCandsTask.add(process.genJetsAK4Constituents)
      genCandList += cms.VInputTag(cms.InputTag("genJetsAK4Constituents", "constituents"))

    process.finalGenJetsConstituents = cms.EDProducer("PackedGenParticlePtrMerger",
      src = genCandList,
      skipNulls = cms.bool(True),
      warnOnSkip = cms.bool(True)
    )
    process.customizedJetCandsTask.add(process.finalGenJetsConstituents)
    candInputForTable = cms.InputTag("finalGenJetsConstituents")
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
  # Need to change "simplePATPackedGenParticleFlatTableProducer" if using >= CMSSW_14_0_6_patch1 (NanoV14 release)
  # - simplePATPackedGenParticleFlatTableProducer is defined in:
  #   src/JMEPFNano/Production/plugins/SimplePATFlatTableProducerPlugins.cc
  #
  # process.customGenConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
  process.customGenConstituentsTable = cms.EDProducer("SimplePATPackedGenParticleFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("GenPartCand"),
    doc = cms.string(docStr),
    lazyEval = cms.untracked.bool(True),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      motherGenPartIdx    = Var("?motherRef().isNonnull()?motherRef().key():-1",    int, doc=motherGenPartIdxDoc),
      # motherGenPartPdgId  = Var("?motherRef().isNonnull()?motherRef().pdgId():0",   int, doc="pdgId of mother genpart"),
      # motherGenPartStatus = Var("?motherRef().isNonnull()?motherRef().status():-1", int, doc="status of mother genpart"),
    )
  )
  process.customGenConstituentsTable.variables.pdgId = Var("pdgId()", int, doc="pdgId from MC truth")
  process.customizedJetCandsTask.add(process.customGenConstituentsTable)

  ###############################################################################################################
  # Uncomment this if you want to have meaningful mapping of the GenPartCand_genPartIdx to GenPart collection.
  ###############################################################################################################
  process.genParticleTable.src = "prunedGenParticles"
  process.genParticleTable.doc = "All gen particles from prunedGenParticles"
  process.genIso.genPart = "prunedGenParticles" # Need to set this if use >= CMSSW_14_0_6_patch1

  # process.customGenParticleConstituentsExtTable = cms.EDProducer("GenParticleCandidateExtTableProducer",
  #   srcGenPartCandidates = process.customGenConstituentsTable.src,
  #   name = process.customGenConstituentsTable.name,
  # )
  # process.customizedJetCandsTask.add(process.customGenParticleConstituentsExtTable)

  #keep maximum precision for 4-vector
  process.customGenConstituentsTable.variables.pt.precision = -1
  process.customGenConstituentsTable.variables.eta.precision = -1
  process.customGenConstituentsTable.variables.phi.precision = -1
  process.customGenConstituentsTable.variables.mass.precision = -1

  ############################################################
  #
  # Setup modules to store information to associate candidates
  # with jets.
  #
  #
  ############################################################
  candIdxName="GenPartCandIdx"
  candIdxDoc="Index in the GenPartCand table"
  if doAK8:
    process.customAK8GenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genJetAK8Table.name.value()}GenPartCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genJetAK8Table.src,
      candidates = process.customGenConstituentsTable.src,
      jetCut = process.genJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.customAK8GenConstituentsTable)

  if doAK8Subjets:
    process.customAK8SubJetGenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genSubJetAK8Table.name.value()}GenPartCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genSubJetAK8Table.src,
      candidates = process.customGenConstituentsTable.src,
      jetCut = process.genSubJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.customAK8SubJetGenConstituentsTable)

  if doAK4:
    process.customAK4GenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      name = cms.string(f"{process.genJetTable.name.value()}GenPartCand"),
      candIdxName = cms.string(candIdxName),
      candIdxDoc = cms.string(candIdxDoc),
      jets = process.genJetTable.src,
      candidates = process.customGenConstituentsTable.src,
      jetCut = process.genJetTable.cut
    )
    process.customizedJetCandsTask.add(process.customAK4GenConstituentsTable)
  return process
