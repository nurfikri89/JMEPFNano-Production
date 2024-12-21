import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data

def PrepJMEPFCustomNanoAOD(process, runOnMC):
  process.customizedPFCandsTask = cms.Task()
  process.schedule.associate(process.customizedPFCandsTask)

  process.rekeyAK4PuppiJets = cms.EDProducer("RekeyReclusteredPuppiJets",
    candidates = cms.InputTag("packedPFCandidates"),
    jets = cms.InputTag("updatedJetsAK4PFPUPPIWithUserData"),
  )
  process.jetAK4PFPUPPISequence.insert(process.jetAK4PFPUPPISequence.index(process.updatedJetsAK4PFPUPPIWithUserData)+1, process.rekeyAK4PuppiJets)
  process.finalJetsAK4PFPUPPI.src = "rekeyAK4PuppiJets"
  #
  #
  #
  process.finalJetsAK8Constituents = cms.EDProducer("PatJetConstituentPtrSelector",
    src = cms.InputTag("finalJetsAK8"),
    cut = cms.string("")
  )
  process.customizedPFCandsTask.add(process.finalJetsAK8Constituents)

  #
  #
  #
  process.finalJetsAK4CHSConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
    src = cms.InputTag("finalJets"),
    cut = cms.string("pt > 8")
  )
  process.customizedPFCandsTask.add(process.finalJetsAK4CHSConstituents)

  #
  #
  #
  process.finalJetsAK4PuppiConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
    src = cms.InputTag("finalJetsAK4PFPUPPI"),
    cut = cms.string("pt > 8")
  )
  process.customizedPFCandsTask.add(process.finalJetsAK4PuppiConstituents)

  #
  #
  #
  #
  candList = cms.VInputTag(
    # cms.InputTag("finalJetsAK8Constituents", "constituents"),
    cms.InputTag("finalJetsAK4CHSConstituents", "constituents"), 
    cms.InputTag("finalJetsAK4PuppiConstituents", "constituents")
  )
  process.finalJetsConstituents = cms.EDProducer("PackedCandidatePtrMerger", 
    src = candList, 
    skipNulls = cms.bool(True), 
    warnOnSkip = cms.bool(True)
  )
  process.customizedPFCandsTask.add(process.finalJetsConstituents)
  candInputForTable = cms.InputTag("finalJetsConstituents")

  process.customPFConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
  src = candInputForTable,
  cut = cms.string(""), #we should not filter
  name = cms.string("PFCand"),
  doc = cms.string("interesting particles from AK4 and AK8 jets"),
  singleton = cms.bool(False), # the number of entries is variable
  extension = cms.bool(False), # this is the extension table for the AK8 constituents
  variables = cms.PSet(CandVars,
      energy = Var("energy()", float, doc="energy",precision=-1),
      puppiWeight = Var("puppiWeight()", float, doc="Puppi weight",precision=-1),
      puppiWeightNoLep = Var("puppiWeightNoLep()", float, doc="Puppi weight removing leptons",precision=-1),
      passCHS = Var("fromPV", bool, doc="fromPV(0)"),
      isIsolatedChargedHadron = Var("isIsolatedChargedHadron()", bool, doc="isIsolatedChargedHadron()"),
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
  process.customizedPFCandsTask.add(process.customPFConstituentsTable)
  #keep maximum precision for 4-vector
  process.customPFConstituentsTable.variables.pt.precision = -1
  process.customPFConstituentsTable.variables.eta.precision = -1
  process.customPFConstituentsTable.variables.phi.precision = -1
  process.customPFConstituentsTable.variables.mass.precision = -1

  process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
    srcPFCandidates = process.customPFConstituentsTable.src,
    srcPrimaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    name = process.customPFConstituentsTable.name,
    # srcWeights = cms.InputTag("packedpuppi"),
    # weightName = cms.string("puppiWeightValueMap"),
    # weightDoc = cms.string("Puppi Weight (ValueMap from PuppiProducer)"),
    # weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  )
  process.customizedPFCandsTask.add(process.customPFConstituentsExtTable)

  process.customAK8ConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJetsAK8"),
    name = cms.string("FatJetPFCand"),
    idx_name = cms.string("PFCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK8ConstituentsTable)

  process.customAK4CHSConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJets"),
    name = cms.string("JetPFCand"),
    idx_name = cms.string("PFCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4CHSConstituentsTable)

  process.customAK4PuppiConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJetsAK4PFPUPPI"),
    name = cms.string("JetPuppiPFCand"),
    idx_name = cms.string("PFCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4PuppiConstituentsTable)

  return process

def PrepJMEPFCustomNanoAOD_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True)
  return process

def PrepJMEPFCustomNanoAOD_Data(process):
  PrepJMECustomNanoAOD_Data(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=False)
  return process