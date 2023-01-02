#
# First try work with 12_6_X and be compatible for Run-3 and Run-2 samples.
#
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, CandVars
from PhysicsTools.NanoAOD.custom_jme_cff import PrepJMECustomNanoAOD_MC, PrepJMECustomNanoAOD_Data
from PhysicsTools.NanoAOD.nano_eras_cff import run2_nanoAOD_ANY

def PrepJMEPFCustomNanoAOD(process, runOnMC):
  process.customizedPFCandsTask = cms.Task()
  process.schedule.associate(process.customizedPFCandsTask)
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
    src = cms.InputTag("finalJetsPuppi"),
    cut = cms.string("pt > 8")
  )
  process.customizedPFCandsTask.add(process.finalJetsAK4PuppiConstituents)

  #
  #
  #
  #
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
    vtxChi2 = Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2",precision=10),
    trkChi2 = Var("?hasTrackDetails()?pseudoTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=10),
    dz = Var("?hasTrackDetails()?dz():-1", float, doc="pf dz", precision=10),
    dzErr = Var("?hasTrackDetails()?dzError():-1", float, doc="pf dz err", precision=10),
    d0 = Var("?hasTrackDetails()?dxy():-1", float, doc="pf d0", precision=10),
    d0Err = Var("?hasTrackDetails()?dxyError():-1", float, doc="pf d0 err", precision=10),
    pvAssocQuality = Var("pvAssociationQuality()", int, doc="primary vertex association quality"),
    lostInnerHits = Var("lostInnerHits()", int, doc="lost inner hits"),
    trkQuality = Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
    )
  )
  process.customizedPFCandsTask.add(process.customPFConstituentsTable)

  process.customPFConstituentsExtTable = cms.EDProducer("PFCandidateExtTableProducer",
    srcPFCandidates = process.customPFConstituentsTable.src,
    name = process.customPFConstituentsTable.name,
    srcWeights = cms.InputTag("packedPFCandidatespuppi"),
    weightName = cms.string("puppiWeightRecomputed"),
    weightDoc = cms.string("Recomputed Puppi Weights"),
    weightPrecision = cms.int(process.customPFConstituentsTable.variables.precision),
  )
  process.customizedPFCandsTask.add(process.customPFConstituentsExtTable)


  process.customAK8ConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJetsAK8"),
    name = cms.string("FatJetPFCand"),
    idx_name = cms.string("pFCandsIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK8ConstituentsTable)

  process.customAK4CHSConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJets"),
    name = cms.string("JetCHSPFCand"),
    idx_name = cms.string("pFCandsIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4CHSConstituentsTable)

  process.customAK4PuppiConstituentsTable = cms.EDProducer("SimplePatJetConstituentTableProducer",
    candidates = candInputForTable,
    jets = cms.InputTag("finalJetsPuppi"),
    name = cms.string("JetPFCand"),
    idx_name = cms.string("pFCandsIdx"),
  )
  process.customizedPFCandsTask.add(process.customAK4PuppiConstituentsTable)
  
  #
  # Switch to AK4 CHS jets for Run-2
  #
  # print(run2_nanoAOD_ANY)
  # run2_nanoAOD_ANY.toModify(
  #   process.customAK4CHSConstituentsTable, name="JetPFCand"
  # ).toModify(
  #   process.customAK4PuppiConstituentsTable, name="JetPuppiPFCand"
  # )

  return process

def PrepJMEPFCustomNanoAOD_MC(process):
  PrepJMECustomNanoAOD_MC(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=True)
  return process

def PrepJMEPFCustomNanoAOD_Data(process):
  PrepJMECustomNanoAOD_Data(process)
  PrepJMEPFCustomNanoAOD(process,runOnMC=False)
  return process