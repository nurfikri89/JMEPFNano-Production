#
# First try work with 12_6_X and be compatible for Run-3 and Run-2 samples.
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


def PrepJMEPFCustomNanoAOD(process, runOnMC):
  process.customizedPFCandsTask = cms.Task()
  process.schedule.associate(process.customizedPFCandsTask)
  
  #
  # NOTE: For CHS studies (new Definition)
  #
  # chsCutStr =  '(abs(pdgId)==130 || abs(pdgId)==11 || abs(pdgId)==22 || abs(pdgId)==13 || abs(pdgId)==1 || abs(pdgId)==2) || '
  # chsCutStr += '((abs(pdgId)==211) && (fromPV(0)>0 || (vertexRef().key<=2 && abs(dz(0))<0.2)))'
  # process.packedPFCandidateschs.cut = chsCutStr

  #
  # NOTE: We setup "packedPFCandidatespuppi" here if not done in JMENano.
  # Situation where this can happen is when we use slimmedJets and slimmedJetsPuppi
  # for the input jet collection table
  #
  # puppiForJetReclusterInJMENano="packedPFCandidatespuppi"
  # if not hasattr(process,puppiForJetReclusterInJMENano): #jetsFromMini
  #   addProcessAndTask(process, puppiForJetReclusterInJMENano, puppi.clone(
  #       candName = "packedPFCandidates",
  #       vertexName = "offlineSlimmedPrimaryVertices",
  #       clonePackedCands = True,
  #       useExistingWeights = True,
  #     )
  #  )

  #
  #
  #
  saveOnlyPFCandsInJets = False
  if saveOnlyPFCandsInJets:
    # Collect AK8 Puppi Constituents pointers
    process.finalJetsAK8Constituents = cms.EDProducer("PatJetConstituentPtrSelector",
      src = cms.InputTag("finalJetsAK8"),
      cut = cms.string("")
    )
    process.customizedPFCandsTask.add(process.finalJetsAK8Constituents)

    # Collect AK4 CHS Constituents pointers
    process.finalJetsAK4CHSConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
      src = cms.InputTag("finalJets"),
      cut = cms.string("pt > 8")
    )
    process.customizedPFCandsTask.add(process.finalJetsAK4CHSConstituents)

    # Collect AK4 Puppi Constituents pointers
    process.finalJetsAK4PuppiConstituents = cms.EDProducer("PatJetConstituentPtrSelector",
      src = cms.InputTag("finalJetsPuppi"),
      cut = cms.string("pt > 8")
    )
    process.customizedPFCandsTask.add(process.finalJetsAK4PuppiConstituents)
    # Merge all the pointers
    candList = cms.VInputTag(
      cms.InputTag("finalJetsAK8Constituents", "constituents"),
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
  else:
    # NOTE: Store all packedPFCandidates
    candInputForTable = cms.InputTag("packedPFCandidates")

  process.customPFConstituentsTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
  src = candInputForTable,
  cut = cms.string(""), #we should not filter
  name = cms.string("PFCand"),
  doc = cms.string("interesting particles from AK4 and AK8 jets"),
  singleton = cms.bool(False), # the number of entries is variable
  extension = cms.bool(False), # this is the extension table for the AK8 constituents
  variables = cms.PSet(CandVars,
    puppiWeight = Var("puppiWeight()", float, doc="Puppi weight",precision=-1),
    puppiWeightNoLep = Var("puppiWeightNoLep()", float, doc="Puppi weight removing leptons",precision=-1),
    vtxChi2 = Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2",precision=15),
    trkChi2 = Var("?hasTrackDetails()?pseudoTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=15),
    dz = Var("?hasTrackDetails()?dz():-1", float, doc="pf dz", precision=15),
    dzErr = Var("?hasTrackDetails()?dzError():-1", float, doc="pf dz err", precision=15),
    d0 = Var("?hasTrackDetails()?dxy():-1", float, doc="pf d0", precision=15),
    d0Err = Var("?hasTrackDetails()?dxyError():-1", float, doc="pf d0 err", precision=15),
    pvAssocQuality = Var("pvAssociationQuality()", int, doc="primary vertex association quality (NotReconstructedPrimary = 0, OtherDeltaZ = 1, CompatibilityBTag = 4, CompatibilityDz = 5, UsedInFitLoose = 6, UsedInFitTight = 7)"),
    fromPV0 = Var("fromPV()", int, doc="PV0 association (NoPV = 0, PVLoose = 1, PVTight = 2, PVUsedInFit = 3)"),
    vertexRef = Var("?vertexRef().isNonnull()?vertexRef().key():-1", int, doc="vertexRef().key()"),
    lostInnerHits = Var("lostInnerHits()", int, doc="lost inner hits"),
    trkQuality = Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
    passCHS = Var(process.packedPFCandidateschs.cut.value(), bool, doc=process.packedPFCandidateschs.cut.value()),
    # passCHS = Var(pfCHS.cut.value(), bool, doc=pfCHS.cut.value()), #jetsFromMini
    )
  )
  #keep maximum precision for 4-vector
  process.customPFConstituentsTable.variables.pt.precision = -1 
  process.customPFConstituentsTable.variables.eta.precision = -1
  process.customPFConstituentsTable.variables.phi.precision = -1
  process.customPFConstituentsTable.variables.mass.precision = -1

  process.customizedPFCandsTask.add(process.customPFConstituentsTable)

  process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
    srcPFCandidates = process.customPFConstituentsTable.src,
    name = process.customPFConstituentsTable.name,
    srcWeights = cms.InputTag("packedPFCandidatespuppi"),
    weightName = cms.string("puppiWeightValueMap"),
    weightDoc = cms.string("Puppi Weight (ValueMap from PuppiProducer)"),
    weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  )
  process.customizedPFCandsTask.add(process.customPFConstituentsExtTable)

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
  #     "puppiWeightRecomputed",
  #   ),
  #   weightDocsV = cms.vstring(
  #     "Recomputed Puppi Weights",
  #   ),
  #   weightPrecision = process.customPFConstituentsTable.variables.puppiWeight.precision,
  # )
  # process.customizedPFCandsTask.add(process.customPFConstituentsExtTable)

  process.customAK8ConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = process.customPFConstituentsTable.src,
    jets = cms.InputTag("finalJetsAK8"),
    name = cms.string("FatJetPFCand"),
    idx_name = cms.string("pfCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK8ConstituentsTable)

  process.customAK4CHSConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = process.customPFConstituentsTable.src,
    jets = cms.InputTag("finalJets"),
    name = cms.string("JetCHSPFCand"),
    idx_name = cms.string("pfCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4CHSConstituentsTable)

  process.customAK4PuppiConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = process.customPFConstituentsTable.src,
    jets = cms.InputTag("finalJetsPuppi"),
    name = cms.string("JetPFCand"),
    idx_name = cms.string("pfCandIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4PuppiConstituentsTable)
  
  #
  # Switch to AK4 CHS jets for Run-2
  #
  run2_nanoAOD_ANY.toModify(
    process.customAK4CHSConstituentsTable, name="JetPFCand"
  )
  run2_nanoAOD_ANY.toModify(
    process.customAK4PuppiConstituentsTable, name="JetPuppiPFCand"
  )

  return process

def PrepJMEPFCustomNanoAOD_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True)
  return process

def PrepJMEPFCustomNanoAOD_Data(process):
  PrepJMECustomNanoAOD_Data(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=False)
  return process
