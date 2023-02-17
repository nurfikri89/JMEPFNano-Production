# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step1 --mc --fileout file:./tree_jmepfnano_default_puppiRecompute_MC22_mini_tt.root --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 126X_mcRun3_2022_realistic_v2 --step NANO --era Run3,run3_nanoAOD_124 --python_filename ./JME-Run3Summer22NanoAOD_mini_tt_jmepfnano_default_puppiRecompute_cfg.py --no_exec -n 10 --filein=file:/afs/cern.ch/user/n/nbinnorj/work/Samples/Mini/store/mc/Run3Summer22MiniAODv3/TT_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v3/70000/ac3541ad-110b-4273-9827-99298b27dd67.root --customise_commands=from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)\n process.packedPFCandidatespuppi.useExistingWeights=False\n process.pfDeepFlavourTagInfosAK4PFCHSFinal.puppi_value_map='packedPFCandidatespuppi'\n process.pfDeepFlavourTagInfosAK4PFPUPPIFinal.puppi_value_map='packedPFCandidatespuppi'\n process.pfParticleNetAK4TagInfosAK4PFCHSFinal.puppi_value_map='packedPFCandidatespuppi'\n process.pfParticleNetAK4TagInfosAK4PFPUPPIFinal.puppi_value_map='packedPFCandidatespuppi'\n process.pfInclusiveSecondaryVertexFinderTagInfosAK4PFCHSFinal.weights='packedPFCandidatespuppi'\n process.pfInclusiveSecondaryVertexFinderTagInfosAK4PFPUPPIFinal.weights='packedPFCandidatespuppi'\n 
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.Eras.Modifier_run3_nanoAOD_124_cff import run3_nanoAOD_124

process = cms.Process('NANO',Run3,run3_nanoAOD_124)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/afs/cern.ch/user/n/nbinnorj/work/Samples/Mini/store/mc/Run3Summer22MiniAODv3/TT_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/124X_mcRun3_2022_realistic_v12-v3/70000/ac3541ad-110b-4273-9827-99298b27dd67.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step1 nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:tree.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '126X_mcRun3_2022_realistic_v2', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# End of customisation functions


# Customisation from command line

from JMEPFNano.Production.custom_jme_pf_nano_cff import PrepJMEPFCustomNanoAOD_MC; PrepJMEPFCustomNanoAOD_MC(process)
process.packedPFCandidatespuppi.useExistingWeights=False
process.pfDeepFlavourTagInfosAK4PFCHSFinal.puppi_value_map='packedPFCandidatespuppi'
process.pfDeepFlavourTagInfosAK4PFPUPPIFinal.puppi_value_map='packedPFCandidatespuppi'
process.pfParticleNetAK4TagInfosAK4PFCHSFinal.puppi_value_map='packedPFCandidatespuppi'
process.pfParticleNetAK4TagInfosAK4PFPUPPIFinal.puppi_value_map='packedPFCandidatespuppi'
process.pfInclusiveSecondaryVertexFinderTagInfosAK4PFCHSFinal.weights='packedPFCandidatespuppi'
process.pfInclusiveSecondaryVertexFinderTagInfosAK4PFPUPPIFinal.weights='packedPFCandidatespuppi'

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
