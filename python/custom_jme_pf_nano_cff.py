#
# Compatible with NanoV11 (CMSSW_12_6_0_patch1). Tested on Run3Summer22MiniAODv3 (CMSSSW_12_4_11_patch3) samples 
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

from CommonTools.PileupAlgos.Puppi_cff import puppi
from CommonTools.ParticleFlow.pfCHS_cff import pfCHS

from PhysicsTools.PatAlgos.tools.helpers  import getPatAlgosToolsTask, addToProcessAndTask
def addProcessAndTask(proc, label, module):
  task = getPatAlgosToolsTask(proc)
  addToProcessAndTask(label, module, proc, task)

def PrepPuppiProducer(process):
  #
  # NOTE: We setup "packedPFCandidatespuppi" here if not done in JMENano.
  # Situation where this can happen is when we use slimmedJets and slimmedJetsPuppi
  # for the input jet collection table
  #
  puppiForJetReclusterInJMENano="packedPFCandidatespuppi"
  if not hasattr(process,puppiForJetReclusterInJMENano):
    addProcessAndTask(process, puppiForJetReclusterInJMENano, puppi.clone(
        candName = "packedPFCandidates",
        vertexName = "offlineSlimmedPrimaryVertices",
        clonePackedCands = True,
        useExistingWeights = True,
      )
   )
  return process

#####################################################################
#
#
#
######################################################################
def PrepJetConstituents(process, doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=True):
  candList = cms.VInputTag()

  if doAK8Puppi:
    # Collect AK8 Puppi Constituents pointers
    process.finalJetsAK8Constituents = cms.EDProducer("PatJetConstituentPtrSelector",
      src = cms.InputTag("finalJetsAK8"),
      cut = cms.string("") # Store all PF candidates for all jets in finalJetsAK8
    )
    process.customizedJetCandsTask.add(process.finalJetsAK8Constituents)
    candList += cms.VInputTag(cms.InputTag("finalJetsAK8Constituents", "constituents"))

  if doAK8PuppiSubjets:
    # Collect AK8 Puppi Subjets Constituents pointers
    process.finalJetsAK8SubjetConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
      src = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
      cut = cms.string("") # Store all PF candidates for all jets in finalJetsAK8
    )
    process.customizedJetCandsTask.add(process.finalJetsAK8SubjetConstituents)
    candList += cms.VInputTag(cms.InputTag("finalJetsAK8SubjetConstituents", "constituents"))

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

  return process, candList

