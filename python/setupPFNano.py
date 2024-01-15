#
# Compatible with NanoV12 and JMENanoV12p5. Tested with MiniAODv4 using CMSSW_13_2_6_patch2
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data

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
  doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=False):

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

def SaveIsoChargedHadronPFCandidates(process):
  process.pfIsoChargedHadron = cms.EDProducer("PackedCandidatePtrSelector",
    src = cms.InputTag("packedPFCandidates"),
    cut = cms.string("isIsolatedChargedHadron()"),
  )
  process.finalJetsConstituents.src += cms.VInputTag(cms.InputTag("pfIsoChargedHadron"))
  process.customizedJetCandsTask.add(process.pfIsoChargedHadron)

  process.customPFIsoChargedHadronCandidateTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("pfIsoChargedHadron"),
    cut = cms.string(""), #we should not filter
    name = cms.string("IsoChHadPFCand"),
    doc = cms.string("Isolated Charged Hadron PF candidates passing CHS and track p > 3 GeV"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(
      rawCaloFraction = Var("rawCaloFraction()", float, doc="(rawEcalE+rawHcalE)/candE. Only for isolated charged hadron", precision=15),
      rawHcalFraction = Var("rawHcalFraction()", float, doc="rawHcalE/(rawEcalE+rawHcalE). Only for isolated charged hadrons", precision=15),
      caloFraction = Var("caloFraction()", float, doc="(EcalE+HcalE)/candE", precision=15),
      hcalFraction = Var("hcalFraction()", float, doc="HcalE/(EcalE+HcalE)", precision=15),
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
    )
  )
  process.customizedJetCandsTask.add(process.customPFIsoChargedHadronCandidateTable)

  process.customPFIsoChargedHadronCandidateExtTable = cms.EDProducer("SimpleSelectedCandidateTableProducer",
    name = cms.string("IsoChHadPFCand"),
    candIdxName = cms.string("PFCandIdx"),
    candIdxDoc = cms.string("Index in PFCand table"),
    candidatesMain = process.customPFConstituentsTable.src,
    candidatesSelected = process.customPFIsoChargedHadronCandidateTable.src,
    pc2gp = cms.InputTag("packedPFCandidateToGenAssociation")
  )
  process.customizedJetCandsTask.add(process.customPFIsoChargedHadronCandidateExtTable)

  return process