def PrepJetConstituentTables(process, candInputForTable, saveOnlyPFCandsInJets, 
  doAK8Puppi=True, doAK4Puppi=True, doAK4CHS=True, doAK8PuppiSubjets=True):

  docStr = "PF Candidates"
  if saveOnlyPFCandsInJets:
    docStrList = []
    if doAK8Puppi: docStrList += ["AK8Puppi"]
    if doAK4Puppi: docStrList += ["AK4Puppi"]
    if doAK4CHS:   docStrList += ["AK4CHS"]
    if doAK8PuppiSubjets:   docStrList += ["AK8PuppiSubjets"]
    docStr += " from following jets: "+",".join(docStrList)

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
      vtxChi2 = Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2",precision=15),
      trkChi2 = Var("?hasTrackDetails()?pseudoTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=15),
      dz = Var("?hasTrackDetails()?dz():-1", float, doc="dz", precision=15),
      dzErr = Var("?hasTrackDetails()?dzError():-1", float, doc="dz err", precision=15),
      d0 = Var("?hasTrackDetails()?dxy():-1", float, doc="dxy", precision=15),
      d0Err = Var("?hasTrackDetails()?dxyError():-1", float, doc="dxy err", precision=15),
      pvAssocQuality = Var("pvAssociationQuality()", int, doc="primary vertex association quality (NotReconstructedPrimary = 0, OtherDeltaZ = 1, CompatibilityBTag = 4, CompatibilityDz = 5, UsedInFitLoose = 6, UsedInFitTight = 7)"),
      fromPV0 = Var("fromPV()", int, doc="PV0 association (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)"),
      vertexRef = Var("?vertexRef().isNonnull()?vertexRef().key():-1", int, doc="vertexRef().key()"),
      trkQuality = Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
      trkHighPurity = Var("trackHighPurity()", bool, doc="is trackHighPurity"),
      passCHS = Var(pfCHS.cut.value(), bool, doc=pfCHS.cut.value()),
      nPixelHits = Var("numberOfPixelHits()", int, doc="numberOfPixelHits()"),
      nHits = Var("numberOfHits()", int, doc="numberOfHits()"),
      lostInnerHits = Var("lostInnerHits()", int, doc="lostInnerHits()"),
    )
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsTable)
  #keep maximum precision for 4-vector
  process.customPFConstituentsTable.variables.pt.precision = -1 
  process.customPFConstituentsTable.variables.eta.precision = -1
  process.customPFConstituentsTable.variables.phi.precision = -1
  process.customPFConstituentsTable.variables.mass.precision = -1

  process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
    srcPFCandidates = process.customPFConstituentsTable.src,
    srcPrimaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
    name = process.customPFConstituentsTable.name,
    srcWeights = cms.InputTag("packedPFCandidatespuppi"),
    weightName = cms.string("puppiWeightValueMap"),
    weightDoc = cms.string("Puppi Weight (ValueMap from PuppiProducer)"),
    weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  )
  process.customizedJetCandsTask.add(process.customPFConstituentsExtTable)

  #
  # NOTE: Use this one if you want to store multiple constituent weights
  #
  # process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducerV2",
  #   srcPFCandidates = process.customPFConstituentsTable.src,
  #   name = process.customPFConstituentsTable.name,
  #   srcWeightsV = cms.VInputTag(
  #     cms.InputTag("packedPFCandidatespuppi")
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

  if doAK8Puppi:
    process.customAK8ConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      candidates = process.customPFConstituentsTable.src,
      jets = cms.InputTag("finalJetsAK8"),
      name = cms.string("FatJetPFCand"),
      idx_name = cms.string("PFCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK8ConstituentsTable)

  if doAK8PuppiSubjets:
    process.customAK8SubjetConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      candidates = process.customPFConstituentsTable.src,
      jets = cms.InputTag("slimmedJetsAK8PFPuppiSoftDropPacked","SubJets"),
      name = cms.string("SubJetPFCand"),
      idx_name = cms.string("PFCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK8SubjetConstituentsTable)

  if doAK4Puppi:
    process.customAK4PuppiConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      candidates = process.customPFConstituentsTable.src,
      jets = cms.InputTag("finalJetsPuppi"),
      name = cms.string("JetPFCand"),
      idx_name = cms.string("PFCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK4PuppiConstituentsTable)
    # Switch name for Run-2.
    run2_nanoAOD_ANY.toModify(
      process.customAK4PuppiConstituentsTable, name="JetPuppiPFCand"
    )

  if doAK4CHS:
    process.customAK4CHSConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
      candidates = process.customPFConstituentsTable.src,
      jets = cms.InputTag("finalJets"),
      name = cms.string("JetCHSPFCand"),
      idx_name = cms.string("PFCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK4CHSConstituentsTable)
    # Switch name for Run-2.
    run2_nanoAOD_ANY.toModify(
      process.customAK4CHSConstituentsTable, name="JetPFCand"
    )

  return process

def PrepGenJetConstituents(process, doAK8=True, doAK4=True, doAK8Subjets=True):
  candList = cms.VInputTag()

  if doAK8:
    # Collect AK8 Gen Constituents pointers
    process.genJetsAK8Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
      src = process.genJetAK8Table.src,
      cut = process.genJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.genJetsAK8Constituents)
    candList += cms.VInputTag(cms.InputTag("genJetsAK8Constituents", "constituents"))

  if doAK8Subjets:
    # Collect AK8 Gen Subjet Constituents pointers
    process.genSubJetsAK8Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
      src = process.genSubJetAK8Table.src,
      cut = process.genSubJetAK8Table.cut
    )
    process.customizedJetCandsTask.add(process.genSubJetsAK8Constituents)
    candList += cms.VInputTag(cms.InputTag("genSubJetsAK8Constituents", "constituents"))

  if doAK4:
    # Collect AK4 Gen Constituents pointers
    process.genJetsAK4Constituents = cms.EDProducer("GenJetPackedConstituentPtrSelector",
      src = process.genJetTable.src,
      cut = process.genJetTable.cut
    )
    process.customizedJetCandsTask.add(process.genJetsAK4Constituents)
    candList += cms.VInputTag(cms.InputTag("genJetsAK4Constituents", "constituents"))

  return process, candList

def PrepGenJetConstituentTables(process, candInputForTable, saveOnlyGenCandsInJets, doAK8=True, doAK4=True, doAK8Subjets=True):

  docStr = "Particle-level Gen Candidates"
  if saveOnlyGenCandsInJets:
    docStrList = []
    if doAK8: docStrList += ["AK8Gen"]
    if doAK4: docStrList += ["AK4Gen"]
    if doAK8Subjets: docStrList += ["AK8GenSubjets"]
    docStr += " from following jets: "+",".join(docStrList)

  process.customGenConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = candInputForTable,
    cut = cms.string(""), #we should not filter
    name = cms.string("GenCand"),
    doc = cms.string(docStr),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the extension table for the AK8 constituents
    variables = cms.PSet(CandVars,
      statusFlags = process.genParticleTable.variables.statusFlags,
    )
  )
  process.customGenConstituentsTable.variables.pdgId = Var("pdgId()", int, doc="pdgId from MC truth")
  process.customizedJetCandsTask.add(process.customGenConstituentsTable)

  #keep maximum precision for 4-vector
  process.customGenConstituentsTable.variables.pt.precision = -1
  process.customGenConstituentsTable.variables.eta.precision = -1
  process.customGenConstituentsTable.variables.phi.precision = -1
  process.customGenConstituentsTable.variables.mass.precision = -1

  if doAK8:
    process.customAK8GenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      candidates = process.customGenConstituentsTable.src,
      jets = process.genJetAK8Table.src,
      name = cms.string("GenJetAK8Cand"),
      idx_name = cms.string("GenCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK8GenConstituentsTable)

  if doAK8Subjets:
    process.customAK8SubJetGenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      candidates = process.customGenConstituentsTable.src,
      jets = process.genSubJetAK8Table.src,
      name = cms.string("SubGenJetAK8Cand"),
      idx_name = cms.string("GenCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK8SubJetGenConstituentsTable)

  if doAK4:
    process.customAK4GenConstituentsTable = cms.EDProducer("SimpleGenJetConstituentTableProducer",
      candidates = process.customGenConstituentsTable.src,
      jets = process.genJetTable.src,
      name = cms.string("GenJetCand"),
      idx_name = cms.string("GenCandIdx"),
    )
    process.customizedJetCandsTask.add(process.customAK4GenConstituentsTable)

def PrepJMEPFCustomNanoAOD(process, runOnMC, saveOnlyPFCandsInJets=True, saveGenJetCands=False, saveOnlyGenCandsInJets=True):
  process.customizedJetCandsTask = cms.Task()
  process.schedule.associate(process.customizedJetCandsTask)

  # process = PrepPuppiProducer(process) #jetsFromMini

  ###################################
  #
  # Reco-jets and PF candidates
  #
  ###################################
  if saveOnlyPFCandsInJets:
    process, candList = PrepJetConstituents(
      process,
      doAK8Puppi=True,
      doAK4Puppi=True,
      doAK4CHS=True
    )
    process.finalJetsConstituents = cms.EDProducer("PackedCandidatePtrMerger",
      src = candList,
      skipNulls = cms.bool(True),
      warnOnSkip = cms.bool(True)
    )
    process.customizedJetCandsTask.add(process.finalJetsConstituents)
    candInputForTable = cms.InputTag("finalJetsConstituents")
  else:
    # NOTE: Store all packedPFCandidates
    candInputForTable = cms.InputTag("packedPFCandidates")

  process = PrepJetConstituentTables(
    process,
    candInputForTable,
    saveOnlyPFCandsInJets=saveOnlyGenCandsInJets,
    doAK8Puppi=True,
    doAK4Puppi=True,
    doAK4CHS=True
  )
  process.customPFConstituentsTable.variables.passCHS.expr = process.packedPFCandidateschs.cut.value()
  process.customPFConstituentsTable.variables.passCHS.doc = process.packedPFCandidateschs.cut.value()

  if not(saveOnlyPFCandsInJets):
    process.customPFConstituentsTable.doc = "PF Candidates"

  ###################################
  #
  # GenJets and Gen candidates
  #
  ###################################
  if runOnMC and saveGenJetCands:
    candInputForTable = None
    if saveOnlyGenCandsInJets:
      process, genCandList = PrepGenJetConstituents(
        process,
        doAK8=True,
        doAK4=True
      )
      process.finalGenJetsConstituents = cms.EDProducer("PackedGenParticlePtrMerger",
        src = genCandList,
        skipNulls = cms.bool(True),
        warnOnSkip = cms.bool(True)
      )
      process.customizedJetCandsTask.add(process.finalGenJetsConstituents)
      candInputForTable = cms.InputTag("finalGenJetsConstituents")
    else:
      # NOTE: Store all packedPFCandidates
      candInputForTable = cms.InputTag("packedGenParticles")

    process = PrepGenJetConstituentTables(
      process,
      candInputForTable,
      saveOnlyGenCandsInJets=saveOnlyGenCandsInJets,
      doAK8=True,
      doAK4=True,
    )
    if not(saveOnlyGenCandsInJets):
      process.customGenConstituentsTable.doc = "Particle-level Gen Candidates"

  return process

def PrepJMEPFCustomNanoAOD_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True)
  return process

def PrepJMEPFCustomNanoAOD_SaveGenJetCands_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True,saveGenJetCands=True,saveOnlyGenCandsInJets=True)
  return process

def PrepJMEPFCustomNanoAOD_Data(process):
  PrepJMECustomNanoAOD_Data(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=False)
  return process

def PrepJMEPFCustomNanoAOD_SavePFAll_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True,saveOnlyPFCandsInJets=False)
  return process

def PrepJMEPFCustomNanoAOD_SavePFAll_Data(process):
  PrepJMECustomNanoAOD_Data(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=False,saveOnlyPFCandsInJets=False)
  return process