def PrepJetConstituentTables(process, candInputForTable, saveOnlyPFCandsInJets,
  doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=False):

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

  process.customPFConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("PFCand"),
    doc = cms.string(docStr),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      puppiWeight = Var("puppiWeight()", float, doc="Puppi weight",precision=-1),
      puppiWeightNoLep = Var("puppiWeightNoLep()", float, doc="Puppi weight removing leptons",precision=-1),
      passCHS = Var(pfCHS.cut.value(), bool, doc=pfCHS.cut.value()),
      isIsolatedChargedHadron = Var("isIsolatedChargedHadron()", bool, doc="isIsolatedChargedHadron()"),
      #
      # rawCaloFraction = Var("rawCaloFraction()", bool, doc="(rawEcalE+rawHcalE)/candE. Only for isolated charged hadron"),
      # rawHcalFraction = Var("rawHcalFraction()", bool, doc="rawHcalE/(rawEcalE+rawHcalE). Only for isolated charged hadrons"),
      # caloFraction = Var("caloFraction()", bool, doc="(EcalE+HcalE)/candE"),
      # hcalFraction = Var("hcalFraction()", bool, doc="HcalE/(EcalE+HcalE)"),
      #
      # trkQuality = Var("?hasTrackDetails()?bestTrack().qualityMask():0", int, doc="track quality mask"),
      # trkHighPurity = Var("trackHighPurity()", bool, doc="is trackHighPurity"),
      # trkAlgo = Var("?hasTrackDetails()?bestTrack().algo():-1", int, doc="track algorithm"),
      # trkP = Var("?hasTrackDetails()?bestTrack().p():-1", float, doc="track momemtum", precision=-1),
      # trkPt = Var("?hasTrackDetails()?bestTrack().pt():-1", float, doc="track pt", precision=-1),
      # trkEta = Var("?hasTrackDetails()?bestTrack().eta():-1", float, doc="track eta", precision=-1),
      # trkPhi = Var("?hasTrackDetails()?bestTrack().phi():-1", float, doc="track phi", precision=-1),
      # dz = Var("?hasTrackDetails()?dz():-1", float, doc="dz", precision=15),
      # dzErr = Var("?hasTrackDetails()?dzError():-1", float, doc="dz err", precision=15),
      # d0 = Var("?hasTrackDetails()?dxy():-1", float, doc="dxy", precision=15),
      # d0Err = Var("?hasTrackDetails()?dxyError():-1", float, doc="dxy err", precision=15),
      # nHits = Var("numberOfHits()", int, doc="numberOfHits()"),
      # nPixelHits = Var("numberOfPixelHits()", int, doc="numberOfPixelHits()"),
      # lostInnerHits = Var("lostInnerHits()", int, doc="lost inner hits. -1: validHitInFirstPixelBarrelLayer, 0: noLostInnerHits, 1: oneLostInnerHit, 2: moreLostInnerHits"),
      # lostOuterHits = Var("?hasTrackDetails()?bestTrack().hitPattern().numberOfLostHits('MISSING_OUTER_HITS'):0", int, doc="lost outer hits"),
      # trkChi2 = Var("?hasTrackDetails()?bestTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=15),
      # pvAssocQuality = Var("pvAssociationQuality()", int, doc="primary vertex association quality (NotReconstructedPrimary = 0, OtherDeltaZ = 1, CompatibilityBTag = 4, CompatibilityDz = 5, UsedInFitLoose = 6, UsedInFitTight = 7)"),
      # vertexRef = Var("?vertexRef().isNonnull()?vertexRef().key():-1", int, doc="vertexRef().key()"),
      # fromPV0 = Var("fromPV()", int, doc="PV0 association (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)"),
      # vtxChi2 = Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2",precision=15),
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
  # process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducerV2",
  #   srcPFCandidates = process.customPFConstituentsTable.src,
  #   name = process.customPFConstituentsTable.name,
  #   srcWeightsV = cms.VInputTag(
  #     cms.InputTag("packedpuppi")
  #   ),
  #   weightNamesV = cms.vstring(
  #     "puppiWeightValueMap",
  #   ),
  #   weightDocsV = cms.vstring(
  #     "Puppi Weight (ValueMap from PuppiProducer)",
  #   ),
  #   weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  # )
  # process.customizedJetCandsTask.add(process.customPFConstituentsExtTable)

  ############################################################
  #
  # Setup modules to store information to associate candidates
  # with jets. Can do this in two ways
  #
  #
  ############################################################
  addJetIdxForConstTable=False
  makeConstJetTable=True

  #
  # Option 1:
  # Add the index of the jets (to which a candidate belongs to)
  # in the candidate table.
  #
  if addJetIdxForConstTable:
    jetsList = []
    jetIdxNamesList = []
    jetIdxDocsList = []
    jetCutList = []
    if doAK8Puppi:
      jetsList += [process.fatJetTable.src.value()]
      jetIdxNamesList += [process.fatJetTable.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.fatJetTable.name.value()}"]
      jetCutList += [""]
    if doAK8PuppiSubjets:
      jetsList += [process.subJetTable.src.value()]
      jetIdxNamesList += [process.subJetTable.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.subJetTable.name.value()}"]
      jetCutList += [""]
    if doAK4Puppi:
      jetsList += [process.jetPuppiTable.src.value()]
      jetIdxNamesList += [process.jetPuppiTable.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.jetPuppiTable.name.value()}"]
      jetCutList += [""]
    if doAK4CHS:
      jetsList += [process.jetTable.src.value()]
      jetIdxNamesList += [process.jetTable.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.jetTable.name.value()}"]
      jetCutList += [""]

    process.customPFConstituentsJetIdxExtTable = cms.EDProducer("CandidatePatJetIdxExtTableProducer",
      name = process.customPFConstituentsTable.name,
      candidates = process.customPFConstituentsTable.src,
      jetsV = cms.VInputTag(jetsList),
      jetIdxNamesV = cms.vstring(jetIdxNamesList),
      jetIdxDocsV = cms.vstring(jetIdxDocsList),
      jetCutV = cms.vstring(jetCutList),
    )
    process.customizedJetCandsTask.add(process.customPFConstituentsJetIdxExtTable)

  #
  # Option 2:
  # Make a separate table for each jet collection, which consists of the index of the candidate
  # and the index of the jet
  #
  makeConstJetTable=False
  candIdxName="PFCandIdx"
  candIdxDoc="Index in the PFCand table"
  #
  #
  #
  if makeConstJetTable:
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

  process.customGenConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("GenPartCand"),
    doc = cms.string(docStr),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      # statusFlags = process.genParticleTable.variables.statusFlags, # We don't need this
    )
  )
  process.customGenConstituentsTable.variables.pdgId = Var("pdgId()", int, doc="pdgId from MC truth")
  process.customizedJetCandsTask.add(process.customGenConstituentsTable)

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
  # with jets. Can do this in two ways
  #
  #
  ############################################################
  addJetIdxForConstTable=False
  makeConstJetTable=True

  #
  # Option 1:
  # Add the index of the jets (to which a candidate belongs to)
  # in the candidate table.
  #
  if addJetIdxForConstTable:
    jetsList = []
    jetIdxNamesList = []
    jetIdxDocsList = []
    jetCutList = []
    if doAK8:
      jetsList += [process.genJetAK8Table.src.value()]
      jetIdxNamesList += [process.genJetAK8Table.name.value()]
      jetIdxDocsList += [f"Index of the parent gen jet in {process.genJetAK8Table.name.value()}"]
      jetCutList += [process.genJetAK8Table.cut.value()]
    if doAK8Subjets:
      jetsList += [process.genSubJetAK8Table.src.value()]
      jetIdxNamesList += [process.genSubJetAK8Table.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.genSubJetAK8Table.name.value()}"]
      jetCutList += [process.genSubJetAK8Table.cut.value()]
    if doAK4:
      jetsList += [process.genJetTable.src.value()]
      jetIdxNamesList += [process.genJetTable.name.value()]
      jetIdxDocsList += [f"Index of the parent jet in {process.genJetTable.name.value()}"]
      jetCutList += [process.genJetTable.cut.value()]

    process.customGenConstituentsJetIdxExtTable = cms.EDProducer("CandidateGenJetIdxExtTableProducer",
      name = process.customGenConstituentsTable.name,
      candidates = process.customGenConstituentsTable.src,
      jetsV = cms.VInputTag(jetsList),
      jetIdxNamesV = cms.vstring(jetIdxNamesList),
      jetIdxDocsV = cms.vstring(jetIdxDocsList),
      jetCutV = cms.vstring(jetCutList),
    )
    process.customizedJetCandsTask.add(process.customGenConstituentsJetIdxExtTable)

  #
  # Option 2:
  # Make a separate table for each jet collection, which consists of the index of the candidate
  # and the index of the jet
  #
  if makeConstJetTable:
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
